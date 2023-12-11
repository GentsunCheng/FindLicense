import cv2
import threading
import time
import os


class PreCam(object):
    def __init__(self):
        self.BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../source/"))
        self.stop_flag = False
        self.pre_im = cv2.imread(os.path.join(self.BASE_PATH, "load.png"), 1)
        self.proc_im = self.pre_im
        self.proc_im = cv2.cvtColor(self.pre_im, cv2.COLOR_BGR2GRAY)
        ret, self.proc_im = cv2.threshold(self.proc_im, 127, 255, cv2.THRESH_BINARY)
        self.lock = threading.Lock()
        self.cam_thread = threading.Thread(target=self.camera)
        self.proc_thread = threading.Thread(target=self.im_process)
        pass

    def camera(self):
        cap = cv2.VideoCapture(0)
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

    def start(self):
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
