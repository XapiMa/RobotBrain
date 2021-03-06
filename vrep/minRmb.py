# -*- coding: utf-8 -*-
import pandas as pd
from sklearn import tree
import sys
import random
import time
import numpy as np
import socket
from contextlib import closing
import cv2
from RoombaSCI_ogi import RoombaAPI
# タイヤ間の距離23cm

# 時間での管理を諦め、画像での管理に専念したい

RIGHT = -1
LEFT = 1
SPAN = 200


class HurryAPI(RoombaAPI):

    def __init__(self, name, param, r_port, r_baudrate, sock):
        super(HurryAPI, self).__init__(r_port, 115200)
        self.start()
        self.full()
        # 学習時にはTrue 評価時にはFalse
        # self.learnFlag = True
        self.learnFlag = False

        print self.port
        self.now_R = 0
        self.now_L = 0
        self.direction = 0
        self.param = param / 1000.0  # 速度mm/sを現実時刻から仮想環境内の時刻に調整するパラメータ．学内Macなら275/1000が妥当．
        self.speed = 500
        self.im = None
        self.im_h = 0
        self.im_w = 0
        self.name = name
        self.cap = cv2.VideoCapture(1)
        self.cap.set(3, 640)  # カメラの横のサイズ
        self.cap.set(4, 480)  # カメラの縦のサイズ
        self.clf = tree.DecisionTreeClassifier(max_depth=6)
        if self.learnFlag:
            self.f_obj = open("data9.txt","a")
            #print >> self.f_obj,"status,xa1,xa2,xb1,xb2,xc1,xc2,xd1,xd2"

        cv2.namedWindow(self.name)
        if not self.learnFlag:
            self.dataanalysis()
        self.sock = sock
        self.go()

    def go(self):
        now_status = "pause"
        bufsize = 4096
        flag = True
        while True:
            # xas = self.recognize_line()
            xas = self.line_pos((100,200,300,400,320+100,320-100), 190, None)
            # self.turn_corner(xa1, xa2)
            time.sleep(0.01)
            # 画面描画
            key = cv2.waitKey(1)
            # cv2.imshow('image',self.wimg)

            if not self.learnFlag:
                print xas
                # txa = xas[2:8]
                # txa.append(xas[10])
                # txa.append(xas[11])
                textkey = self.clf.predict(xas)
                if textkey == "left":
                    key = 'a'
                elif textkey == "right":
                    key = 'd'
                elif textkey == "straight":
                    key = 'w'
            try:
                key = self.sock.recv(bufsize)
            except socket.error:
                pass

            if key == 'a':
                print "goleft"
                now_status = "left"
                self.turn_corner(LEFT)
            elif key == 'd':
                self.turn_corner(RIGHT)
                now_status = "right"
            elif key == 'w':
                print "gostraight"
                now_status = "straight"
                self.drive_direct(self.speed, self.speed)
            # elif key == 'c':
            #     print "speed up"
            #     now_status = "speedup"
            #     self.speed_up()
            # elif key == 'z':
            #     print "speed down"
            #     now_status = "speeddown"
            #     self.speed_down()
                # self.front(xb1, xb2)
            elif key == 's':
                print 'pause'
                self.drive_direct(0,0)
                now_status = "pause"
            elif key == 'j':
                print 'bye'
                self.drive_direct(0,0)
                sys.exit()
            if self.learnFlag:
                s_xas = map(str,xas)
                print >> self.f_obj,now_status+","+",".join(s_xas)
                #print >> self.f_obj,now_status+","+str(xas[0])+","+str(xas[1])+","+str(xas[2])+","+str(xas[3])+","+str(xas[4])+","+str(xas[5])+","+str(xas[6])+","+str(xas[7])
                #print >> self.f_obj,now_status+","+str(xas[0])+","+str(xas[1])+","+str(xas[2])+","+str(xas[3])+","+str(xas[4])

    def speed_up(self):
        add_speed = SPAN
        max_speed = self.now_R
        if max_speed < self.now_L:
            max_speed = self.now_L
        if max_speed + add_speed > 500:
            add_speed = 500 - max_speed
        self.drive_direct(self.now_R + add_speed, self.now_L + add_speed)
        time.sleep(0.3)

    def speed_down(self):
        reduce_speed = SPAN
        min_speed = self.now_R
        if min_speed > self.now_L:
            min_speed = self.now_L
        if min_speed - reduce_speed < 0:
            reduce_speed = min_speed
        self.drive_direct(self.now_R - reduce_speed, self.now_L - reduce_speed)
        time.sleep(0.3)

    def adjust(self, direction):
        self.drive_direct(self.speed - 30 - 30 * RIGHT * direction,
                          self.speed - 30 - 30 * LEFT * direction)

    def turn_corner(self, direction):
        # 仮に、ルンバから横に100mmの位置を中心として85度回転するように設定した
        self.turn(direction, 10, 50)

    def turn(self, direction, angle, distance):
        # distanceは内側のタイヤと回転の中心との距離
        if angle < 0:
            direction *= -1
            angle = abs(angle)
        limit = (distance + 230) * 2 * 3.14159 / \
            (self.speed * self.param) * angle / 360

        inside = distance / (distance + 230.0)
        if(direction == RIGHT):
            lSP = 1
            rSP = inside
        elif(direction == LEFT):
            lSP = inside
            rSP = 1
        else:
            lSP = 0
            rSP = 0
        self.drive_direct(self.speed * rSP, self.speed * lSP)

    def line_w(self):
        # 曲がると判断する位置に横線があればTrueを、なければFalseを返す
        return True

    def line_pos(self, ya,  thd, im=None):
        errorCode, image = self.cap.read()
        # errorCode, resolution, image = vrep.simxGetVisionSensorImage(
        #     self.clientID, self.cam_handle, 0, vrep.simx_opmode_streaming)
        yoko = [None,None,None,None,None,None,None,None]
        tate = [None,None,None,None]
        xas = [i for i in range(12)]
        if errorCode == True:
            im = np.array(image, dtype=np.uint8)         # numpy に変換
            # im.resize([resolution[0], resolution[1], 3])  # サイズを変換
            im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)     # 色を変換 RGB -> BGR
            im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
            image = im.copy()
            for i in range(4):
                yoko[i] = image[ya[i], :]
            xmax = image.shape[1]
            xmid = xmax / 2


            for i in range(4):
                if np.max(yoko[i][0:xmid]) < thd:
                    xas[i*2] = -1
                else:
                    xas[i*2] = np.argmax(yoko[i][0:xmid])

                if np.max(yoko[i][xmid:xmax]) < thd:
                    xas[i*2+1] = 641
                    # xa2 = -1
                else:
                    xas[i*2+1] = np.argmax(yoko[i][xmid:xmax]) + xmid


            # draw line
            for i in range(4):

                cv2.line(image, (0, ya[i]), (xmax, ya[i]), 100, 2)

                if xas[i*2] != -1:
                    cv2.circle(image, (xas[i*2], ya[i]), 10, 100, -1)
                if xas[i*2+1] != 641:
                    cv2.circle(image, (xas[i*2+1], ya[i]), 10, 100, -1)
            if len(ya)>4:
                for j in range(2):
                    i = j+4
                    yoko[i] = image[:,ya[i]]
                ymax = image.shape[0]
                ymid = ymax/2
                for j in range(2):
                    i = j+4
                    if np.max(yoko[i][0:ymid]) < thd:
                        xas[i*2] = -1
                    else:
                        xas[i*2] = np.argmax(yoko[i][0:ymid])

                    if np.max(yoko[i][ymid:ymax]) < thd:
                        xas[i*2+1] = 481
                        # xa2 = -1
                    else:
                        xas[i*2+1] = np.argmax(yoko[i][ymid:ymax]) + ymid


                # draw line
                for j in range(2):
                    i = j+4
                    cv2.line(image, (ya[i], 0), (ya[i],ymax), 100, 2)

                    if xas[i*2] != -1:
                        cv2.circle(image, (ya[i],xas[i*2]), 10, 100, -1)
                    if xas[i*2+1] != 641:
                        cv2.circle(image, (ya[i],xas[i*2+1]), 10, 100, -1)
            self.im_h = image.shape[0]
            self.im_w = image.shape[1]
            self.im = image
            #self.show_im()
            cv2.imshow(self.name,self.im)

            return xas

        else:
            return -2, -2, -2, -2


    def drive_direct(self, vel_right, vel_left):
        # 指定した速度で走る
        print type(vel_right),vel_right,type(vel_left),vel_left
        super(HurryAPI, self).drive_direct(int(vel_right), int(vel_left))
        # 現在の速度でnow_Rとnow_Lを更新する
        self.now_R = vel_right
        self.now_L = vel_left
        # 最大速度±500なので、それに調整するための分岐処理
        if(vel_right > 500):
            self.now_R = 500
        elif(vel_right < -500):
            self.now_R = -500
        if(vel_left > 500):
            self.now_L = 500
        elif(vel_left < -500):
            self.now_L = -500

    def dataanalysis(self):
        dataset = pd.read_csv("data9.txt")
        # dataset = dataset.drop_duplicates()
        data = dataset[["xa1","xa2","xb1", "xb2","xc1","xc2","xd1","xd2","ya1","ya2","yb1","yb2"]]
        target = dataset["status"]
        target.value_counts()
        self.clf = tree.DecisionTreeClassifier(max_depth=6)
        self.clf = self.clf.fit(data, target)
