import socket

SERVER_IP = '10.1.161.1'
SERVER_PORT = 5501


client_sock = socket.socket()
client_sock.connect((SERVER_IP, SERVER_PORT))
client_sock.send("hello")
data = client_sock.recv(1024)
print data
client_sock.close()
