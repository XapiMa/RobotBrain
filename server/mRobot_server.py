
# -*- coding: utf-8 -*-

from multiprocessing import Process
import socket
import time

import cv2
from RoombaSCI_ogi import RoombaAPI

PROCESSES = 5
SERVER_IP = '10.1.161.1'
SERVER_PORT = 5600



class mRobotServer(object):

    def __init__(self, host, port, processes):
        self._server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_sock.bind((host, port))
        self._server_sock.listen(processes)
        self.processes = processes

    def start(self, handler):
        for num in range(self.processes):
            p = Process(target=handler, args=(self._server_sock,))
            p.daemon = True
            p.start()
        self._parent_main_loop()

    def _parent_main_loop(self):
        while True:
            while True:
                # 引数としてルンバの接続のインスタンスを渡してしまい，それぞれの子プロセスでルンバを操作する！！
                # #子プロセスで受けた命令を親プロセスに集め，親プロセスが一括でルンバとの通信を行う
                # #親プロセスはルンバのセンサー情報を子プロセスに送信し，子プロセスは通信相手にセンサー情報を転送する
                # #子プロセスからの命令で親プロセスを終了する
                time.sleep(0.01)


class RSockerStreamHandler(object):

    def __init__(self,Roomba):
        self._sock = None
        self._address = None
        self.Roomba = Roomba

    def __call__(self, server_sock):
        while True:
            (self._sock, self._addr) = server_sock.accept()
            with self:
                self.handle()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        self._sock.shutdown(socket.SHUT_RDWR)
        self._sock.close()

    def handle(self):
        raise NotImplementedError




class mRHendler(RSockerStreamHandler):

    def handle(self):
        while True:
            print "connected by" , self._addr
            data = self._sock.recv(1024)
            if not data : break
                ########################
                #### キーボードの入力 ####
                ########################
                if key == 'q':    # ESC キー: 終了
                    break
                if key == 'j': # 上矢印キー: 前進
                    Roomba.forward()
                if key == 'k': # 下矢印キー: 後退
                    Roomba.backward()
                if key == 'l': # 右矢印キー: 右回転
                    Roomba.spin_right()
                if key == 'h': # 左矢印キー: 左回転
                    Roomba.spin_left()
                if key == 'z':    # スペースキー: 停止
                    Roomba.stop()

                if Roomba.sensors.bumps.left==True:
                    print u"バンパーに何かあたったよ"
                    self._sock.send(U"バンパーに何かあたったよ")
                    Roomba.stop()
            self._sock.send(data)   #送信データの確認



if __name__ =='__main__':
    # ルンバの接続の初期化
    port = "/dev/cu.usbserial-A2001n4D"
    baudrate = 115200

    Roomba = RoombaAPI(port, baudrate)

    Roomba.start()
    Roomba.full()


    # 画像の読み込み
    img = cv2.imread("face.png",0)

    server = mRobotServer(SERVER_IP,SERVER_PORT, PROCESSES)
    handler = mRHendler(Roomba)
    server.start(handler)
