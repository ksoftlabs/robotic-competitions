#this is not a part of the robot used to manually calibate color filtering
import numpy as np
import cv2
import common
from matplotlib import pyplot as plt

def make_details_windwow(frame):#histogram initalizing not wokinng
    histr_RED = cv2.calcHist([frame],[0],None,[256],[0,256])
    histr_GREEN = cv2.calcHist([frame],[1],None,[256],[0,256])
    histr_BLUE = cv2.calcHist([frame],[2],None,[256],[0,256])
    plt.ion()
    fig = plt.figure()
    # ax = fig.add_subplot(1,1,1)
    # x = [1,2,3]
    # labels = ['FSR', 'Tilt', 'IR']
    # ax.set_xticklabels(labels)
    # y = [5.0,5.0,5.0]
    # ax.bar(x,y)

    f = fig.add_subplot(221),plt.imshow(frame),plt.title('frame'),plt.xticks([]),plt.yticks([])
    r = fig.add_subplot(222),plt.plot(histr_RED,color='r'),plt.title('Red'), plt.xlim([0,256])
    g = fig.add_subplot(223),plt.plot(histr_GREEN,color='g'), plt.title('Green'),plt.xlim([0,256])
    b = fig.add_subplot(224),plt.plot(histr_BLUE,color='b'), plt.title('Blue'),plt.xlim([0,256])
    #plt.plot()
    plt.show()
    return f,r,g,b

def color_details(frame,f,r,g,b):#histogram update not working
    histr_RED = cv2.calcHist([frame],[0],None,[256],[0,256])
    histr_GREEN = cv2.calcHist([frame],[1],None,[256],[0,256])
    histr_BLUE = cv2.calcHist([frame],[2],None,[256],[0,256])

    #f.imshow(frame)
    r.plot(histr_RED)
    g.plot(histr_GREEN)
    b.plot(histr_BLUE)

    plt.show()





def empty(e):#empty fuction
    pass

def calibration(frame,h,v,s,b,g,r):#calibrate
    blue = np.uint8([[[b,g,r]]])
    hsv_blue = cv2.cvtColor(blue, cv2.COLOR_BGR2HSV)

    half = h
    hue_low = s
    value_low = v
    blue_range = (np.uint8([hsv_blue[0,0,0]-h,s,v]),np.uint8([hsv_blue[0,0,0]+h,255,255]))

    common.find_objects(frame,blue_range,"Calibration")




cam = cv2.VideoCapture(0)
cv2.namedWindow('Adjust')
cv2.createTrackbar('B','Adjust',0,255,empty)
cv2.createTrackbar('G','Adjust',0,255,empty)
cv2.createTrackbar('R','Adjust',0,255,empty)
cv2.createTrackbar('Hue Range','Adjust',0,255,empty)
cv2.createTrackbar('S Low','Adjust',0,255,empty)
cv2.createTrackbar('V Low','Adjust',0,255,empty)

#ret, fr = cam.read()
#f,r,g,b = make_details_windwow(fr)
while True:
    ret, frame = cam.read()

    b = cv2.getTrackbarPos('B','Adjust')
    g = cv2.getTrackbarPos('G','Adjust')
    r = cv2.getTrackbarPos('R','Adjust')
    h = cv2.getTrackbarPos('Hue Range','Adjust')
    s = cv2.getTrackbarPos('S Low','Adjust')
    v = cv2.getTrackbarPos('V Low','Adjust')

    calibration(frame,h,v,s,b,g,r)
    #color_details(frame,f,r,g,b)
    #cv2.imshow('Adjust',frame)


    if cv2.waitKey(1) % 256 == 27:
        break
