import cv2
import maze
import box
import path
import control

cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()

    cv2.imshow('Feed', frame)

    if cv2.waitKey(1) == 27:
        break
