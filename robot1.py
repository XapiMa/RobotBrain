# -*- coding: utf-8 -*-

import cv2
from RoombaSCI import RoombaAPI

# ルンバの接続の初期化
port = "/dev/cu.usbserial-A2001n4D"
baudrate = 115200

x = RoombaAPI(port, baudrate)

x.start()   # 前回から若干修正！
x.full()

# 画像の読み込み
img = cv2.imread("face.png",0)

# 無限ループ
while 1:
    cv2.imshow('image',img)

    key = cv2.waitKey(30)
    if key == 27:  # ESC キーが入力されたら終了
        break
    if key == 63232:  #↑
        x.forward()
    if key == 63233:#↓
        x.backward()
    if key == 63235:
        x.spin_right()#->
    if key == 63234: #<-
        x.spin_left()
    if key == 32:  # space が押されたらストップ
        x.stop()

# 終了時の処理
cv2.destroyAllWindows()
x.off()
x.close()
