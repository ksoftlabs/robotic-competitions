# Interface to detect and navigate on arrow-head path
import cv2
import numpy as np

def detect_maze(self, frame, output): #why are we taking self here ?
    return output


def detect_arrow(frame,return_frame): #takes a grey scalled frame(with arrows with corresponding color)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#for testing
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    #thresh = cv2.threshold(blurred, 255, cv2.THRESH_BINARY+cv2)[1]#without OTSU methode

    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

    #for testing
    contour_details = contours[-1]
    contours = contours[:-1]
    for c in contours:
        cv2.drawContours(thresh, c, -1, (255, 0, 0), 2)
    #for testing

    return thresh
