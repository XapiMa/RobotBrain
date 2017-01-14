# -*- coding: utf-8 -*-
import cv2
import numpy as np
import time
import sys


class HurrySim(object):

    def __init__(self, name):
	    self.im = None
	    self.im_h = 0
	    self.im_w = 0
	    self.name = name
	    self.cap = cv2.VideoCapture(0)
	    self.cap.set(3, 640)  # カメラの横のサイズ
	    self.cap.set(4, 480)  # カメラの縦のサイズ
	    cv2.namedWindow(self.name)
	    self.recognize_line()
	    self.roops()

    def roops(self):
		while True:
			self.recognize_line()
			time.sleep(0.1)

    def recognize_line(self):
	    # 各座標の取得・表示・画面描画を行う
	    xa1, xa2, xb1, xb2 = self.line_pos(200, 350, 200, None)
	    print xa1, xa2, xb1, xb2, self.im_w
	    return xa1, xa2, xb1, xb2

    def line_pos(self, ya, yb, thd, im=None):
	    errorCode, image = self.cap.read()
	    # errorCode, resolution, image = vrep.simxGetVisionSensorImage(
	    #     self.clientID, self.cam_handle, 0, vrep.simx_opmode_streaming)

	    if errorCode == True:
	        im = np.array(image, dtype=np.uint8)         # numpy に変換
	        # im.resize([resolution[0], resolution[1], 3])  # サイズを変換
	        im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)     # 色を変換 RGB -> BGR
	        im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
	        im = cv2.flip(im, 0)
	        image = im.copy()
	        yoko_a = image[ya, :]
	        yoko_b = image[yb, :]

	        xmax = image.shape[1]
	        xmid = xmax / 2
	        # print xmax, xmid

	        if np.max(yoko_a[0:xmid]) < thd:
	            xa1 = -1
	        else:
	            xa1 = np.argmax(yoko_a[0:xmid])

	        if np.max(yoko_a[xmid:xmax]) < thd:
	            xa2 = -1
	        else:
	            xa2 = np.argmax(yoko_a[xmid:xmax]) + xmid

	        if np.max(yoko_b[0:xmid]) < thd:
	            xb1 = -1
	        else:
	            xb1 = np.argmax(yoko_b[0:xmid])

	        if np.max(yoko_b[xmid:xmax]) < thd:
	            xb2 = -1
	        else:
	            xb2 = np.argmax(yoko_b[xmid:xmax]) + xmid

	        # draw line
	        cv2.line(image, (0, ya), (xmax, ya), 100, 2)
	        cv2.line(image, (0, yb), (xmax, yb), 100, 2)

	        if xa1 != -1:
	            cv2.circle(image, (xa1, ya), 10, 100, -1)
	        if xa2 != -1:
	            cv2.circle(image, (xa2, ya), 10, 100, -1)
	        if xb1 != -1:
	            cv2.circle(image, (xb1, yb), 10, 100, -1)
	        if xb2 != -1:
	            cv2.circle(image, (xb2, yb), 10, 100, -1)
	        self.im_h = image.shape[0]
	        self.im_w = image.shape[1]
	        self.im = image
	        self.show_im()

	        return xa1, xa2, xb1, xb2

	    else:
	        return -2, -2, -2, -2

    def show_im(self):
    	cv2.imshow(self.name, self.im)
        ex = cv2.waitKey(1)
        if ex == 'e':
			sys.exit()

rmb = HurrySim("rmb")
cv2.destroyAllWindows()
