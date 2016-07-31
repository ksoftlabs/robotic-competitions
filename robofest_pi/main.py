import cv2
import test

cam = cv2.VideoCapture(0)       # Capture the feed from camera

test.movement_test()

while True:
    ret, frame = cam.read()

    cv2.imshow('Feed', frame)

    if cv2.waitKey(1) % 256 == 27:
        break
