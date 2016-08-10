#this is not a part of the robot used to manually calibate color filtering
import numpy as np
import cv2


def empty(e):#empty fuction
    pass

def calibration(frame,hue_low,value_low,satu_low,hue_high,value_high,satu_high):

    color_low = np.array([hue_low,satu_low,value_low])
    color_high = np.array([hue_high,satu_high,value_high])

    hsv_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv_frame,color_low,color_high)

    mframe=cv2.bitwise_and(frame,frame,mask=mask)
    gframe = cv2.cvtColor(mframe,cv2.COLOR_BGR2GRAY)
    blurred= cv2.GaussianBlur(gframe, (5, 5), 0)
    ret, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    rframe = cv2.cvtColor(thresh,cv2.COLOR_GRAY2BGR)
    _, contours, _  = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        cv2.drawContours(rframe,c,-1, (0,0,255), 2)

    cv2.imshow('Calibrated',rframe)




cam = cv2.VideoCapture(0)
cv2.namedWindow('Adjust')

cv2.createTrackbar('hue_low','Adjust',0,179,empty)
cv2.createTrackbar('satu_low','Adjust',0,255,empty)
cv2.createTrackbar('value_low','Adjust',0,255,empty)

cv2.createTrackbar('hue_high','Adjust',0,179,empty)
cv2.createTrackbar('satu_high','Adjust',0,255,empty)
cv2.createTrackbar('value_high','Adjust',0,255,empty)

while True:
    ret, frame = cam.read()
    hue_high = cv2.getTrackbarPos('hue_high','Adjust')
    satu_high = cv2.getTrackbarPos('satu_high','Adjust')
    value_high = cv2.getTrackbarPos('value_high','Adjust')

    hue_low = cv2.getTrackbarPos('hue_low','Adjust')
    satu_low = cv2.getTrackbarPos('satu_low','Adjust')
    value_low = cv2.getTrackbarPos('value_low','Adjust')

    calibration(frame,hue_low,value_low,satu_low,hue_high,value_high,satu_high)
    cv2.imshow('feed',frame)


    if cv2.waitKey(1) % 256 == 27:
        break
