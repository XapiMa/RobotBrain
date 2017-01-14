from __future__ import print_function
import socket
import time
from contextlib import closing
import getch


def main():
    # host = '172.29.151.214'
    host = '127.0.0.1'
    port = 5800
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    with closing(sock):
        while True:
            message = getch.getch()
            print(message)
            if message == 'e':
                break
            sock.sendto(message, (host, port))
        time.sleep(1)
    return

if __name__ == '__main__':
    main()
