class State:
    def __init__(self):
        self.base_speed = 150
        self.pVar, self.iVar, self.dVar = 0.0, 0.0, 0.0
        self.kp, self.ki, self.kd = 0.0, 0.0, 0.0
        self.error, self.pre_error = 0.0, 0.0
        self.turn = 0.0
        self.lf, self.rf, self.lb, self.rb = 0, 0, 0, 0

    def calculate_error(self):
        self.pre_error = self.error

        # Calculate the new error

    def pid(self):
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
        self.lf = self.base_speed - self.turn
        self.rf = self.base_speed + self.turn
        self.lb = self.base_speed - self.turn
        self.rb = self.base_speed + self.turn


class Control:
    def __init__(self):
        self.lf, self.rf, self.lb, self.rb = 0, 0, 0, 0
        self.positive_thresh, self.negative_thresh = 110, -110

    def adjust_speed(self):
        diff = (self.positive_thresh - self.negative_thresh)
        if self.lf < self.positive_thresh:
            self.lf -= diff
        if self.rf < self.positive_thresh:
            self.rf -= diff
        if self.lb < self.positive_thresh:
            self.lb -= diff
        if self.rb < self.positive_thresh:
            self.rb -= diff

    def drive(self, lf, rf, lb, rb):
        if lf > 255:
            lf = 255
        elif lf < -255:
            lf = -255

        if rf > 255:
            rf = 255
        elif rf < -255:
            rf = -255

        if lb > 255:
            lb = 255
        elif lb < -255:
            lb = -255

        if rb > 255:
            rb = 255
        elif rb < -255:
            rb = -255
