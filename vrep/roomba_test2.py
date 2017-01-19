import hurrySim2
import time
import cv2

rmb = hurrySim2.HurrySim()

cv2.namedWindow("camera")


while True:

    rmb.drive_direct(500.0, 500.0)

    #x,y,w,h,im =  rmb.detect_col("red") # center and size of color(red) and camera image

    xa1, xa2, xb1, xb2, im = rmb.line_pos(400, 450, 200, None)
    print xa1, xa2, xb1, xb2

    if im!=None:
        cv2.imshow("camera", im)

    time.sleep(0.1)

    if cv2.waitKey(10) > 0:

        break
