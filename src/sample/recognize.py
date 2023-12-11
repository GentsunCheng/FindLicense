import os
import time
import cv2


class FindLicense(object):
    def __init__(self):
        self.plate_num = ""
        self.BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../source/"))
        self.pre_im = cv2.imread(os.path.join(self.BASE_PATH, "load.png"), 1)
        self.proc_im = self.pre_im
        self.proc_im = cv2.cvtColor(self.proc_im, cv2.COLOR_BGR2GRAY)
        ret, self.proc_im = cv2.threshold(self.proc_im, 127, 255, cv2.THRESH_BINARY)
        pass

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
            # 假定车牌的长宽比例在2到5之间
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h
            if 2 < aspect_ratio < 5:
                possible_plates.append((x, y, w, h))
        # 在原图上绘制车牌区域
        for (x, y, w, h) in possible_plates:
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
