import cv2
import sys
import argparse
import sample.gui as gui
import sample.recognize as rgz
import sample.preload as prd
from PyQt6.QtWidgets import QApplication

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='车牌识别程序')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()

    prc_cam = prd.PreCam()
    prc_cam.start(cap_id=2)
    find = rgz.FindLicense()
    app = QApplication(sys.argv)
    gui_window = gui.MainWindow()
    gui_window.show()

    while True:
        im, num = find.get_plate(pre_im=prc_cam.get_im(process=False), proc_im=prc_cam.get_im(process=True),
                                 debug=args.debug)
        # 处理车牌号
        if num:
            numbers = "车牌号为：" + num
        else:
            numbers = "未识别到车牌号"
        # 处理图片
        height, width, _ = im.shape
        scale_factor = 720 / height
        new_width = int(width * scale_factor)
        new_height = 720
        image = cv2.resize(im, (new_width, new_height), interpolation=cv2.INTER_AREA)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 显示图片
        gui_window.update_gui(image, numbers)
        if (not gui_window.isVisible()) or (cv2.waitKey(1) & 0xFF == ord('q')):
            break

    prc_cam.stop()
    cv2.destroyAllWindows()
