# -*- coding: utf-8 -*-

import cv2
from RoombaSCI import RoombaAPI

# ルンバの接続の初期化
port = "/dev/cu.usbserial-A2001n4D" #ここは各自で違う！
baudrate = 115200

x = RoombaAPI(port, baudrate)

x.start()   # 前回から若干修正！
x.full()


# 画像の読み込み
img = cv2.imread("face.png",0)

# 無限ループ
while 1:

    ########################
    #### キーボードの入力 ####
    ########################
    key = cv2.waitKey(30)
    if key == 27:    # ESC キー: 終了
        break
    if key == 63232: # 上矢印キー: 前進
        x.forward()
    if key == 63233: # 下矢印キー: 後退
        x.backward()
    if key == 63235: # 右矢印キー: 右回転
        x.spin_right()
    if key == 63234: # 左矢印キー: 左回転
        x.spin_left()
    if key == 32:    # スペースキー: 停止
        x.stop()

    ###################
    #### 画像の表示 ####
    ##################
    cv2.imshow('image',img)

# 終了時の処理
cv2.destroyAllWindows()
x.off()
x.close()
