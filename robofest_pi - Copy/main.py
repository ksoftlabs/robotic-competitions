import physics
import communicate
import movement
import maze_logic
import box_logic
import path_logic

import cv2
import time
import common


comm = communicate.Port()                                   # Raspberry pi - Arduino serial communication interface
# robot = physics.Robot(comm, '192.168.1.4:8080')             # Define current robot state
robot = physics.Robot(comm)                                 # Define current robot state
path_queue = movement.PathQueue(robot.get_frame_height())   # Expected path offset values
pid = movement.PID(robot, path_queue)                       # Adjust course through pid
control = movement.Control(robot, comm)                     # Robot movement controls

maze = maze_logic.Maze(robot)                               # Maze logic
box = box_logic.Box(robot)                                  # Box logic
path = path_logic.Path(robot, path_queue, box)              # Path logic

#################################################################################################################
# Testing area

frame_width = robot.get_frame_width()
frame_height = robot.get_frame_height()

while True:
    robot.see('arrows.png')
    start = time.time()

    path.create_path()

    end = time.time()
    diff = end - start
    if diff == 0:
        diff = 0.0000001

    fps = 1.0 / diff

    common.draw_machine_details(robot.processed_frame, fps)
    common.draw_crosshair(robot.processed_frame, width=frame_width, height=frame_height)

    cv2.imshow('Feed', robot.current_frame)
    cv2.imshow('Processed feed', robot.processed_frame)
    cv2.imshow('Threshold image', path.threshold_img)

    if cv2.waitKey(1) % 256 == 27:
        break
robot.cam.release()
cv2.destroyAllWindows()
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
        pid.run_pid(offset=True)
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

robot.cam.release()
cv2.destroyAllWindows()
