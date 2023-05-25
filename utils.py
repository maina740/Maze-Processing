import math
import cv2 as cv
import numpy as np


# return Euclidean distance between the points passed as parameters
def euclidean_distance(point1, point2):
    (x1, y1) = (point1[1], point1[0])
    (x2, y2) = (point2[1], point2[0])

    # print(x1, y1, x2, y2)
    return int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))


# returns average of rgb values
def get_average(pixel):
    return (int(pixel[0]) + int(pixel[1]) + int(pixel[2])) // 3


def bound(lower_bound, n, upper_bound):
    return min(upper_bound, max(lower_bound, n))
