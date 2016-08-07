import cv2
import numpy as np
def detect_box(frame,right,left,top,bottom):
    lower_red_range = (np.array([0, 50, 50]), np.array([10, 255, 255]))
    upper_red_range = (np.array([170, 50, 50]), np.array([180, 255, 255]))
    blue_range = (np.array([80, 50, 50]), np.array([160, 255, 255]))
    green_range = (np.array([160, 50, 50]) , np.array([260, 255, 255]))

    crop_frame(frame,right,left,top,bottom)

    #arrows, rectangles = cmn.find_objects(frame, [lower_red_range,upper_red_range,blue_range,green_range], "Omini color box")

def crop_frame(frame,right,left,top,bottom):
    rows,cols,channel = frame.shape
    T = np.float32([[1,0,-left],[0,1,-top]])
    croped1 = cv2.warpAffine(frame,T,(cols,rows))
    T = np.float32([[1,0,left+right],[0,1,top+bottom]])
    croped2 = cv2.warpAffine(croped1,T,(cols,rows))
    T = np.float32([[1,0,-right],[0,1,-bottom]])
    croped3 = cv2.warpAffine(croped2,T,(cols,rows))
    cv2.imshow("Croped ", croped3)
    #return croped2
