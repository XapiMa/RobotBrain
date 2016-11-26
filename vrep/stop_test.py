import hurrySim2
import time
import cv2
##mm
right = -1
left = 1

rmb = hurrySim2.HurrySim()

cv2.namedWindow("camera")
count =0

rmb.drive_direct(505, 500)

while True:

    # center and size of color(red) and camera image
    x, y, w, h, im = rmb.detect_col("red")
    # maybe wMax is 255

    if im!=None:
        cv2.imshow("camera", im)

    print x, w
    if w > 40:
        rmb.slow_stop()
        if count ==0:
            x, y, w, h, im = rmb.detect_col("red")
            print x, w
            time.sleep(0.1)
            rmb.turn_color("red")
            # rmb.turn_angle("r",360)
            rmb.turn_around(right,360,600)
            rmb.turn_color("blue")
            rmb.drive_direct(500,500)
            while True:
                x, y, w, h, im = rmb.detect_col("blue")
                if w > 40:
                    rmb.slow_stop()
                    rmb.turn_around(right,360*2,600)
            count+=1

    time.sleep(0.1)

    if cv2.waitKey(10) > 0:

        break
