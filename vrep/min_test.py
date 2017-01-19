# -*- coding: utf-8 -*-
import cv2
import sys
import socket
from contextlib import closing
import minRmb
# コマンドライン引数でパラメータを指定して実行する
# 学校のMac環境なら275が妥当。回転しすぎるなら大きく、回転不足なら小さくする

r_port = "/dev/cu.usbserial-A2001mJ7" #ここは各自で違う！
#1r_port ="/dev/cu.usbserial-A2001mXk"
#
r_baudrate = 115200

param =1000
if len(sys.argv)>=2:
	param =float(sys.argv[1])

n_host = '172.29.165.193'
# n_host = '127.0.0.1'
n_port = 5800
# bufsize = 4096

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

with closing(sock):
	sock.bind((n_host, n_port))
	sock.setblocking(0)
	rmb = minRmb.HurryAPI("rmb",param,r_port,r_baudrate,sock)

# 終了時の処理
cv2.destroyAllWindows()
rmb.off()
rmb.close()
