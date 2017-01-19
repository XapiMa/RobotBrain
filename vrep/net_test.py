# -*- coding: utf-8 -*-
import sys
import time
import socket
from contextlib import closing
# コマンドライン引数でパラメータを指定して実行する

# host = '172.29.151.214'
host = '127.0.0.1'
port = 5800
bufsize = 4096

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
with closing(sock):
	sock.bind((host, port))
	sock.setblocking(0)
	count = 1
	while True:
		try:
			key = sock.recv(bufsize)
			print key
			if key=='q':
				sys.exit()
			if key == 'a':
				print 'go_left'
			elif key == 'd':
				print 'go_right'
			elif key == 'w':
				print 'go_straight'
			elif key == 's':
				print 'pause'
		except socket.error:
			# print "no Massage"
			pass
		print count
		count +=1
		time.sleep(1)
