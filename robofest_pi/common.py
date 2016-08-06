import cv2
import math


def get_gradient(x1, y1, x2, y2):
    return (y2 - y1) / float(x2 - x1)


def get_distance(x1, y1, x2, y2):
    return math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))


def get_normal_threshold(gray_img, min_val=70, max_val=255, thresh_type=cv2.THRESH_BINARY):
    returned = False
    while not returned:
        returned, threshold_img = cv2.threshold(gray_img, min_val, max_val, thresh_type)
    return threshold_img


def get_otsu_threshold(gray_img):
    returned = False
    while not returned:
        returned, threshold_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return threshold_img


def get_otsu_gaussian_threshold(gray_img, width=3, height=3):
    blurred = cv2.GaussianBlur(gray_img, (width, height), 0)
    returned = False
    while not returned:
        returned, threshold_img = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return threshold_img


def get_contours(img):
    _, contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

