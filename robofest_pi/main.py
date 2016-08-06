import physics
import communicate
import movement
import maze_logic
import box_logic
import path_logic

import cv2
import time
import common
import contour


comm = communicate.Port()                           # Raspberry pi - Arduino serial communication interface
robot = physics.Robot(comm, '192.168.1.2:8080')     # Define current robot state
pid = movement.PID(robot)                           # Adjust course through pid
control = movement.Control(robot, comm)             # Robot movement controls

maze = maze_logic.Maze(robot)                       # Maze logic
box = box_logic.Box(robot)                          # Box logic
path = path_logic.Path(robot)                       # Path logic

#################################################################################################################
# Testing area
while True:
    robot.see()
    start = time.time()

    # Contours
    frame_hsv = cv2.cvtColor(robot.current_frame, cv2.COLOR_BGR2HSV)

    frame_mask = common.get_red_mask(frame_hsv) + common.get_green_mask(frame_hsv) + common.get_blue_mask(frame_hsv)
    robot.processed_frame = cv2.bitwise_and(robot.current_frame, robot.current_frame, mask=frame_mask)

    gray_img = cv2.cvtColor(robot.processed_frame, cv2.COLOR_BGR2GRAY)
    threshold_img = common.get_otsu_gaussian_threshold(gray_img)

    contours = common.get_contours(threshold_img)

    for cnt in contours:
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.01 * peri, True)
        cv2.drawContours(robot.processed_frame, [approx], -1, (255, 0, 0), 2)

        if len(approx) == 7:
            for i in range(7):
                arrow = contour.Arrow(approx, i)

                if arrow.is_valid_arrow():
                    arrow.calculate_mid_point()

                    arrow.draw_initial_point(robot.processed_frame)
                    arrow.draw_mid_base_point(robot.processed_frame)

                    arrow.enable_lines(robot.processed_frame)
                    arrow.enable_labels(robot.processed_frame)

    end = time.time()
    diff = end - start
    if diff == 0:
        diff = 0.0000001

    fps = 1.0 / diff

    common.draw_machine_details(robot.processed_frame, fps)

    cv2.imshow('Feed', robot.current_frame)
    cv2.imshow('Threshold image', gray_img)
    cv2.imshow('Processed feed', robot.processed_frame)

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

robot.cam.release()
cv2.destroyAllWindows()
