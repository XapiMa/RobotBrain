# -*- coding: utf-8 -*-
import cv2
import numpy as np
import colorsys

px = 0
py = 0
qx = 0
qy = 0
h_min, s_min, v_min = 0,0,0
h_max, s_max, v_max = 0,0,0
drawing = False

col = np.array([0,0,0])

im_hsv = np.zeros((320,240))

def pick_color(event, x, y, flags, param):
    global px, py
    global qx, qy
    global col
    global h_min, s_min, v_min
    global h_max, s_max, v_max
    global drawing
    global im_hsv
    if event == cv2.EVENT_LBUTTONDOWN:
        if drawing == False:
	    px = x
	    py = y
	    print "(x,y)=", x, y
	    #px = im[x,y]
	    print "hsv=",colorsys.rgb_to_hsv(px[2], px[1], px[0])
	    col = im_hsv[y,x]
	    #print "col=", col
	    #print "hsv=", im_hsv[y,x]
	    #print "bgr=", im[y,x]
	    drawing == True

    if event == cv2.EVENT_LBUTTONUP:
#        if drawing == True:
	    qx = x
	    qy = y
	    roi = im_hsv[py:qy,px:qx]
	    h,s,v = cv2.split(roi)
	    h_min = np.min(h)
	    h_max = np.max(h)
	    s_min = np.min(s)
	    s_max = np.max(s)
	    v_min = np.min(v)
	    v_max = np.max(v)
	    drawing = False

def detect_color(imc):
    global im_hsv
    im_hsv = cv2.cvtColor(imc, cv2.COLOR_BGR2HSV)
    #cv2.circle(imc, (px,py), 5, (0, 0, 255), -1)
    if drawing==True:
        cv2.rectangle(imc, (px, py), (qx, qy), (0, 0, 255), 1)

    # 緑色(HSV)の範囲を定義
    green_min = np.array([h_min,s_min,v_min])
    green_max = np.array([h_max,s_max,v_max])
    # マスク画像を用いて元画像から指定した色を抽出
    mask_green = cv2.inRange(im_hsv, green_min, green_max)
    im_green = cv2.bitwise_and(imc,imc, mask=mask_green)
    
    # 輪郭検出
    contours, hierarcy = cv2.findContours(mask_green, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    max_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            best_cnt= cnt
    x,y = -1,-1
    w,h = 0, 0
    if max_area!=0:
        x,y,w,h = cv2.boundingRect(best_cnt)
        cv2.rectangle(imc, (x,y), (x+w, y+h), (0,255,0), 2)
    
    return im_green, x+w/2, y+h/2, w, h

