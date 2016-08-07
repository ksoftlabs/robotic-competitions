import cv2
import numpy as np
import cmn
from AndroidCamFeed import AndroidCamFeed
import box_detection as bd
## for onboard cam ##
cam = cv2.VideoCapture(0)

## for android cam ##
#cam = AndroidCamFeed('192.168.1.6:8080')#it's not working I don't know why


#color ranges to be adjusted
lower_red_range = (np.array([0, 50, 50]), np.array([10, 255, 255]))
upper_red_range = (np.array([170, 50, 50]), np.array([180, 255, 255]))
blue_range = (np.array([80, 50, 50]), np.array([160, 255, 255]))
green_range = (np.array([160, 50, 50]) , np.array([260, 255, 255]))

while True:
    ret, frame = cam.read()
    cv2.imshow("feed", frame)

    arrows, rectangles = cmn.find_objects(frame, [blue_range], "Blue")# (frame, color_range, window_name) returns an arrow list and a rectangle list see last 2 fuction in cmn.py for more details
    #contours = cmn.find_objects(frame, green_range, "Green")
    #contours = cmn.find_objects(frame, upper_red_range, "Red Upper")
    #contours = cmn.find_objects(frame, lower_red_range, "Red lower")

    bd.detect_box(frame,20,30,40,50)#sonar right,left,top,bottom in pixel values
    if cv2.waitKey(1) % 256 == 27:
        break
