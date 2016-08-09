
def detect_box(frame,right,left,top,bottom):
    lower_red_range = (np.array([0, 50, 50]), np.array([10, 255, 255]))
    upper_red_range = (np.array([170, 50, 50]), np.array([180, 255, 255]))
    blue_range = (np.array([80, 50, 50]), np.array([160, 255, 255]))
    green_range = (np.array([160, 50, 50]) , np.array([260, 255, 255]))

    crop_frame(frame,right,left,top,bottom)
    arrows, rectangles = cmn.find_objects(frame, [lower_red_range,upper_red_range,blue_range,green_range], "Omini color box")

def crop_frame(frame,right,left,top,bottomm):
    
