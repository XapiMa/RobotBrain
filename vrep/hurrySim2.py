# -*- coding: utf-8 -*-

# import vrep
# import sys
# import cv2
# import random
# import time
# import numpy as np
from roombaSimAPI2 import *
# タイヤ間の距離23cm

right = -1
left = 1


class HurrySim(RoombaSim):

    def __init__(self):
        super(HurrySim, self).__init__()
        self.nowR = 0
        self.nowL = 0
        # self.right = -1
        # self.left = 1
        self.direction = 0
        self.param = 160 / 1000.0  # 速度mm/sを現実時刻から仮想環境内の時刻に調整するパラメータ．学内Macなら275/1000が妥当．

    def drive_direct(self, vel_right, vel_left):
        super(HurrySim, self).drive_direct(vel_right, vel_left)
        self.nowR = vel_right
        self.nowL = vel_left

    def slow_stop(self):
        startR = self.nowR
        startL = self.nowL
        for step in range(10):
            self.drive_direct(self.nowR - startR / 10, self.nowL - startL / 10)
            time.sleep(0.1)
        self.quick_stop()

    def quick_stop(self):
        self.drive_direct(0, 0)

    def turn_angle(self, direction, angle):
        # if (direction == "r"):
        #     self.direction = self.right
        # elif(direction == "l"):
        #     self.direction = self.left
        # else:  # 回転方向の指定をミスったら止まる
        #     direction = 0

        limit = 115 * 2 * 3.14159 / (500 * self.param) * angle / 360
        self.drive_direct(-500 * direction * right, -500 * direction * left)
        time.sleep(limit)
        # print "回転時間(angle):",limit
        self.quick_stop()

    def turn_around(self, direction, angle, distance):
        limit = (distance + 230) * 2 * 3.14159 / (1000 * self.param)

        self.turn_angle(-1 * direction, 90)

        inside = distance / (distance + 230.0)
        # print inside
        if(direction == right):
            lSP = 1
            rSP = inside
            # self.turn_angle("l", 90)
        elif(direction == left):
            lSP = inside
            rSP = 1
            # self.turn_angle("r", 90)
        else:
            lSP = 0
            rSP = 0

        self.drive_direct(500.0 * rSP, 500.0 * lSP)
        time.sleep(limit)
        self.quick_stop()

    def turn_color(self, sColor):
        view_center = 255 / 2.0
        x, y, w, h, im = self.detect_col(sColor)
        if(x == view_center):
            sys.exit(turn_color())
        elif(x <= 0):
            self.turn_angle(right, 30)
            self.turn_color(sColor)
        elif(x > view_center):
            while(x > view_center):
                self.drive_direct(-50, 50)  # 精度が決まる．環境によって異なる？
                time.sleep(0.001)  # 限界の最小時刻は環境依存？
                x, y, w, h, im = self.detect_col(sColor)
            self.quick_stop()
        else:
            while(x < view_center):
                self.drive_direct(50, -50)
                time.sleep(0.001)
                x, y, w, h, im = self.detect_col(sColor)
            self.quick_stop()
