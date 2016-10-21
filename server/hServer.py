import socket

SERVER_IP = '10.1.161.1'
SERVER_PORT = 5501

class hServer:
    def __init__(self,host,port):
        self.server_sock = socket.socket()
        self.server_sock.bind((host, port))
        self.server_sock.listen(1)

    def start(self):
        conn, addr = self.server_sock.accept()
        print "connected by", addr
        conn.send("Hello,world")
        conn.close()

server = hServer(SERVER_IP, SERVER_PORT,R)
server.start()
