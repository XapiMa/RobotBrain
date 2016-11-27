# -*- coding: utf-8 -*-

# import vrep
# import sys
# import cv2
# import random
# import time
# import numpy as np
from roombaSimAPI2 import *
# タイヤ間の距離23cm

RIGHT = -1
LEFT = 1
SPAN = 200


class HurrySim(RoombaSim):

    def __init__(self):
        super(HurrySim, self).__init__()
        self.now_R = 0
        self.now_L = 0
        self.direction = 0
        self.param = 100 / 1000.0  # 速度mm/sを現実時刻から仮想環境内の時刻に調整するパラメータ．学内Macなら275/1000が妥当．
        self.speed = 500

    def step_speed(self, after_R, after_L, span):  # spanに慣性力でPCが落下しない最大加速度((mm/s)/s)/10を入力
        step_R = abs(self.now_R - after_R) / span
        step_L = abs(self.now_L - after_L) / span
        if self.now_R <= after_R:
            HL_R = 1
        else:
            HL_R = -1
        if self.now_L <= after_L:
            HL_L = 1
        else:
            HL_L = -1
        step = step_R
        if step < step_L:
            step = step_L
        for i in range(step):
            if step_R > 0:
                this_R = self.now_R - span * HL_R
            else:
                this_R = after_R
            if step_L > 0:
                this_L = self.now_L - span * HL_L
            else:
                this_L = after_L
            self.drive_direct(this_R, this_L)
            time.sleep(0.1)
            step_R -= 1
            step_L -= 1

    def drive_direct(self, vel_right, vel_left):
        super(HurrySim, self).drive_direct(vel_right, vel_left)
        self.now_R = vel_right
        self.now_L = vel_left

    def slow_stop(self):
        self.step_speed(0, 0, SPAN)

    def quick_stop(self):
        self.drive_direct(0, 0)

    def turn_angle(self, direction, angle):
        if angle < 0:
            direction *= -1
            angle = abs(angle)
        limit = 115 * 2 * 3.14159 / (self.speed * self.param) * angle / 360
        self.drive_direct(-1 * self.speed * direction *
                          RIGHT, -1 * self.speed * direction * LEFT)
        time.sleep(limit)
        # print "回転時間(angle):",limit
        # self.quick_stop()

    def turn(self, direction, angle, distance):
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
        time.sleep(limit)
        # self.quick_stop()

    def turn_around(self, direction, angle, distance):
        if angle < 0:
            direction *= -1
            angle = abs(angle)
        self.turn_angle(-1 * direction, 90)
        self.turn(direction, angle, distance)

    def turn_color(self, sColor):
        view_center = 255 / 2.0
        x, y, w, h, im = self.detect_col(sColor)
        if(x == view_center):
            sys.exit(turn_color())
        elif(x <= 0):
            self.turn_angle(RIGHT, 30)
            self.turn_color(sColor)
        elif(x > view_center):
            while(x > view_center):
                self.drive_direct(-50, 50)  # 精度が決まる．環境によって異なる？
                time.sleep(0.001)  # 限界の最小時刻は環境依存？
                x, y, w, h, im = self.detect_col(sColor)
            # self.quick_stop()
        else:
            while(x < view_center):
                self.drive_direct(50, -50)
                time.sleep(0.001)
                x, y, w, h, im = self.detect_col(sColor)
            # self.quick_stop()

    def go(self):
        cv2.namedWindow("camera")
        while True:

            xa1, xa2, xb1, xb2, im = self.line_pos(400, 450, 200, None)
            print xa1, xa2, xb1, xb2

            if im != None:
                cv2.imshow("camera", im)

            if xb1 == -1:
                self.turn_left_course()
            elif xb2 == -1:
                self.turn_right_course()
            elif xa1 <= 68 and xa2 <= 462:
                self.adjust_left()
            elif xa1 >= 68 and xa2 >= 462:
                self.adjust_right()
            else:
                self.drive_direct(self.speed, self.speed)
            time.sleep(0.01)

    def turn_right_course(self):
        self.turn(RIGHT,90,150)

    def turn_left_course(self):
        self.turn(LEFT,90,150)

    def adjust(self, direction):
        self.drive_direct(self.speed - 2 * RIGHT * direction,
                          self.speed - 2 * LEFT * direction)

    def adjust_right(self):
        self.adjust(RIGHT)

    def adjust_left(self):
        self.adjust(LEFT)
