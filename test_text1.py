# -*- coding: utf-8 -*-

import cv2

img = cv2.imread("face.png",1)
img2 = cv2.imread("angry.png",1)

mode=1

while 1:

    ########################
    #### キーボードの入力 ####
    ########################

    key = cv2.waitKey(30)
    if key == 27:  # ESC キーが入力されたら
        break
    if key == ord("h"):
        mode=1
        print u"こんにちは"
    if key == ord("a"):
        mode=2
        print u"あん？"

    ####################
    #### 画像の表示 ####
    ####################

    if mode==1:
        img3 = img.copy()
    if mode==2:
        img3 = img2.copy()

    cv2.imshow('image',img3)

# 終了時の処理
cv2.destroyAllWindows()
