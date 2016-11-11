import asynchat
import socket


class EchoClient(asynchat.async_chat):
    ac_in_buffer_size = 64
    ac_out_buffer_size = 64

    def __init__(self, host, port, message):
        self.message = message
        self.received_data = []
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        return

    def handle_connect(self):
        # コマンドを送る
        self.push('ECHO %d\n' % len(self.message))
        # データを送る
        self.push_with_producer(EchoProducer(self.message, buffer_size=self.ac_out_buffer_size))
        # データがそのまま送り返されるはずなのでデータ長をターミネイタにセットする
        self.set_terminator(len(self.message))

    def collect_incoming_data(self, data):
        self.received_data.append(data)

    def found_terminator(self):
        received_message = ''.join(self.received_data)
        print received_message

class EchoProducer(asynchat.simple_producer):
    def more(self):
        response = asynchat.simple_producer.more(self)
        return response
