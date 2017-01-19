# -*- coding: utf-8 -*-
import socket
from contextlib import closing
import netCameraAPI as minRmb

# host = '172.29.151.214'
host = '127.0.0.1'
port = 5800

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

with closing(sock):
    sock.bind((host, port))
    sock.setblocking(0)
    rmb = minRmb.HurrySim("rmb", sock)
