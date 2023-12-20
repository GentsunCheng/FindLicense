import cv2
import threading
import time
import os
import numpy as np


class PreCam(object):
    def __init__(self):
        self.BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../source/"))
        self.stop_flag = False
        self.debug = False
        self.cap_id = 0
        self.pre_im = cv2.imread(os.path.join(self.BASE_PATH, "load.png"), 1)
        self.proc_im = self.pre_im
        self.proc_im = cv2.cvtColor(self.pre_im, cv2.COLOR_BGR2GRAY)
        ret, self.proc_im = cv2.threshold(self.proc_im, 127, 255, cv2.THRESH_BINARY)
        self.lock = threading.Lock()
        self.cam_thread = threading.Thread(target=self.camera)
        self.proc_thread = threading.Thread(target=self.im_process)

    def camera(self):
        cap = cv2.VideoCapture(self.cap_id)
        while not self.stop_flag:
            ret, frame = cap.read()
            with self.lock:
                self.pre_im = frame

    def im_process(self):
        while not self.stop_flag:
            time.sleep(0.05)
            with self.lock:
                # 将图像转换为HSV颜色空间
                hsv = cv2.cvtColor(self.pre_im, cv2.COLOR_BGR2HSV)

                # 定义颜色范围
                lower_blue = np.array([100, 50, 50])
                upper_blue = np.array([140, 255, 255])
                lower_green = np.array([50, 50, 50])
                upper_green = np.array([70, 255, 255])
                lower_yellow = np.array([20, 100, 100])
                upper_yellow = np.array([30, 255, 255])

                # 创建掩模以选择特定颜色范围
                mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
                mask_green = cv2.inRange(hsv, lower_green, upper_green)
                mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

                # 合并掩模
                combined_mask = cv2.bitwise_or(mask_blue, cv2.bitwise_or(mask_green, mask_yellow))

                # 保留选定区域，其他区域填充为白色
                self.proc_im = cv2.bitwise_and(self.pre_im, self.pre_im, mask=combined_mask)

                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
                self.proc_im = cv2.morphologyEx(self.proc_im, cv2.MORPH_OPEN, kernel)
                self.proc_im = cv2.morphologyEx(self.proc_im, cv2.MORPH_CLOSE, kernel)

                # 寻找轮廓并填充
                contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for contour in contours:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(self.proc_im, (x, y), (x + w, y + h), (255, 255, 255), thickness=cv2.FILLED)

    def start(self, debug=False, cap_id=0):
        self.cap_id = cap_id
        self.debug = debug
        self.cam_thread.start()
        self.proc_thread.start()

    def stop(self):
        self.stop_flag = True
        self.cam_thread.join()
        self.proc_thread.join()
        self.pre_im = cv2.imread(os.path.join(self.BASE_PATH, "load.png"), 1)
        self.proc_im = self.pre_im
        self.proc_im = cv2.cvtColor(self.proc_im, cv2.COLOR_BGR2GRAY)
        ret, self.proc_im = cv2.threshold(self.proc_im, 127, 255, cv2.THRESH_BINARY)

    def get_im(self, process=True):
        with self.lock:
            if process:
                return self.proc_im
            else:
                return self.pre_im


if __name__ == '__main__':
    pre_cam = PreCam()
    pre_cam.start()

    while True:
        img = pre_cam.get_im()
        cv2.imshow("img", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pre_cam.stop()
            break
