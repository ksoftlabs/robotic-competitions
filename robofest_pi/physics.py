import cv2
import numpy as np


class Robot:
    def __init__(self, cam, comm):
        # Dimensions
        self.length = 0.0
        self.width = 0.0
        self.height = 0.0

        # Capture the feed from camera
        self.cam = cv2.VideoCapture(0)
        self.ret, self.current_frame = self.cam.read()
        self.processed_frame = np.zeros(self.current_frame.shape, np.uint8)

        self.comm = comm

        self.state = 'maze'

        self.lf_motor = 0     # Left-front motor speed
        self.rf_motor = 0     # Right-front motor speed
        self.lb_motor = 0     # Left-back motor speed
        self.rb_motor = 0     # Right-back motor speed

        self.front_sonar = 0    # Front sonar distance
        self.left_sonar = 0     # Left sonar distance
        self.right_sonar = 0    # Right sonar distance
        self.back_sonar = 0     # Back sonar distance

    def see(self):
        self.ret, self.current_frame = self.cam.read()

    def update_sonar_data(self):
        self.front_sonar = self.comm.get_front_distance()
        self.left_sonar = self.comm.get_left_distance()
        self.right_sonar = self.comm.get_right_distance()
        self.back_sonar = self.comm.get_back_direction()
