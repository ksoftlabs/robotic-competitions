#import cv2
#import numpy as np
#import communicate
#import physics
#from AndroidCamFeed import AndroidCamFeed

class Box:
    def __init__(self, robot):
        self.robot = robot
        self.box_color = None
        self.all_rectangles = []                    #Optional
        self.box_points = None
        self.box_center_x = 0
        self.image_half_width = 768 ##### TO EDIT: get the width from a global variable #####
        self.center_accuracy = 100                  #is used when checking the box is in the center or not

    def check(self):
        self.all_rectangles = []
        self.box_points = None

        #Color Ranges
        lower_blue = np.array([110, 50, 50],np.uint8)
        upper_blue = np.array([130,255,255],np.uint8)
        #lower_green = 
        #upper_green = 
        #lower_red = 
        #upper_red = 
        

        #check box for each color
        if self.check_box_by_color(lower_blue, upper_blue):
            self.box_color = "BLUE"
            return
        #elif self.check_box_by_color(lower_green, upper_green):
            #self.box_color = "GREEN"
            #return
        #elif self.check_box_by_color(lower_red, upper_red):
            #self.box_color = "RED"
            #return
        else:
            self.box_color = None
            
    def check_box_by_color(self, lower, upper):
        img=cv2.cvtColor(robot.current_frame, cv2.COLOR_BGR2HSV)
        separated=cv2.inRange(img,lower,upper)

        cv2.imshow("a", separated)

        im,contours,hierarchy=cv2.findContours(separated,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        max_area = 0
        largest_contour = None
        var = 0.2     #Variance for right-square
        
        for idx, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                largest_contour=contour
                if not largest_contour==None:
                    moment = cv2.moments(largest_contour)
                    if moment["m00"] > 1000:
                        rect = cv2.minAreaRect(largest_contour)
                        rect = ((rect[0][0], rect[0][1]), (rect[1][0], rect[1][1]), rect[2])
                        (width,height)=(rect[1][0],rect[1][1])
                        box = cv2.boxPoints(rect)
                        box = np.int0(box)
                        self.all_rectangles.append(box)                         #Optional: adding all rectangles to a list
                        if(height>(1-var)*width and height<(1+var)*width):
                            self.box_points = box
                            self.box_center_x = int(box[:,0].mean())
                            return True
        return False
        
    def is_box_seen(self):
        self.check()
        return self.box_points != None

    def show(self):                         # For testing
        frame = robot.current_frame
        if self.is_box_seen():
            cv2.drawContours(frame,[self.box_points], 0, (0, 0, 255), 2)
            cv2.circle(frame, (self.box_center_x,100), 7, (0,0,255), 1)
        cv2.imshow("Box View", frame)

    def is_centered(self):                 #Check wheather the box is centered or not
        return abs(self.image_half_width - self.box_center_x) <= self.center_accuracy

    def left_shifting(self):               #Distance to the left from the center
        shifting = (self.image_half_width - self.center_accuracy) - self.box_center_x
        return shifting if shifting > 0 else 0

    def right_shifting(self):               #Distance to the right from the center
        shifting = self.box_center_x - (self.image_half_width + self.center_accuracy)
        return shifting if shifting > 0 else 0

    #def is_box_partially_visible(self):
        #pass

    #def is_box_totally_visible(self):
        #pass


##########

#comm = communicate.Port()                           # Raspberry pi - Arduino serial communication interface
#robot = physics.Robot(comm, '192.168.43.1:8080')
#box = Box(robot)

#while True:
    #robot.see()
    #box.check()
    #box.show()
    #if box.is_box_seen():
        #print "BOX"
        #print box.left_shifting()
        #print box.right_shifting()

    #cv2.imshow("show", robot.current_frame)

    #if cv2.waitKey(1) % 256 == 27:
        #break

