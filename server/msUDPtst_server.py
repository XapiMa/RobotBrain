from socket import *
import time
from time import ctime


HOST = '10.1.161.1'
PORT = 6200
BUFSIZ = 1024
ADDR = (HOST, PORT)
addrlist =[]

udpSerSock = socket(AF_INET, SOCK_DGRAM)
udpSerSock.bind(ADDR)

while True:
    print 'waiting for message...'
    data, addr = udpSerSock.recvfrom(BUFSIZ)
    udpSerSock.sendto('[%s] %s' % (ctime(), data), addr)
    if data =='break': break
    print '...received from and returned to:', addr
    if addr not in addrlist:
        addrlist.append(addr)
    if len(addrlist)%1==0:
        for addr in addrlist:
            udpSerSock.sendto('%d client connected' % len(addrlist), addr)
udpSerSock().close()
