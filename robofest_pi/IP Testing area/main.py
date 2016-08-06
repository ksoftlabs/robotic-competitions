import cv2
import numpy as np
import cmn
import AndroidCamFeed
## for onboard cam ##
cam = cv2.VideoCapture(0)

## for android cam ##
# cam = AndroidCamFeed('192.168.1.6:8080')


while True:
    ret, frame = cam.read()
    cv2.imshow("feed", frame)


    lower_red_range = (np.array([0, 50, 50]), np.array([10, 255, 255]))

    upper_red_range = (np.array([170, 50, 50]), np.array([180, 255, 255]))

    blue_range = (np.array([80, 50, 50]), np.array([160, 255, 255]))

    green_range = (np.array([160, 50, 50]) , np.array([260, 255, 255]))


    #for testing
    cmn.find_objects(frame, blue_range, "Blue")# frame, color range, window_name
    cmn.find_objects(frame, green_range, "Green")
    cmn.find_objects(frame, upper_red_range, "Red Upper")
    cmn.find_objects(frame, lower_red_range, "Red lower")

    if cv2.waitKey(1) % 256 == 27:
        break
