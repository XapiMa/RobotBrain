from multiprocessing import Process
import socket
import time
import m_server

PROCESSES = 5
SERVER_IP = '10.1.161.1'
SERVER_PORT = 5600




class mEchoHendler(m_server.SockerStreamHandler):
    def handle(self):

        # ルンバの接続の初期化
        port = "/dev/cu.usbserial-A2001n4D" #ここは各自で違う！
        baudrate = 115200

        x = RoombaAPI(port, baudrate)

        x.start()   # 前回から若干修正！
        x.full()

        while True:
            print "connected by" , self._addr
            data = self._sock.recv(1024)
            key = data

            ########################
            #### キーボードの入力 ####
            ########################
            if key == 'q':    # ESC キー: 終了
                break
            if key == 'k': # 上矢印キー: 前進
                x.backward()
            if key == 'j': # 下矢印キー: 後退
                x.forward()
            if key == 'l': # 右矢印キー: 右回転
                x.spin_right()
            if key == 'h': # 左矢印キー: 左回転
                x.spin_left()
            if key == 'z':    # スペースキー: 停止
                x.stop()

            ###################
            #### 画像の表示 ####
            ##################
            #cv2.imshow('image',img)

            if not data : break

            self._sock.send(data)

        # 終了時の処理
        cv2.destroyAllWindows()
        x.off()
        x.close()


if __name__ =='__main__':

    server = m_server.MultiprocessingSocketStreamServer(SERVER_IP,SERVER_PORT, PROCESSES)
    handler = mEchoHendler()
    server.start(handler)
