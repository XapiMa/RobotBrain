# -*- coding: utf-8 -*-

import cv2
from RoombaSCI import RoombaAPI
#from __future__ import print_function
import socket
from contextlib import closing

def main():
    # ルンバの接続の初期化
    port = "/dev/cu.usbserial-A2001n4D" #ここは各自で違う！
    baudrate = 115200

    x = RoombaAPI(port, baudrate)

    x.start()   # 前回から若干修正！
    x.full()


    # 画像の読み込み
    img = cv2.imread("face.png",0)

    host = '172.29.240.115'
    port = 5800
    bufsize = 4096

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    with closing(sock):
      sock.bind((host, port))
      while True:
        key = sock.recv(bufsize)
        ########################
        #### キーボードの入力 ####
        ########################
        if key == 'q':    # ESC キー: 終了
            break
        if key == 'j': # 上矢印キー: 前進
            x.forward()
        if key == 'k': # 下矢印キー: 後退
            x.backward()
        if key == 'l': # 右矢印キー: 右回転
            x.spin_right()
        if key == 'h': # 左矢印キー: 左回転
            x.spin_left()
        if key == 'z':    # スペースキー: 停止
            x.stop()

        ###################
        #### 画像の表示 ####
        ##################
        cv2.imshow('image',img)

    # 終了時の処理
    cv2.destroyAllWindows()
    x.off()
    x.close()

if __name__ == '__main__':
    main()
