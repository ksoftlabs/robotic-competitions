import cv2
import numpy as np
import sys
import common

########### THIS PART IS BASIC FUNCTIONS, PREFFERED NOT TO BE CAHNGED , find below box and arrow detection methods########################################################################
def filter_color(frame, color, window_name):#color range as a tuple
    hsv_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    image_mask = 0#np.zeros((frame.shape[0],frame.shape[1]))
    for c in color:
        mask=cv2.inRange(hsv_frame,c[0],c[1])
        image_mask = image_mask + mask


    rframe=cv2.bitwise_and(frame,frame,mask=image_mask)
    #cv2.imshow("Mask "+ window_name,image_mask)
    #cv2.imshow("Color Filter "+ window_name, rframe)
    rframe = cv2.cvtColor(rframe, cv2.COLOR_BGR2GRAY)
    return rframe

def thresholding(frame):
    blurred= cv2.GaussianBlur(frame, (5, 5), 0)
    ret, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #thresh = cv2.threshold(blurred, 255, cv2.THRESH_BINARY+cv2)[1]#without OTSU methode
    return thresh

def find_polygons(frame):
    _, contours, _  = cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    poly = []
    for c in contours :
        peri = cv2.arcLength(c, True)
        poly.append(cv2.approxPolyDP(c, 0.02 * peri, True))
    return poly

def find_objects(frame, color, window_name):
    filtered = filter_color(frame ,color, window_name)
    thresholded = thresholding(filtered)
    polys = find_polygons(thresholded)
    arrows, rectangles = draw_shapes(thresholded, polys, window_name)
    return arrows, rectangles

##############################################################################################################################################



############### shape detections method calls arrow detection method & box detection method #################
def draw_shapes(frame, contours, window_name):
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    rectangles = []
    arrows = []
    for c in contours:
    ########## calls box detections method #########
        if len(c)==4:
            r = draw_box(c,frame)
            rectangles.append(r)
    ######### calls arrow detections methode ########
        elif len(c)==7:
            a = draw_traingles(c,frame)
            arrows.append(a)

    cv2.imshow("Contors "+window_name, frame)
    return arrows, rectangles



#### Box detection method #############
def draw_box(c,frame):
    r = cv2.boundingRect(c)
    cv2.rectangle(frame, (r[0],r[1]), (r[2],r[3]), (0,255,0), thickness=1)
    return r



#### Oshan's Arrow detections method ################################################################
def draw_traingles(approx,frame):
    #print '___________________________________________________________________________________________________'
    for c in approx:
        sys.stdout.write(str(c) + '     ')
    #print ' '

    for i in range(7):
        xi0 = approx[i][0][0]
        yi0 = approx[i][0][1]
        xi1 = approx[(i + 1) % 6][0][0]
        yi1 = approx[(i + 1) % 6][0][1]
        xi2 = approx[(i + 2) % 6][0][0]
        yi2 = approx[(i + 2) % 6][0][1]
        xi3 = approx[(i + 3) % 6][0][0]
        yi3 = approx[(i + 3) % 6][0][1]
        if i == 0:
            xin2 = approx[5][0][0]
            yin2 = approx[5][0][1]
        elif i == 1:
            xin2 = approx[6][0][0]
            yin2 = approx[6][0][1]
        else:
            xin2 = approx[i - 2][0][0]
            yin2 = approx[i - 2][0][1]

        m1 = common.find_gradient(xi0, yi0, xi1, yi1)
        m2 = common.find_gradient(xi2, yi2, xi3, yi3)

        diff = abs(m1 - m2)
        if -0.1 <= diff <= 0.1:
            xmid = (xi1 + xi2) / 2
            ymid = (yi1 + yi2) / 2

            cv2.circle(frame, (xi0, yi0), 4, (0, 255, 0), 2)
            cv2.line(frame, (xmid, ymid), (xin2, yin2), (0, 255, 0), 2)
            cv2.line(frame, (xi0, yi0), (xi1, yi1), (255, 255, 255), 2)
            cv2.line(frame, (xi2, yi2), (xi3, yi3), (255, 255, 255), 2)

            cv2.putText(frame, str(i), (xi0 + 10, yi0 + 10),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (255, 255, 255))
            cv2.putText(frame, str(i + 1), (xi1 + 10, yi1 + 10),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (255, 255, 255))
            cv2.putText(frame, str(i + 2), (xi2 + 10, yi2 + 10),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (255, 255, 255))
            cv2.putText(frame, str(i + 3), (xi3 + 10, yi3 + 10),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (255, 255, 255))
            cv2.putText(frame, str('HEAD'), (xin2 + 10, yin2 + 10),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (255, 255, 255))
            cv2.putText(frame, str('BASE'), (xmid + 10, ymid + 10),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (255, 255, 255))

            #print str(xi1) + ',' + str(xi2) + ',' + str(xmid) + '       ' + str(yi1) + ',' + str(yi2) + ',' + str(ymid)
            return (xi1,xi2,xmid,yi1,yi2,ymid)
