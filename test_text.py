# -*- coding: utf-8 -*-

import cv2

img = cv2.imread("face.png",1)
            #1（カラーで読み込み)にする!

msg="Hello Python"

while 1:
    ########################
    #### キーボードの入力 ####
    ########################
    key = cv2.waitKey(30)
    if key == 27:  # ESC キー: 終了
        break
    if key == ord("a"):
        msg = "Hello Roomba"
        print u"こんにちは"
    if key == ord("b"):
        msg = "Angry!"
        print u"怒ったぞ!"

    #################################
    #### テキストを画像に書き込み ####
    #################################

    img2 = img.copy()  #書き込み用に画像をコピー

    # テキストの設定
    location=(0,30)   # テキストを出力する位置
    color=(255,0,0)   # テキストの色 rgb の 0~255
    fontface=cv2.FONT_HERSHEY_PLAIN  #フォント
    fontscale=2     #フォントの大きさ
    thickness=2     #フォントの太さ

    # 画像に書き込み
    cv2.putText(img2, msg, location, fontface, fontscale, color)

    ###################
    #### 画像の表示 ####
    ##################

    cv2.imshow('image',img2)

# 終了時の処理
cv2.destroyAllWindows()
