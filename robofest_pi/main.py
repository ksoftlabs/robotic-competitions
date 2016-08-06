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
import common
import sys

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

    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    lower_red_mask = cv2.inRange(frame_hsv, lower_red, upper_red)

    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    upper_red_mask = cv2.inRange(frame_hsv, lower_red, upper_red)

    lower_green = np.array([80, 50, 50])
    upper_green = np.array([160, 255, 255])
    green_mask = cv2.inRange(frame_hsv, lower_green, upper_green)

    lower_blue = np.array([160, 50, 50])
    upper_blue = np.array([260, 255, 255])
    blue_mask = cv2.inRange(frame_hsv, lower_blue, upper_blue)

    img_mask = lower_red_mask + upper_red_mask + green_mask + blue_mask

    robot.processed_frame = cv2.bitwise_and(robot.current_frame, robot.current_frame, mask=img_mask)

    rgb = cv2.cvtColor(robot.processed_frame, cv2.COLOR_HSV2RGB)
    gray = cv2.cvtColor(robot.processed_frame, cv2.COLOR_RGB2GRAY)
    # ret, thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)

    # Otsu's thresholding
    # ret2, thresh2 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Otsu's thresholding after Gaussian filtering
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    ret3, thresh3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    cv2.imshow('thresh3', gray)
    _, contours, _ = cv2.findContours(thresh3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # cv2.drawContours(robot.processed_frame, contours, -1, (0, 0, 255), 2)

    # Good features to track
    # corners = cv2.goodFeaturesToTrack(gray, 7, 0.01, 10)
    # if corners is not None:
    #     corners = np.int0(corners)
    #
    #     for i in corners:
    #         x, y = i.ravel()
    #         cv2.circle(robot.processed_frame, (x, y), 3, 255, -1)
    # else:
    #     pass

    # Corner detection
    # gray = np.float32(gray)
    # dst = cv2.cornerHarris(gray, 2, 29, 0.05)
    # # Result is dilated for marking the corners, not important
    # dst = cv2.dilate(dst, None)
    # # Threshold for an optimal value, it may vary depending on the image.
    # robot.current_frame[dst > 0.1 * dst.max()] = [0, 0, 255]
    # cv2.imshow('dst', robot.current_frame)

    # Process contours
    for cnt in contours:
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        # m1 = cv2.moments(approx)
        cv2.drawContours(robot.processed_frame, [approx], -1, (255, 0, 0), 2)

        if len(approx) == 7:
            print '___________________________________________________________________________________________________'
            for c in approx:
                sys.stdout.write(str(c) + '     ')
            print ' '

            for i in range(7):
                xi0 = approx[i][0][0]
                yi0 = approx[i][0][1]
                xi1 = approx[(i + 1) % 6][0][0]
                yi1 = approx[(i + 1) % 6][0][1]
                xi2 = approx[(i + 2) % 6][0][0]
                yi2 = approx[(i + 2) % 6][0][1]
                xi3 = approx[(i + 3) % 6][0][0]
                yi3 = approx[(i + 3) % 6][0][1]
                if i == 0:
                    xin2 = approx[5][0][0]
                    yin2 = approx[5][0][1]
                elif i == 1:
                    xin2 = approx[6][0][0]
                    yin2 = approx[6][0][1]
                else:
                    xin2 = approx[i - 2][0][0]
                    yin2 = approx[i - 2][0][1]

                m1 = common.find_gradient(xi0, yi0, xi1, yi1)
                m2 = common.find_gradient(xi2, yi2, xi3, yi3)

                d1 = common.find_distance(xi0, yi0, xi1, yi1)
                d2 = common.find_distance(xi2, yi2, xi3, yi3)

                diff = abs(m1 - m2)
                dist_diff = abs(d1 - d2)
                if diff <= 0.3 and dist_diff <= 10:
                    xmid = (xi1 + xi2) / 2
                    ymid = (yi1 + yi2) / 2

                    cv2.circle(robot.processed_frame, (xi0, yi0), 4, (0, 255, 0), 2)
                    cv2.line(robot.processed_frame, (xmid, ymid), (xin2, yin2), (0, 255, 0), 2)
                    cv2.line(robot.processed_frame, (xi0, yi0), (xi1, yi1), (255, 255, 255), 2)
                    cv2.line(robot.processed_frame, (xi2, yi2), (xi3, yi3), (255, 255, 255), 2)

                    cv2.putText(robot.processed_frame, str(i), (xi0 + 10, yi0 + 10),
                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (255, 255, 255))
                    cv2.putText(robot.processed_frame, str(i + 1), (xi1 + 10, yi1 + 10),
                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (255, 255, 255))
                    cv2.putText(robot.processed_frame, str(i + 2), (xi2 + 10, yi2 + 10),
                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (255, 255, 255))
                    cv2.putText(robot.processed_frame, str(i + 3), (xi3 + 10, yi3 + 10),
                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (255, 255, 255))
                    cv2.putText(robot.processed_frame, str('HEAD'), (xin2 + 10, yin2 + 10),
                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (255, 255, 255))
                    cv2.putText(robot.processed_frame, str('BASE'), (xmid + 10, ymid + 10),
                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (255, 255, 255))
                    print str(m1) + ',' + str(m2) + ',' + str(diff) + '     ' + str(d1) + ',' + str(d2) + ',' + str(dist_diff)
                    # break
                # else:
                #     print str(m1) + ',' + str(m2) + ',' + str(diff) + '     ' + str(d1) + ',' + str(d2) + ',' + str(dist_diff)

        # rect = cv2.minAreaRect(cnt)
        # box = cv2.boxPoints(rect)
        # box = np.int0(box)
        # m2 = cv2.moments(box)
        # robot.processed_frame = cv2.drawContours(robot.processed_frame, [box], 0, (0, 0, 255), 2)


        # try:
        #     (cm1X, cm1Y) = (int(m1["m10"] / m1["m00"]), int(m1["m01"] / m1["m00"]))
        #     (cm2X, cm2Y) = (int(m2["m10"] / m2["m00"]), int(m2["m01"] / m2["m00"]))
        #     cv2.circle(robot.processed_frame, (cm1X, cm1Y), 1, (255, 0, 0), 2)
        #     cv2.circle(robot.processed_frame, (cm2X, cm2Y), 1, (0, 0, 255), 2)
        # except:
        #     pass


    end = time.time()
    diff = end - start
    if diff == 0:
        diff = 10000

    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    # cv2.putText(robot.current_frame, 'FPS ' + str(1.0 / diff), (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8,
    #             (255, 0, 0))
    # cv2.putText(robot.current_frame, 'CPU usage ' + str(cpu), (10, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8,
    #             (255, 0, 0))
    # cv2.putText(robot.current_frame, 'Memory usage ' + str(mem), (10, 70), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8,
    #             (255, 0, 0))
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
