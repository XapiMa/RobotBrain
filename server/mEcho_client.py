import socket

SERVER_IP = '10.1.161.1'
SERVER_PORT = 5600

client_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_sock.connect((SERVER_IP, SERVER_PORT))

while True:
    clientInput = raw_input('please input > ')
    client_sock.send(clientInput)
    response = client_sock.recv(1024)
    print response

client_sock.close()
