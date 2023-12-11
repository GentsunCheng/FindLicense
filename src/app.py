import cv2
import argparse
import sample.recognize as rgz
import sample.preload as prd

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='车牌识别程序')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()

    pre_cam = prd.PreCam()
    pre_cam.start()
    find = rgz.FindLicense()
    while True:
        im, num = find.get_plate(pre_im=pre_cam.get_im(process=False), proc_im=pre_cam.get_im(process=True), debug=args.debug)
        cv2.imshow('image', im)
        if num:
            print("车牌号是:", num)
        else:
            print("未识别到车牌号")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    pre_cam.stop()
