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
        if vel_right > 500.0:
            vel_right = 500.0
        if vel_right < -500.0:
            vel_right = -500.0
        if vel_left > 500.0:
            vel_left = 500.0
        if vel_left < -500.0:
            vel_left = -500.0

        radius = 35.0  # [mm]
        # [mm/sec] -> [rad/sec]
        vR = -vel_right / (2.0 * 3.14159 * radius)
        vL = -vel_left / (2.0 * 3.14159 * radius)

        errorCode = vrep.simxSetJointTargetVelocity(
            self.clientID, self.motorR, vR, vrep.simx_opmode_oneshot_wait)
        errorCode = vrep.simxSetJointTargetVelocity(
            self.clientID, self.motorL, vL, vrep.simx_opmode_oneshot_wait)

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
                return x + w / 2, y + h / 2, w, h, im
            else:
                return -1, -1, -1, -1, None

        else:
            return -1, -1, -1, -1, None

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

            #cv2.imshow("image", image)

            return xa1, xa2, xb1, xb2, image

        else:
            return -2, -2, -2, -2, None
