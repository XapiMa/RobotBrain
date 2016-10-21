from multiprocessing import Process
import socket
import time

PROCESSES = 5
SERVER_IP = '10.1.161.1'
SERVER_PORT = 5600

class MultiprocessingSocketStreamServer(object):

    def __init__(self, host, port,processes):
        self._server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._server_sock.bind((host, port))
        self._server_sock.listen(processes)
        self.processes = processes


    def start(self,handler):
        for num in range(self.processes):
            p = Process(target =handler,args=(self._server_sock,))
            p.daemon=True
            p.start()
        self._parent_main_loop()

    def _parent_main_loop(self):
        while True:
            time.sleep(1)

class SockerStreamHandler(object):

    def __init__(self):
        self._sock=None
        self._address = None

    def __call__(self,server_sock):
        while True:
            (self._sock,self._addr)=server_sock.accept()
            with self:
                self.handle()

    def __enter__(self):
        pass

    def __exit__(self,exc_type,exc_value,traceback):
        self._sock.shutdown(socket.SHUT_RDWR)
        self._sock.close()

    def handle(self):
        raise NotImplementedError

class HelloWorldHendler(SockerStreamHandler):
    def handle(self):
        while True:
            print "connected by" , self._addr
            data = self._sock.recv(1024)
            if not data : break
            self._sock.send(data)

if __name__ =='__main__':
    server = MultiprocessingSocketStreamServer(SERVER_IP,SERVER_PORT, PROCESSES)
    handler = HelloWorldHendler()
    server.start(handler)
