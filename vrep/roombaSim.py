# -*- coding: utf-8 -*-

import vrep
import sys
import cv2
import random
import time
import numpy as np


class RoombaSim(object):

    def __init__(self):
        #################################
        # preparation for V-REP
        #################################
        self.colorData = {
            "red":
            {"MAX": [0, 255, 255], "min": [0, 100, 149]},
            "blue":
            {"MAX": [240, 255, 255], "min": [240, 100, 149]}
        }

        vrep.simxFinish(-1)

        self.clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

        if self.clientID != -1:
            print "Connected to remote API server"
        else:
            print "Connection failed"
            sys.exit()

        ###################################
        # getting handles
        ###################################

        errorCode, self.motorR = vrep.simxGetObjectHandle(
            self.clientID, "motor_R", vrep.simx_opmode_oneshot_wait)
        # print errorCode
        errorCode, self.motorL = vrep.simxGetObjectHandle(
            self.clientID, "motor_L", vrep.simx_opmode_oneshot_wait)
        # print errorCode

        errorCode, self.cam_handle = vrep.simxGetObjectHandle(
            self.clientID, "Vision_sensor", vrep.simx_opmode_oneshot_wait)

    def drive_direct(self, vel_right, vel_left):

        radius = 35.0  # [mm]
        # [mm/sec] -> [rad/sec]
        vR = -vel_right / (2.0 * 3.14159 * radius)
        vL = -vel_left / (2.0 * 3.14159 * radius)

        errorCode = vrep.simxSetJointTargetVelocity(
            self.clientID, self.motorR, vR, vrep.simx_opmode_oneshot_wait)
        errorCode = vrep.simxSetJointTargetVelocity(
            self.clientID, self.motorL, vL, vrep.simx_opmode_oneshot_wait)

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
