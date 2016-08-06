import cv2
import numpy as np
import global_values as g


class Path:
    def __init__(self, robot):
        self.robot = robot

    @staticmethod
    def get_red_mask(frame_hsv):
        lower_red = np.array([g.red_lower1, g.lower_saturation, g.lower_value])
        upper_red = np.array([g.red_upper1, g.upper_saturation, g.upper_value])
        lower_red_mask = cv2.inRange(frame_hsv, lower_red, upper_red)

        lower_red = np.array([g.red_lower2, g.lower_saturation, g.lower_value])
        upper_red = np.array([g.red_upper2, g.upper_saturation, g.upper_value])
        upper_red_mask = cv2.inRange(frame_hsv, lower_red, upper_red)

        return lower_red_mask + upper_red_mask

    @staticmethod
    def get_green_mask(frame_hsv):
        lower_green = np.array([g.green_lower, g.lower_saturation, g.lower_value])
        upper_green = np.array([g.green_upper, g.upper_saturation, g.upper_value])
        return cv2.inRange(frame_hsv, lower_green, upper_green)

    @staticmethod
    def get_blue_mask(frame_hsv):
        lower_blue = np.array([g.blue_lower, g.lower_saturation, g.lower_value])
        upper_blue = np.array([g.blue_upper, g.upper_saturation, g.upper_value])
        return cv2.inRange(frame_hsv, lower_blue, upper_blue)
