import cv2

def filter_color(frame, color, window_name):#color range as a tuple
    hsv_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    image_mask=cv2.inRange(hsv_frame,color[0],color[1])
    rframe=cv2.bitwise_and(hsv_frame,frame,hsv_frame,mask=image_mask)
    cv2.imshow("Color Filter "+ window_name, rframe)
    rframe = cv2.cvtColor(rframe, cv2.COLOR_BGR2GRAY)
    return rframe

def thresholding(frame):
    blurred= cv2.GaussianBlur(frame, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    #thresh = cv2.threshold(blurred, 255, cv2.THRESH_BINARY+cv2)[1]#without OTSU methode
    return thresh

def find_contours(frame):
    contours = cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def draw_contours(frame, contours, window_name):
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    #contour_details = contours[-1]
    contours = contours[:-1]
    for c in contours:
        cv2.drawContours(frame, c, -1, (255, 0, 0), 2)

    cv2.imshow("Contors "+window_name, frame)

def find_objects(frame, color, window_name):
    filtered = filter_color(frame ,color, window_name)
    thresholded = thresholding(filtered)
    contours = find_contours(thresholded)
    draw_contours(thresholded, contours, window_name)
    return contours
