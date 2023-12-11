import cv2
import threading
import time
import os


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
        pass

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
