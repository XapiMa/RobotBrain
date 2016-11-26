# -*- coding: utf-8 -*-

# import vrep
# import sys
# import cv2
# import random
# import time
# import numpy as np
from roombaSim import *
# タイヤ間の距離23cm

right = -1
left = 1


class HurrySim(RoombaSim):

    def __init__(self):
        super(HurrySim, self).__init__()
        self.colorData = {
            "red":
            {"MAX": [0, 255, 255], "min": [0, 100, 149]},
            "blue":
            {"MAX": [120, 255, 255], "min": [120, 100, 149]}
        }
        self.nowR = 0
        self.nowL = 0
        # self.right = -1
        # self.left = 1
        self.direction = 0
        self.param=160/1000.0#速度mm/sを現実時刻から仮想環境内の時刻に調整するパラメータ．学内Macなら275/1000が妥当．

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
        self.drive_direct(0,0)

    def turn_angle(self, direction, angle):
        # if (direction == "r"):
        #     self.direction = self.right
        # elif(direction == "l"):
        #     self.direction = self.left
        # else:  # 回転方向の指定をミスったら止まる
        #     direction = 0

        limit = 115 * 2 * 3.14159 / (1000*self.param) * angle / 360
        self.drive_direct(-1000 * direction * right, -1000 * direction * left)
        time.sleep(limit)
        # print "回転時間(angle):",limit
        self.quick_stop()

    def turn_around(self, direction, angle, distance):
        limit = (distance + 230) * 2 * 3.14159 / (1000*self.param)

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

        self.drive_direct(1000.0 * rSP, 1000.0 * lSP)
        time.sleep(limit)
        self.quick_stop()

    def turn_color(self, sColor):
        view_center = 255 / 2.0
        x, y, w, h, im = self.detect_col(sColor)
        obj_center = x + w / 2.0  # x,yはobjの左上の値
        if(obj_center == view_center):
            sys.exit(turn_color())
        elif(x <= 0):
            self.turn_angle(right, 30)
            self.turn_color(sColor)
        elif(obj_center > view_center):
            while(obj_center > view_center):
                self.drive_direct(-50, 50)  # 精度が決まる．環境によって異なる？
                time.sleep(0.001)  # 限界の最小時刻は環境依存？
                x, y, w, h, im = self.detect_col(sColor)
                obj_center = x + w / 2.0
                print "a_obj_center:", obj_center
            self.quick_stop()
        else:
            while(obj_center < view_center):
                self.drive_direct(50, -50)
                time.sleep(0.001)
                x, y, w, h, im = self.detect_col(sColor)
                obj_center = x + w / 2.0
                print "b_obj_center:", obj_center
            self.quick_stop()

    def detect_col(self, sColor):

        errorCode, resolution, image = vrep.simxGetVisionSensorImage(
            self.clientID, self.cam_handle, 0, vrep.simx_opmode_streaming)

        if errorCode == 0:
            im = np.array(image, dtype=np.uint8)         # numpy に変換
            im.resize([resolution[0], resolution[1], 3])  # サイズを変換
            im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)     # 色を変換 RGB -> BGR
            im = cv2.flip(im, 0)                      # 上下反転
            #cv2.imshow("image", im)
            ##############################################
            # color detection
            ##############################################
            im_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
            #im_hsv = im
            color_min = np.array(self.colorData[sColor]["min"])
            color_max = np.array(self.colorData[sColor]["MAX"])
            mask_color = cv2.inRange(im_hsv, color_min, color_max)
            contours, hierarcy = cv2.findContours(
                mask_color, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
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

                # print "(x,y)=", x, y
                return x, y, w, h, im
                #cv2.imshow("camera", im)
            else:
                #cv2.imshow("camera", im)
                return -1, -1, -1, -1, im

        else:
            return -2, -2, -2, -2, 0
