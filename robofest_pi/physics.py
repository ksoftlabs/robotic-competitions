class Robot:
    def __init__(self, comm):
        self.comm = comm

        self.lf_motor = 0     # Left-front motor speed
        self.rf_motor = 0     # Right-front motor speed
        self.lb_motor = 0     # Left-back motor speed
        self.rb_motor = 0     # Right-back motor speed

        self.front_sonar = 0
        self.left_sonar = 0
        self.right_sonar = 0
        self.back_sonar = 0

    def update_sonar_data(self):
        self.front_sonar = self.comm.get_front_distance()
        self.left_sonar = self.comm.get_left_distance()
        self.right_sonar = self.comm.get_right_distance()
        self.back_sonar = self.comm.get_back_direction()
