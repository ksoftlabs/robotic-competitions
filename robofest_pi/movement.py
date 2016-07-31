import communicate
from time import sleep


class Robot:
    def __init__(self):
        self.lf = 0     # Left-front motor speed
        self.rf = 0     # Right-front motor speed
        self.lb = 0     # Left-back motor speed
        self.rb = 0     # Right-back motor speed


class PID:
    def __init__(self, robot):
        self.robot = robot
        self.base_speed = 150                               # Speed when moving straight >> affect the average speed
        self.pVar, self.iVar, self.dVar = 0.0, 0.0, 0.0     # Proportional, Integral and Derivative values
        self.kp, self.ki, self.kd = 0.0, 0.0, 0.0           # Proportional, Integral and Derivative constants
        self.error = 0.0                                    # Current error
        self.pre_error = 0.0                                # Previous error
        self.turn = 0.0

    def calculate_error(self):
        self.pre_error = self.error
        ###########################
        # Calculate the new error #
        ###########################

    def run_pid(self):
        self.calculate_error()

        # Calculate P
        self.pVar = self.kp * self.error

        # Calculate I
        if self.error == 0.0:
            self.iVar = 0.0
        else:
            self.iVar = (self.iVar + self.error) * self.ki

        # Calculate D
        self.dVar = (self.error - self.pre_error) * self.kd

        self.turn = self.pVar + self.iVar + self.dVar
        self.robot.lf = self.base_speed - self.turn
        self.robot.rf = self.base_speed + self.turn
        self.robot.lb = self.base_speed - self.turn
        self.robot.rb = self.base_speed + self.turn


class Control:
    def __init__(self, robot):
        self.robot = robot
        self.comm = communicate.Port()
        self.positive_thresh = 110          # Minimum forward power level which the dc motors work
        self.negative_thresh = -110         # Minimum reverse power level which the dc motors work

    # Control the motor speeds
    def drive(self, lf, rf, lb, rb):
        self.robot.lf = lf
        self.robot.rf = rf
        self.robot.lb = lb
        self.robot.rb = rb

        # Change the power level if motors are in stall state
        diff = (self.positive_thresh - self.negative_thresh)
        if self.robot.lf < self.positive_thresh & self.robot.lf > self.negative_thresh:
            self.robot.lf -= diff
        if self.robot.rf < self.positive_thresh & self.robot.rf > self.negative_thresh:
            self.robot.rf -= diff
        if self.robot.lb < self.positive_thresh & self.robot.lb > self.negative_thresh:
            self.robot.lb -= diff
        if self.robot.rb < self.positive_thresh & self.robot.rb > self.negative_thresh:
            self.robot.rb -= diff

        # Verify whether motor power values are in range of -255 and 255
        if self.robot.lf > 255:
            self.robot.lf = 255
        elif self.robot.lf < -255:
            self.robot.lf = -255

        if self.robot.rf > 255:
            self.robot.rf = 255
        elif self.robot.rf < -255:
            self.robot.rf = -255

        if self.robot.lb > 255:
            self.robot.lb = 255
        elif self.robot.lb < -255:
            self.robot.lb = -255

        if self.robot.rb > 255:
            self.robot.rb = 255
        elif self.robot.rb < -255:
            self.robot.rb = -255

        self.comm.change_speed(self.robot.lf, self.robot.rf, self.robot.lb, self.robot.rb)

    def forward(self, speed=150, t=0.1):
        speed = abs(speed)
        self.drive(speed, speed, speed, speed)
        sleep(t)

    def reverse(self, speed=130, t=0.1):
        speed = abs(speed)
        self.drive(-1 * speed, -1 * speed, -1 * speed, -1 * speed)
        sleep(t)

    def turn_left(self, speed=170, t=0.01):
        speed = abs(speed)
        self.drive(-1 * speed, speed, -1 * speed, speed)
        sleep(t)

    def turn_right(self, speed=170, t=0.01):
        speed = abs(speed)
        self.drive(speed, -1 * speed, speed, -1 * speed)
        sleep(t)

    def turn_back(self, speed=180, t=1):
        speed = abs(speed)
        self.drive(speed, -1 * speed, speed, -1 * speed)
        sleep(t)
