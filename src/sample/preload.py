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
                # 转换图像到HSV颜色空间
                hsv = cv2.cvtColor(self.pre_im, cv2.COLOR_BGR2HSV)
                hsv = cv2.addWeighted(hsv, 1.0, hsv, 0, 5)

                # 定义颜色范围
                lower_blue = np.array([100, 50, 50])
                upper_blue = np.array([130, 255, 255])
                lower_green = np.array([40, 40, 40])
                upper_green = np.array([80, 255, 255])
                lower_yellow = np.array([20, 100, 100])
                upper_yellow = np.array([30, 255, 255])

                # 创建掩模以选择特定颜色范围
                mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
                mask_green = cv2.inRange(hsv, lower_green, upper_green)
                mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
                # 合并掩模
                self.proc_im = cv2.bitwise_or(mask_blue, cv2.bitwise_or(mask_green, mask_yellow))
                self.proc_im = self.pre_im.copy()
                self.proc_im = cv2.cvtColor(self.proc_im, cv2.COLOR_BGR2GRAY)
                ret, self.proc_im = cv2.threshold(self.proc_im, 127, 255, cv2.THRESH_BINARY)
                # 腐蚀（erode）和膨胀（dilate）
                kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 1))
                kernelY = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 20))
                # x方向进行闭操作（抑制暗细节）
                self.proc_im = cv2.dilate(self.proc_im, kernelX)
                self.proc_im = cv2.erode(self.proc_im, kernelX)
                # y方向的开操作
                self.proc_im = cv2.erode(self.proc_im, kernelY)
                self.proc_im = cv2.dilate(self.proc_im, kernelY)
                # 中值滤波
                self.proc_im = cv2.medianBlur(self.proc_im, 5)
                # 高斯滤波
                self.proc_im = cv2.GaussianBlur(self.proc_im, (5, 5), 0)
                # 双边滤波
                self.proc_im = cv2.bilateralFilter(self.proc_im, 9, 75, 75)

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
