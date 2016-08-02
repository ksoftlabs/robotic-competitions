import cv2
import numpy as np
import logic
import physics
import movement
import communicate
import maze
import box
import path
import test

cam = cv2.VideoCapture(0)       # Capture the feed from camera

comm = communicate.Port()
robot = physics.Robot(comm)
pid = movement.PID(robot)
control = movement.Control(robot)


decision = logic.Decision(robot)

while True:
    ret, frame = cam.read()
    return_frame = np.zeros(frame.shape, np.uint8)

    robot.update_sonar_data()


    cv2.imshow('Feed', frame)
    cv2.imshow('Processed feed', return_frame)

    if cv2.waitKey(1) % 256 == 27:
        break

    #
    #
    #
    #
    #
    # All the testing code go after this #########################################################################

    box.detect_box(frame, return_frame)


