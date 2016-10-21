import socket

serverAddr = '10.1.161.1'
serverPort = 5802

client_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_sock.connect((serverAddr, serverPort))

while True:
    clientInput = raw_input('please input > ')
    client_sock.send(clientInput)
    response = client_sock.recv(1024)
    print response

client_sock.close()
