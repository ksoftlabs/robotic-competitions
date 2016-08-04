import cv2
import box_logic
import communicate
import maze_logic
import movement
import path_logic
import physics

comm = communicate.Port()                   # Raspberry pi - Arduino serial communication interface
robot = physics.Robot(comm)                 # Define current robot state
pid = movement.PID(robot)                   # Adjust course through pid
control = movement.Control(robot, comm)     # Robot movement controls

maze = maze_logic.Maze(robot)               # Maze logic
box = box_logic.Box(robot)                  # Box logic
path = path_logic.Path(robot)               # Path logic

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


