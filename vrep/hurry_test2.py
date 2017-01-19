# -*- coding: utf-8 -*-

import hurrySim2
import time
import cv2

rmb = hurrySim2.HurrySim()

cv2.namedWindow("camera")
# 本当はrmb.go()を呼び出すだけで済ませたい．しかし，rmb.go()を実行してもうまくcv2の画面表示ができない．

b1_count = 0
b2_count = 0
while True:

    xa1, xa2, xb1, xb2, im = rmb.line_pos(400, 450, 200, None)
    print xa1, xa2, xb1, xb2

    if im != None:
        cv2.imshow("camera", im)
        cv2.waitKey(10)

    if xb1 == -1:
        b1_count += 1
        if b1_count >= 2:
            print "turn_left_course"
            cv2.waitKey(100)
            rmb.turn_left_course()
            cv2.waitKey(100)
            b1_count = 0
        xa1, xa2, xb1, xb2, im = rmb.line_pos(400, 450, 200, None)
        print xa1, xa2, xb1, xb2
        continue
    elif xb2 == -1:
        b2_count += 1
        if b2_count >= 2:
            print "turn_right_course"
            cv2.waitKey(100)
            rmb.turn_right_course()
            cv2.waitKey(100)
            b2_count = 0
        xa1, xa2, xb1, xb2, im = rmb.line_pos(400, 450, 200, None)
        print xa1, xa2, xb1, xb2
        continue
    elif xa1 < 68 and xa2 < 462:
        print "adjust_right"
        rmb.adjust_right()
        continue
    elif xa1 > 68 and xa2 > 462:
        print "adjust_left"
        rmb.adjust_left()
        continue
    else:
        print "go_straight"
        rmb.drive_direct(rmb.speed, rmb.speed)

    # rmb.go()
    time.sleep(0.01)
