import physics
import communicate
import movement
import box_logic

comm = communicate.Port()                           # Raspberry pi - Arduino serial communication interface
robot = physics.Robot(comm, '192.168.1.2:8080')     # Define current robot state
pid = movement.PID(robot)                           # Adjust course through pid
control = movement.Control(robot, comm)             # Robot movement controls

box = box_logic.Box(robot)                          # Box logic


ls = box.left_shifting()        #distance to left from the center
rs = box.right_shifting()       #distance to right from the center
if ls > 0:
    control.turn_left()
elif rs > 0:
    control.turn_right()
else:
    ### Go to the box ###
    robot.state = 'box_lift'
