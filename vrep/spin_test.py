import hurrySim
import time
import cv2

rmb = hurrySim.HurrySim()

cv2.namedWindow("camera")


rmb.drive_direct(-1000.0, 1000.0)

while True:

    # center and size of color(red) and camera image
    x, y, w, h, im = rmb.detect_col("red")
    # maybe wMax is 255

    cv2.imshow("camera", im)
    print x, w
    if w > 40:
        rmb.stop()
        rmb.turn_angle(rmb.right,360)

    time.sleep(0.1)

    if cv2.waitKey(10) > 0:

        break
