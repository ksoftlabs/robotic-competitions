import cv2
import numpy as np
import movement
import communicate
import maze
import box
import path
import test

cam = cv2.VideoCapture(0)       # Capture the feed from camera

robot = movement.Robot()
pid = movement.PID(robot)
control = movement.Control(robot)
comm = communicate.Port()

while True:
    ret, frame = cam.read()
    return_frame = np.zeros(frame.shape, np.uint8)

    front_sonar = comm.get_front_distance()
    left_sonar = comm.get_left_distance()
    right_sonar = comm.get_right_distance()
    back_sonar = comm.get_back_direction()


    # box.detect_box(frame, return_frame)




    cv2.imshow('Feed', frame)
    cv2.imshow('Processed feed', return_frame)

    if cv2.waitKey(1) % 256 == 27:
        break
