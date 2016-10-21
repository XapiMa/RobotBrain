# coding: utf-8

import asyncore
import socket

class EchoHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)
        if data:
            self.send(data)

class EchoClient(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.buffer = 'echo_tst'


    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        print 'return:' + self.recv(8192)
        self.handle_close()
        # やり取り一回分の入力データ（初期値）しか持たないので，消化後に，通信を終了する

    def writable(self):
        return bool(self.buffer)

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]

client = EchoClient('10.1.161.1', 5610)
asyncore.loop()
