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

    def __init__(self, name, param):
        super(HurrySim, self).__init__()
        self.now_R = 0
        self.now_L = 0
        self.direction = 0
        self.param = param / 1000.0  # 速度mm/sを現実時刻から仮想環境内の時刻に調整するパラメータ．学内Macなら275/1000が妥当．
        self.speed = 500
        self.im = None
        self.name = name
        self.im_h = 0
        self.im_w = 0
        cv2.namedWindow(self.name)
        self.recognize_line()

    def show_im(self):
        cv2.imshow(self.name, self.im)
        cv2.waitKey(1)

    def recognize_line(self):
        xa1, xa2, xb1, xb2 = self.line_pos(200, 300, 200, None)
        print xa1, xa2, xb1, xb2
        return xa1, xa2, xb1, xb2

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
        for i in range(10):
            self.recognize_line()
            time.sleep(limit / 11.0)
        # self.quick_stop()

    def turn_around(self, direction, angle, distance):
        if angle < 0:
            direction *= -1
            angle = abs(angle)
        self.turn_angle(-1 * direction, 90)
        self.turn(direction, angle, distance)

    def turn_color(self, sColor):
        view_center = 255 / 2.0
        x, y, w, h = self.detect_col(sColor)
        if(x == view_center):
            sys.exit(turn_color())
        elif(x <= 0):
            self.turn_angle(RIGHT, 30)
            self.turn_color(sColor)
        elif(x > view_center):
            while(x > view_center):
                self.drive_direct(-50, 50)  # 精度が決まる．環境によって異なる？
                time.sleep(0.001)  # 限界の最小時刻は環境依存？
                x, y, w, h = self.detect_col(sColor)
            # self.quick_stop()
        else:
            while(x < view_center):
                self.drive_direct(50, -50)
                time.sleep(0.001)
                x, y, w, h = self.detect_col(sColor)
            # self.quick_stop()

    def go(self):
        while True:
            xa1, xa2, xb1, xb2 = self.recognize_line()
            self.front(xb1, xb2)
            self.turn_corner(xa1, xa2)
            # if xb1 == -1:
            #     print "turn_left_course"
            #     time.sleep(2)
            #     self.turn_left_course()
            #     time.sleep(0.1)
            #     b1_count = 0
            #     self.recognize_line()
            # elif xb2 == -1:
            #     print "turn_right_course"
            #     time.sleep(2)
            #     self.turn_right_course()
            #     time.sleep(0.1)
            #     b2_count = 0
            #     self.recognize_line()
            # elif xa1 < 97 and xa2 < 430:
            #     print "adjust_right"
            #     self.adjust_right()
            # elif xa1 > 97 and xa2 > 430:
            #     print "adjust_left"
            #     self.adjust_left()
            # else:
            #     print "go_straight"
            #     self.drive_direct(self.speed, self.speed)
            time.sleep(0.01)

    def turn_right_course(self):
        self.turn(RIGHT, 85, 100)

    def turn_left_course(self):
        self.turn(LEFT, 85, 100)

    def adjust(self, direction):
        self.drive_direct(self.speed - 30 - 30 * RIGHT * direction,
                          self.speed - 30 - 30 * LEFT * direction)

    def front(self, xb1, xb2):
        # 手前の線で直進を判断
        if (xb1 < self.im_w - xb2):
            # if xb1 > 96 or xb2 > 429:
            print "adjust_left"
            self.adjust(LEFT)
        elif (xb1 > self.im_w - xb2):
            # elif xb1 < 96 or xb2 < 492:
            print "adjust_right"
            self.adjust(RIGHT)
        else:
            print "go_straight"
            self.drive_direct(self.speed, self.speed)

    def turn_corner(self, xa1, xa2):
        if self.line_w():
            if xa1 < 0:
                # 左に曲がる
                self.turn_left_course()
            elif xa2 < 0:
                # 右に曲がる
                self.turn_right_course()

    def line_w(self):
        # 曲がると判断する位置に横線があればTrueを、なければFalseを返す
        return True

    def line_pos(self, ya, yb, thd, im=None):
        errorCode, resolution, image = vrep.simxGetVisionSensorImage(
            self.clientID, self.cam_handle, 0, vrep.simx_opmode_streaming)

        if errorCode == 0:
            im = np.array(image, dtype=np.uint8)         # numpy に変換
            im.resize([resolution[0], resolution[1], 3])  # サイズを変換
            im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)     # 色を変換 RGB -> BGR
            im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
            im = cv2.flip(im, 0)
            image = im.copy()
            yoko_a = image[ya, :]
            yoko_b = image[yb, :]

            xmax = image.shape[1]
            xmid = xmax / 2
            # print xmax, xmid

            if np.max(yoko_a[0:xmid]) < thd:
                xa1 = -1
            else:
                xa1 = np.argmax(yoko_a[0:xmid])

            if np.max(yoko_a[xmid:xmax]) < thd:
                xa2 = -1
            else:
                xa2 = np.argmax(yoko_a[xmid:xmax]) + xmid

            if np.max(yoko_b[0:xmid]) < thd:
                xb1 = -1
            else:
                xb1 = np.argmax(yoko_b[0:xmid])

            if np.max(yoko_b[xmid:xmax]) < thd:
                xb2 = -1
            else:
                xb2 = np.argmax(yoko_b[xmid:xmax]) + xmid

            # draw line
            cv2.line(image, (0, ya), (xmax, ya), 100, 2)
            cv2.line(image, (0, yb), (xmax, yb), 100, 2)

            if xa1 != -1:
                cv2.circle(image, (xa1, ya), 10, 100, -1)
            if xa2 != -1:
                cv2.circle(image, (xa2, ya), 10, 100, -1)
            if xb1 != -1:
                cv2.circle(image, (xb1, yb), 10, 100, -1)
            if xb2 != -1:
                cv2.circle(image, (xb2, yb), 10, 100, -1)
            self.im_h = image.shape[0]
            self.im_w = image.shape[1]
            self.im = image
            self.show_im()

            return xa1, xa2, xb1, xb2

        else:
            return -2, -2, -2, -2


def detect_col(self, col):
    errorCode, resolution, image = vrep.simxGetVisionSensorImage(
        self.clientID, self.cam_handle, 0, vrep.simx_opmode_streaming)

    if errorCode == 0:
        im = np.array(image, dtype=np.uint8)         # numpy に変換
        im.resize([resolution[0], resolution[1], 3])  # サイズを変換
        im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)     # 色を変換 RGB -> BGR
        im = cv2.flip(im, 0)
        ##############################################
        # color detection
        ##############################################
        im_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        if col == "red":
            col_min = np.array([0, 100, 149])
            col_max = np.array([0, 255, 255])
        elif col == "blue":
            col_min = np.array([120, 100, 149])
            col_max = np.array([120, 255, 255])
        # if col == "red":
        #     col_min = np.array([0, 10, 0])
        #     col_max = np.array([20, 255, 255])
        # elif col == "blue":
        #     col_min = np.array([110, 10, 0])
        #     col_max = np.array([130, 255, 255])

        mask_col = cv2.inRange(im_hsv, col_min, col_max)
        contours, hierarcy = cv2.findContours(
            mask_col, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        max_area = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > max_area:
                max_area = area
                best_cnt = cnt
                x, y = -1, -1
                w, h = 0, 0
        if max_area != 0:
            x, y, w, h = cv2.boundingRect(best_cnt)
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # cv2.imshow("camera", im)
            # print "(x,y)=", x, y
            self.im = im
            self.show_im()
            return x + w / 2, y + h / 2, w, h
        else:
            return -1, -1, -1, -1

    else:
        return -1, -1, -1, -1
