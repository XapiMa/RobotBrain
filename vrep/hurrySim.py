# -*- coding: utf-8 -*-

# import vrep
# import sys
# import cv2
# import random
# import time
# import numpy as np
from roombaSim import *
# タイヤ間の距離230mm


class HurrySim(RoombaSim):

    def __init__(self):
        super(HurrySim, self).__init__()
        self.colorData = {
            "red":
            {"MAX": [0, 255, 255], "min": [0, 100, 149]},
            "blue":
            {"MAX": [240, 255, 255], "min": [240, 100, 149]}
        }
        self.nowR = 0
        self.nowL = 0
        self.right = -1
        self.left = 1
        self.direction = 0

    def drive_direct(self, vel_right, vel_left):
        super(HurrySim, self).drive_direct(vel_right, vel_left)
        self.nowR = vel_right
        self.nowL = vel_left

    def stop(self):
        startR = self.nowR
        startL = self.nowL
        for step in range(10):
            self.drive_direct(self.nowR - startR / 10, self.nowL - startL / 10)
            time.sleep(0.1)
        self.drive_direct(0, 0)

    def turn_angle(self, direction, angle):
        if (direction == "r"):
            self.direction = self.right
        elif(direction == "l"):
            self.direction = self.left
        else:  # 回転方向の指定をミスったら止まる
            direction = 0

        param = 275  # 1000という速度をどうにか計算して導出
        # (1000という値をどうにか計算して、paramを錬成
        limit = 115 * 2 * 3.14159 / param * angle / 360
        self.drive_direct(-1000 * self.direction * self.right, -
                          1000 * self.direction * self.left)
        time.sleep(limit)
        self.drive_direct(0, 0)

    def turn_around(self, direction, angle, distance):
        param = 275
        limit = (distance + 230) * 3.14159 / param
        self.turn_angle(-1*direction, 90)

        inside = distance / (distance + 23.0)
        print inside
        if(direction == "r"):
            lSP = 1 
            rSP = inside 
        elif(direction == "l"):
            lSP = inside 
            rSP = 1
        else:
            lSP = 0
            rSP = 0
        print lSP

        self.drive_direct(1000.0 * rSP, 1000.0 * lSP)
        time.sleep(limit)
        self.drive_direct(0, 0)

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
