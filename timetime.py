# -*- coding: utf-8 -*-

import cv2
import time
from RoombaSCI_ogi import RoombaAPI


class AjiAPI(RoombaAPI):

    def robot_start(self):
        robot_speed = 0
        self.speed = robot_speed
        t1 = time.time()
        self.forward()
        robot_time = 0.0

        while True:
            print robot_speed

            t2 = time.time()
            robot_time += t2 - t1
            t1 = t2
            if robot_time > 0.1:
                robot_time = 0.0
                if robot_speed < 500:#max500
                    robot_speed += 5
                    self.forward()
                    self.speed = robot_speed
                if robot_speed >= 500:
                    self.speed = 500
                    break

    def robot_stop(self):
        robot_speed = self.speed

        t1 = time.time()

        robot_time = 0.0

        while True:
            print robot_speed

            t2 = time.time()
            robot_time += t2 - t1
            t1 = t2
            if robot_time > 0.1:
                robot_time = 0.0
                if robot_speed > 0:
                    robot_speed = robot_speed - 10
                    self.speed = robot_speed
                    self.forward()
                if robot_speed == 0:
                    self.stop()
                    break


port = "/dev/cu.usbserial-A2001n4D"
baudrate = 115200
x = AjiAPI(port, baudrate)

x.start()
x.full()

img = cv2.imread("face.png", 0)


while True:
    ########################
    #### キーボードの入力 ####
    ########################
    key = cv2.waitKey(30)
    if key == 27:    # ESC キー: 終了
        break
    if key == 63232:  # 上矢印キー: 前進
        x.robot_start()
    if key == 63233:  # 下矢印キー: 後退
        x.backward()
    if key == 63235:  # 右矢印キー: 右回転
        x.spin_right()
    if key == 63234:  # 左矢印キー: 左回転
        x.spin_left()
    if key == 32:    # スペースキー: 停止
        x.robot_stop()

    # print x.sensors.bumps.left

    if x.sensors.bumps.left == True:
        print u"バンパーに何かあたったよ"
        x.robot_stop()


    ###################
    #### 画像の表示 ####
    ##################
    cv2.imshow('image',img)
# 終了時の処理
cv2.destroyAllWindows()
x.off()
x.close()
