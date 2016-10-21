from multiprocessing import Process
import socket
import time
import m_server


PROCESSES = 5
SERVER_IP = '10.1.161.1'
SERVER_PORT = 5600

class mEchoHendler(mRobotServer.SockerStreamHandler):
    def handle(self):
        while True:
            print "connected by" , self._addr
            data = self._sock.recv(1024)
            if not data : break

            self._sock.send(data)

if __name__ =='__main__':
    server = mRobotServer.MultiprocessingSocketStreamServer(SERVER_IP,SERVER_PORT, PROCESSES)
    handler = mEchoHendler(Roomba)
    server.start(handler)
