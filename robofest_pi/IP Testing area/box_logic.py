import cv2
import numpy as np
import common
def detect_box(frame,right,left,top,bottom):
    lower_red_range = (np.array([0, 50, 50]), np.array([10, 255, 255]))
    upper_red_range = (np.array([170, 50, 50]), np.array([180, 255, 255]))
    blue_range = (np.array([80, 50, 50]), np.array([160, 255, 255]))
    green_range = (np.array([160, 50, 50]) , np.array([260, 255, 255]))

    crop_frame(frame,right,left,top,bottom)

    #arrows, rectangles = cmn.find_objects(frame, [lower_red_range,upper_red_range,blue_range,green_range], "Omini color box")


class Box:
    def __init__(self, robot):
        self.robot = robot
        self.color = None
        self.points = None
        self.center_x = 0
        self.image_half_width = 500  ##### TO EDIT: get the width from a global variable #####
        self.center_accuracy = 100  # is used when checking the box is in the center or not
        self.variance = 0.2 # Variance for right-square

    def is_box_totally_visible(self):
        self.points = None
        if self.color is None:
            masked = common.apply_mask(self.robot.current_frame)
        else:
            masked = common.apply_mask(self.robot.current_frame,self.color)
        gray_img = cv2.cvtColor(masked,cv2.COLOR_BGR2GRAY)
        thresh = common.get_otsu_gaussian_threshold(gray_img)
        contours = common.get_contours(thresh)
        self.look_for_box(contours,self.variance)

    def look_for_box(contours,var):
        for c in contours:
            moments = cv2,moments(c)
            if moments["m00"] > 10000: #make 1000 if it didnt work
                r = cv2.minAreaRect(c)
                r = ((r[0][0], r[0][1]), (r[1][0], r[1][1]), r[2])
                (width,height)=(r[1][0], r[1][1])
                box = cv2.boxPoints(r)
                box = int0(box)
                if (height > (1 - var) * width and height < (1 + var) * width):
                    self.box_points = box
                    self.box_center_x = int(box[:, 0].mean())
                    return True
        return False
        
    def is_box_seen(self):
        ########### is box partially visible code goes here ###############



        pass




##############3 debugging code ##############################
    def show(self):  # For testing
        frame = self.robot.current_frame
        if self.is_box_seen():
            cv2.drawContours(frame, [self.points], 0, (0, 0, 255), 2)
            cv2.circle(frame, (self.box_center_x, 100), 7, (0, 0, 255), 1)

            ls = self.left_shifting()
            rs = self.right_shifting()
            if ls > 0:
                cv2.putText(frame, "LEFT SHIFT " + str(ls), (self.image_half_width - 200, 100), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0, 255, 255))
            elif rs > 0:
                cv2.putText(frame, "RIGHT SHIFT " + str(rs), (self.image_half_width + 200, 100), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0, 255, 255))
            else:
                cv2.putText(frame, "CENTERED", (self.image_half_width, 100), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0, 255, 0))



        cv2.imshow("Box View", frame)

    def is_centered(self):  # Check wheather the box is centered or not
        return abs(self.image_half_width - self.box_center_x) <= self.center_accuracy

    def left_shifting(self):  # Distance to the left from the center
        shifting = (self.image_half_width - self.center_accuracy) - self.box_center_x
        return shifting if shifting > 0 else 0

    def right_shifting(self):  # Distance to the right from the center
        shifting = self.box_center_x - (self.image_half_width + self.center_accuracy)
        return shifting if shifting > 0 else 0
