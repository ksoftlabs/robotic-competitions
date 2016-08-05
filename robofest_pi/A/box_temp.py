import cv2
import numpy as np
import cmn


def detect_box(frame, output):
    blue = np.uint8([[[255,0,0]]])
    green = np.uint8([[[0,255,0]]])
    red = np.uint8([[[0,0,255]]])

    hsv_blue = cv2.cvtColor(blue, cv2.COLOR_BGR2HSV)
    hsv_green = cv2.cvtColor(green, cv2.COLOR_BGR2HSV)
    hsv_red = cv2.cvtColor(red, cv2.COLOR_BGR2HSV)

    half = 20
    hue_low = 60
    value_low = 60
    blue_range = (np.uint8([hsv_blue[0,0,0]-half,hue_low,value_low]),np.uint8([hsv_blue[0,0,0]+half,255,255]))
    green_range = (np.uint8([hsv_green[0,0,0]-half,hue_low,value_low]),np.uint8([hsv_green[0,0,0]+half,255,255]))
    red_range = (np.uint8([hsv_red[0,0,0]-half,hue_low,value_low]),np.uint8([hsv_red[0,0,0]+half,255,255]))


    #for testing
    cmn.find_objects(frame, blue_range, "Blue")
    cmn.find_objects(frame, green_range, "Green")
    cmn.find_objects(frame, red_range, "Red")
