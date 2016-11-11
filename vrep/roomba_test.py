import roombaSim
import time
import cv2

rmb = roombaSim.RoombaSim()

cv2.namedWindow("camera")


while True:

    rmb.drive_direct(1000.0, 1000.0)

    x,y,w,h,im =  rmb.detect_col("red") # center and size of color(red) and camera image

    cv2.imshow("camera", im)
    print x,w
    
    time.sleep(0.1)

    if cv2.waitKey(10) > 0:

        break
