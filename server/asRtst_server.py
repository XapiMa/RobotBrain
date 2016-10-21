# -*- coding: utf-8 -*-

import asyncore
import socket

import cv2
from RoombaSCI_ogi import RoombaAPI


class RoombaHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)
        if data:
            # 以下のようなことがしたいが，スコープの関係上そんなことはできない
            # key = data
            # ########################
            # #### キーボードの入力 ####
            # ########################
            # if key == 'q':    # ESC キー: 終了
            #
            # if key == 'j': # 上矢印キー: 前進
            #     x.forward()
            # if key == 'k': # 下矢印キー: 後退
            #     x.backward()
            # if key == 'l': # 右矢印キー: 右回転
            #     x.spin_right()
            # if key == 'h': # 左矢印キー: 左回転
            #     x.spin_left()
            # if key == 'z':    # スペースキー: 停止
            #     x.stop()
            self.send(data)     #入力データの確認を返す(省略可能)

class RoombaServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)


    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = RoombaHandler(sock)

# ルンバの接続の初期化
port = "/dev/cu.usbserial-A2001n4D" #ここは各自で違う！
baudrate = 115200
x = RoombaAPI(port, baudrate)
x.start()
x.full()

#非同期サーバとして稼働
server = RoombaServer('10.1.161.1', 5610)
asyncore.loop()

# 終了時の処理
cv2.destroyAllWindows()
x.off()
x.close()
