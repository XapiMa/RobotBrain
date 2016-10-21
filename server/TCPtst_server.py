#一つ目の接続が閉じるまで，二つ目の接続を受け付けない

from socket import *
from time import ctime

HOST = '10.1.161.1'   # localhost
PORT = 6000        # choose a random port number
BUFSIZ = 1024        # set buffer size to 1K
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

while True:
    print 'waiting for connection...'
    tcpCliSock, addr = tcpSerSock.accept()
    print '...connected from:', addr

    while True:
        data = tcpCliSock.recv(BUFSIZ)
        if not data:
            break
        tcpCliSock.send('[%s] %s' % (ctime(), data))

    tcpCliSock.close()

tcpSerSock.close()  # never executed
