import cv2
import numpy as np
import box
import test
import path

cam = cv2.VideoCapture(0)       # Capture the feed from camera

while True:
    ret, frame = cam.read()
    return_frame = np.zeros(frame.shape, np.uint8)
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)





<<<<<<< HEAD

=======
    #box.detect_box(frame, return_frame)
    path.detect_arrow(frame, return_frame, (np.array([40,100,100]), np.array([255,255,255])))
>>>>>>> e43c476a294038921b254f3e08b552b491579aaf







    cv2.imshow('Feed', frame)
    #cv2.imshow('Processed feed', return_frame)

    if cv2.waitKey(1) % 256 == 27:
        break
