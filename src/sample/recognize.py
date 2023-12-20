import os
import time
import cv2
import numpy as np
import hyperlpr3 as lpr3

class FindLicense(object):
    def __init__(self):
        self.plate_num = ""
        self.BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../source/"))
        self.pre_im = cv2.imread(os.path.join(self.BASE_PATH, "load.png"), 1)
        self.proc_im = self.pre_im
        self.proc_im = cv2.cvtColor(self.proc_im, cv2.COLOR_BGR2GRAY)
        ret, self.proc_im = cv2.threshold(self.proc_im, 127, 255, cv2.THRESH_BINARY)
        self.catcher = lpr3.LicensePlateCatcher()

    def get_plate(self, pre_im=None, proc_im=None, debug=False):
        time.sleep(0.05)
        self.pre_im = pre_im if pre_im is not None else self.pre_im
        self.proc_im = proc_im if proc_im is  not None else self.proc_im

        plate_im = cv2.bitwise_and(self.pre_im, self.proc_im)
        num_list = self.catcher(plate_im)
        if num_list and len(num_list) > 0:
            self.plate_num = num_list[0][0]
        else:
            self.plate_num = ""

        if debug:
            return proc_im, self.plate_num
        else:
            return pre_im, self.plate_num


if __name__ == '__main__':
    find = FindLicense()
    while True:
        im, plate_num = find.get_plate(debug=True)
        cv2.imshow('image', im)
        print("num is {}".format(plate_num))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
