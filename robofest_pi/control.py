class Robot:
    def __init__(self):
        self.lf = 0     # Left-front motor speed
        self.rf = 0     # Right-front motor speed
        self.lb = 0     # Left-back motor speed
        self.rb = 0     # Right-back motor speed


class PID:
    def __init__(self, robot):
        self.robot = robot
        self.base_speed = 150
        self.pVar, self.iVar, self.dVar = 0.0, 0.0, 0.0
        self.kp, self.ki, self.kd = 0.0, 0.0, 0.0           # Proportional, Integral and Derivative constants
        self.error = 0.0                                    # Current error
        self.pre_error = 0.0                                # Previous error
        self.turn = 0.0

    def calculate_error(self):
        self.pre_error = self.error

        # Calculate the new error

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
        self.positive_thresh, self.negative_thresh = 110, -110      # Threshold levels which the dc motors work

    # Change the stall state motor speed values
    def adjust_speed(self):
        diff = (self.positive_thresh - self.negative_thresh)
        if self.robot.lf < self.positive_thresh:
            self.robot.lf -= diff
        if self.robot.rf < self.positive_thresh:
            self.robot.rf -= diff
        if self.robot.lb < self.positive_thresh:
            self.robot.lb -= diff
        if self.robot.rb < self.positive_thresh:
            self.robot.rb -= diff

    # Control the motor speeds with the current values in the robot object
    def drive(self):
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
