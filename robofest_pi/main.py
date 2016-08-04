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


comm = communicate.Port()                   # Raspberry pi - Arduino serial communication interface
robot = physics.Robot(comm)
pid = movement.PID(robot)
control = movement.Control(robot, comm)
decision = logic.Decision(robot)

while True:
    robot.see()

    if decision.state == 'maze':
        robot.update_sonar_data()

        if decision.is_box_seen():
            # Adjust robot
            pass
        elif decision.is_on_junction():
            # Junction work
            pass
        elif decision.is_on_end():
            # End work
            pass

    elif decision.state == 'box_lift':
        ######################################
        # Position the robot to lift the box #
        ######################################
        control.lift_the_box()
    elif decision.state == 'path':
        #######################################################
        # Process the frame to create a path from arrow heads #
        #######################################################
        pid.run_pid(robot.processed_frame)
        control.drive()
    elif decision.state == 'box_place':
        #######################################
        # Position the robot to place the box #
        #######################################
        control.place_the_box()
    else:       # state == 'stop'
        control.stop()

    cv2.imshow('Feed', robot.current_frame)
    cv2.imshow('Processed feed', robot.processed_frame)

    if cv2.waitKey(1) % 256 == 27:
        break

    #
    #
    #
    #
    #
    # All the testing code go after this #########################################################################

    # box.detect_box(frame, return_frame)


