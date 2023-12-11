import os
import time
import cv2
import numpy as np

class FindLicense(object):
    def __init__(self):
        self.plate_num = ""
        self.BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../source/"))
        self.pre_im = cv2.imread(os.path.join(self.BASE_PATH, "load.png"), 1)
        self.proc_im = self.pre_im
        self.proc_im = cv2.cvtColor(self.proc_im, cv2.COLOR_BGR2GRAY)
        ret, self.proc_im = cv2.threshold(self.proc_im, 127, 255, cv2.THRESH_BINARY)
        self.im_plate = self.pre_im
        self.template = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U',
                         'V', 'W', 'X', 'Y', 'Z',
                         '藏', '川', '鄂', '甘', '赣', '贵', '桂', '黑', '沪', '吉', '冀', '津', '晋', '京', '辽', '鲁',
                         '蒙', '闽', '宁',
                         '青', '琼', '陕', '苏', '皖', '湘', '新', '渝', '豫', '粤', '云', '浙']

    def identify(self):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        self.im_plate = cv2.dilate(self.im_plate, kernel)
        self.im_plate = cv2.cvtColor(self.im_plate, cv2.COLOR_BGR2HSV)
        self.im_plate = cv2.addWeighted(self.im_plate, 0.5, self.im_plate, 0, 50)
        self.im_plate = cv2.cvtColor(self.im_plate, cv2.COLOR_BGR2GRAY)
        ret, self.im_plate = cv2.threshold(self.im_plate, 110, 255, cv2.THRESH_BINARY)
        cv2.imshow("plate", self.im_plate)

    def get_plate(self, pre_im=None, proc_im=None, debug=False):
        time.sleep(0.05)
        pre_im = self.pre_im if pre_im is None else pre_im
        proc_im = self.proc_im if proc_im is None else proc_im

        # 进行边缘检测
        edges = cv2.Canny(proc_im, 50, 150)
        # 进行轮廓检测
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 找到可能的车牌区域
        possible_plates = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h
            if 2 < aspect_ratio < 5:
                possible_plates.append((x, y, w, h))

        # 选择最大的区域
        max_plate = max(possible_plates, key=lambda x: x[2] * x[3], default=None)

        # 在pre_im上切割出车牌区域
        if max_plate is not None:
            x, y, w, h = max_plate
            cv2.rectangle(pre_im, (x, y), (x + w, y + h), (0, 255, 0), 2)
            self.im_plate = pre_im[y:y + h, x:x + w]
            # 识别车牌
            self.identify()
        else:
            self.plate_num = ''

        # 在原图上绘制车牌区域
            if debug:
                cv2.rectangle(proc_im, (x, y), (x + w, y + h), (0, 255, 0), 2)
            else:
                cv2.rectangle(pre_im, (x, y), (x + w, y + h), (0, 255, 0), 2)
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
