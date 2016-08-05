import cv2
import sys
## Import AndroidCamFeed module
from AndroidCamFeed import AndroidCamFeed

def main():


    ## Set host
    host = '192.168.1.4:8080'
    cv2.namedWindow('feed', cv2.WINDOW_NORMAL)

    ## Create new AndroidCamFeed instance
    acf = AndroidCamFeed(host)

    ## While camera is open
    while acf.isOpened():
        ## Read frame
        ret, frame = acf.read()
        if ret:
            cv2.imshow('feed', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    ## Must Release ACF instance
    acf.release()
    cv2.destroyAllWindows()
    return

if __name__ == '__main__':
    main()
