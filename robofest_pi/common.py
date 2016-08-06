import math


def find_gradient(x1, y1, x2, y2):
    return (y2 - y1) / float(x2 - x1)


def find_distance(x1, y1, x2, y2):
    return math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))
