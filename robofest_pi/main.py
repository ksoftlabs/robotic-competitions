import cv2
import box_logic
import communicate
import maze_logic
import movement
import path_logic
import physics

import numpy as np
import time
import psutil

comm = communicate.Port()                   # Raspberry pi - Arduino serial communication interface
robot = physics.Robot(comm)                 # Define current robot state
pid = movement.PID(robot)                   # Adjust course through pid
control = movement.Control(robot, comm)     # Robot movement controls

maze = maze_logic.Maze(robot)               # Maze logic
box = box_logic.Box(robot)                  # Box logic
path = path_logic.Path(robot)               # Path logic

#################################################################################################################
# Testing area
while True:
    robot.see()
    start = time.time()

    frame_hsv = cv2.cvtColor(robot.current_frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    lower_mask = cv2.inRange(frame_hsv, lower_red, upper_red)

    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    upper_mask = cv2.inRange(frame_hsv, lower_red, upper_red)

    img_mask = lower_mask + upper_mask

    robot.processed_frame = cv2.bitwise_and(robot.current_frame, robot.current_frame, mask=img_mask)

    end = time.time()
    diff = end - start
    if diff == 0:
        diff = 10000

    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    cv2.putText(robot.current_frame, 'FPS ' + str(1.0 / diff), (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8,
                (255, 0, 0))
    cv2.putText(robot.current_frame, 'CPU usage ' + str(cpu), (10, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8,
                (255, 0, 0))
    cv2.putText(robot.current_frame, 'Memory usage ' + str(mem), (10, 70), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8,
                (255, 0, 0))
    cv2.putText(robot.processed_frame, 'FPS ' + str(1.0 / diff), (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8,
                (255, 0, 0))
    cv2.putText(robot.processed_frame, 'CPU usage ' + str(cpu), (10, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8,
                (255, 0, 0))
    cv2.putText(robot.processed_frame, 'Memory usage ' + str(mem), (10, 70), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8,
                (255, 0, 0))

    cv2.imshow('Feed', robot.current_frame)
    cv2.imshow('Processed feed', robot.processed_frame)

    if cv2.waitKey(1) % 256 == 27:
        break
exit(0)
##################################################################################################################

while True:
    robot.see()

    if robot.state == 'maze':
        robot.update_sonar_data()

        if box.is_box_seen():
            if box.is_box_totally_visible():
                robot.state = 'box_lift'
            elif box.is_box_partially_visible():
                #####################
                # Adjust the course #
                #####################
                pass
        elif maze.is_on_junction():
            if maze.is_left_open():
                control.turn_left()
            elif maze.is_front_open():
                control.forward(t=0.5)
            elif maze.is_right_open():
                control.turn_right()
        elif maze.is_on_end():
            control.turn_back()
        else:
            control.stop()  # Logic error

    elif robot.state == 'box_lift':
        ######################################
        # Position the robot to lift the box #
        ######################################
        control.lift_the_box()
    elif robot.state == 'path':
        #######################################################
        # Process the frame to create a path from arrow heads #
        #######################################################
        pid.run_pid(robot.processed_frame)
        control.drive()
    elif robot.state == 'box_place':
        #######################################
        # Position the robot to place the box #
        #######################################
        control.place_the_box()
    else:       # state == 'stop' or unknown state
        control.stop()

    cv2.imshow('Feed', robot.current_frame)
    cv2.imshow('Processed feed', robot.processed_frame)

    if cv2.waitKey(1) % 256 == 27:
        break


