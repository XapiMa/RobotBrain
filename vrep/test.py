# -*- coding: utf-8 -*-

import vrep
import sys
import cv2
import random
import time
import numpy as np

#################################
# preparation for V-REP
#################################

vrep.simxFinish(-1)

clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)

if clientID!=-1:
    print "Connected to remote API server"
else:
    print "Connection failed"
    sys.exit()

###################################
# getting handles
###################################
errorCode, motorR = vrep.simxGetObjectHandle(clientID, "motor_R", vrep.simx_opmode_oneshot_wait)
print errorCode
errorCode, motorL = vrep.simxGetObjectHandle(clientID, "motor_L", vrep.simx_opmode_oneshot_wait)
print errorCode

errorCode, cam_handle = vrep.simxGetObjectHandle(clientID, "Vision_sensor", vrep.simx_opmode_oneshot_wait)


###################################
## while loop
###################################

while True:

    vR = -10.0/180.0*3.1415
    vL = -10.0/180.0*3.1415

    errorCode = vrep.simxSetJointTargetVelocity(clientID, motorR, vR, vrep.simx_opmode_oneshot_wait)
    errorCode = vrep.simxSetJointTargetVelocity(clientID, motorL, vL, vrep.simx_opmode_oneshot_wait)

