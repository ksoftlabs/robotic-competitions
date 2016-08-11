import cv2
import numpy as np
import physics
import communicate
#import movement
import box_logic
from AndroidCamFeed import AndroidCamFeed

comm = communicate.Port()                           # Raspberry pi - Arduino serial communication interface

#robot = physics.Robot(comm, '192.168.43.1:8080')     # Define current robot state
robot = physics.Robot(comm)
#pid = movement.PID(robot)                           # Adjust course through pid
#control = movement.Control(robot, comm)             # Robot movement controls

box = box_logic.Box(robot)                          # Box logic

while True:
    robot.see()
    box.check()
    if box.is_box_totally_visible():
        ls = box.left_shifting()        #distance to left from the center
        rs = box.right_shifting()       #distance to right from the center
        if ls > 0:
            #control.turn_left()
            pass
        elif rs > 0:
            #control.turn_right()
            pass
        else:
            ### Go to the box ###
            #robot.state = 'box_lift'
            pass
    elif box.is_box_partially_visible():
        pass
        
    box.show() #show frames
        
    if cv2.waitKey(1) % 256 == 27:
        break




