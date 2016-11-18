import hurrySim
import time
import cv2

rmb = hurrySim.HurrySim()

cv2.namedWindow("camera")
count =0

rmb.drive_direct(1000.0, 1000.0)

while True:

    # center and size of color(red) and camera image
    x, y, w, h, im = rmb.detect_col("red")
    # maybe wMax is 255

    cv2.imshow("camera", im)
    print x, w
    if w > 40:
        rmb.stop()
        if count ==0:
            x, y, w, h, im = rmb.detect_col("red")
            print x, w
            time.sleep(0.5)
            rmb.turn_angle(rmb.right,90)
            count+=1

    time.sleep(0.1)

    if cv2.waitKey(10) > 0:

        break
