# -*- coding: utf-8 -*-
import sys
import minSim
import time
import cv2

param =float(sys.argv[1])
rmb = minSim.HurrySim("rmb",param)


b1_count = 0
b2_count = 0
while True:
    rmb.go()
    time.sleep(0.01)
