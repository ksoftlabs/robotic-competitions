import movement
from time import sleep

import physics


def movement_test():
    robot = physics.Robot()
    control = movement.Control(robot)

    control.forward()
    sleep(1)

    control.reverse()
    sleep(1)

    control.turn_left()
    sleep(1)

    control.turn_right()
    sleep(1)

    control.turn_back()
    sleep(1)