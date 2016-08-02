import cv2
import numpy as np
import box
import test
import path

cam = cv2.VideoCapture(0)       # Capture the feed from camera

while True:
    ret, frame = cam.read()
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return_frame = np.zeros(frame.shape, np.uint8)








    box.detect_box(frame, return_frame)







    cv2.imshow('Feed', frame)
    #cv2.imshow('Processed feed', return_frame)

    if cv2.waitKey(1) % 256 == 27:
        break
