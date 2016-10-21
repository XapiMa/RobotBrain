from socket import *

HOST = '10.1.161.1'
PORT = 6200
BUFSIZ = 1024
ADDR = (HOST, PORT)

udpCliSock = socket(AF_INET, SOCK_DGRAM)

while True:
    #while (0.1sec)
    #if flag==0:
    data = raw_input('> ')
    #else data = raw_input('')
    if not data:
        break
    udpCliSock.sendto(data, ADDR)
    data, ADDR = udpCliSock.recvfrom(BUFSIZ)

    #
    if data == 'q':break
    #
    if not data:
        break
    print data
    #
    #data , ADDR = udpCliSock.recvfrom(BUFSIZ)



udpCliSock.close()
