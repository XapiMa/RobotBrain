import socket


class sEcho_server:

    def __init__(self, host, port):
        self.server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_sock.bind((host, port))
        self.server_sock.listen(1)

    def start(self):
        conn, addr = self.server_sock.accept()
        while True:
            print "connected by" , addr
            data = conn.recv(1024)
            if not data : break
            conn.send(data)

        conn.close()

server = sEcho_server('10.1.161.1', 5802)
server.start()
