from time import sleep


class PID:
    def __init__(self, robot):
        self.robot = robot
        self.base_speed = 150                               # Speed when moving straight >> affect the average speed
        self.pVar, self.iVar, self.dVar = 0.0, 0.0, 0.0     # Proportional, Integral and Derivative values
        self.kp, self.ki, self.kd = 0.0, 0.0, 0.0           # Proportional, Integral and Derivative constants
        self.error = 0.0                                    # Current error
        self.pre_error = 0.0                                # Previous error
        self.turn = 0.0

    def calculate_error(self, frame):
        self.pre_error = self.error
        ###########################
        # Calculate the new error #
        ###########################

    def run_pid(self, frame):
        self.calculate_error(frame)

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
        self.robot.lf_motor = self.base_speed - self.turn
        self.robot.rf_motor = self.base_speed + self.turn
        self.robot.lb_motor = self.base_speed - self.turn
        self.robot.rb_motor = self.base_speed + self.turn


class Control:
    def __init__(self, robot, comm):
        self.robot = robot
        self.comm = comm
        self.positive_thresh = 110          # Minimum forward power level which the dc motors work
        self.negative_thresh = -110         # Minimum reverse power level which the dc motors work

    # Control the motor speeds
    def drive(self, lf_motor=None, rf_motor=None, lb_motor=None, rb_motor=None):
        if lf_motor is not None:
            self.robot.lf_motor = lf_motor
        if rf_motor is not None:
            self.robot.rf_motor = rf_motor
        if lb_motor is not None:
            self.robot.lb_motor = lb_motor
        if rb_motor is not None:
            self.robot.rb_motor = rb_motor

        # Change the power level if motors are in stall state
        diff = (self.positive_thresh - self.negative_thresh)
        if (self.robot.lf_motor < self.positive_thresh) & (self.robot.lf_motor > self.negative_thresh):
            self.robot.lf_motor -= diff
        if (self.robot.rf_motor < self.positive_thresh) & (self.robot.rf_motor > self.negative_thresh):
            self.robot.rf_motor -= diff
        if (self.robot.lb_motor < self.positive_thresh) & (self.robot.lb_motor > self.negative_thresh):
            self.robot.lb_motor -= diff
        if (self.robot.rb_motor < self.positive_thresh) & (self.robot.rb_motor > self.negative_thresh):
            self.robot.rb_motor -= diff

        # Verify whether motor power values are in range of -255 and 255
        if self.robot.lf_motor > 255:
            self.robot.lf_motor = 255
        elif self.robot.lf_motor < -255:
            self.robot.lf_motor = -255

        if self.robot.rf_motor > 255:
            self.robot.rf_motor = 255
        elif self.robot.rf_motor < -255:
            self.robot.rf_motor = -255

        if self.robot.lb_motor > 255:
            self.robot.lb_motor = 255
        elif self.robot.lb_motor < -255:
            self.robot.lb_motor = -255

        if self.robot.rb_motor > 255:
            self.robot.rb_motor = 255
        elif self.robot.rb_motor < -255:
            self.robot.rb_motor = -255

        self.comm.change_speed(self.robot.lf_motor, self.robot.rf_motor, self.robot.lb_motor, self.robot.rb_motor)

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

    def brake(self):
        pass

    def stop(self):
        pass

    def lift_the_box(self):
        print 'Lifting the box....'

    def place_the_box(self):
        print 'Placing the box....'