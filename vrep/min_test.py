# -*- coding: utf-8 -*-
import sys
import minRmb
import time
import cv2
import socket
from contextlib import closing
# コマンドライン引数でパラメータを指定して実行する
# 学校のMac環境なら275が妥当。回転しすぎるなら大きく、回転不足なら小さくする

port = "/dev/cu.usbserial-A2001mJ7" #ここは各自で違う！
baudrate = 115200

param =275
if len(sys.argv)>=1:
	param =float(sys.argv[1])
rmb = minRmb.HurrySim("rmb",param,port,baudrate)

host = '172.29.151.214'
port = 5800
bufsize = 4096

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
with closing(sock):
	sock.bind((host, port))
	while True:
		rmb.go(sock)
		time.sleep(0.01)
# 終了時の処理
cv2.destroyAllWindows()
x.off()
x.close()
