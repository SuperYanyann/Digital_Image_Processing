'''
 * Copyright 2018/9/22 Yan Wang.
 *
 * cut the Yellow Mark in the photo
 *
 '''

import cv2
from matplotlib import pyplot as plt
import numpy as np
import math

def findYellowMark(img):
    # Set the upper and lower bounds in HSV
    lower = np.array([26, 160, 20])
    upper = np.array([34, 255, 255])

    # change the photo to hsv model
    img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # use upper and lower to locate the yellow in the photo
    img_mask = cv2.inRange(img_HSV, lower, upper)
    # threshold
    (T, threshold_img) = cv2.threshold(img_mask, 0, 255, cv2.THRESH_OTSU+cv2.THRESH_BINARY)
    # edge detection by Canny
    edge_img = cv2.Canny(threshold_img,100,200)
    # get the contours and the hierarchy of contours
    img_fc, contours, hierarchy = cv2.findContours(edge_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # use the nested models to locate the yellow mark
    hierarchy = hierarchy[0]
    found = []
    for i in range(len(contours)):
        k = i
        c = 0
        while hierarchy[k][2] != -1:
            k = hierarchy[k][2]
            c = c + 1
        if c >= 2:
            found.append(i)
    img_mark = img.copy()
    mark_edge = []
    for i in found:
        # record the edge of yellow mark
        mark_edge.append(contours[i])
        # put the mark_edge into the original img
        cv2.drawContours(img_mark,contours,i,(0,0,255),3)

    return img_mark

if __name__ == '__main__':
    img = cv2.imread('data/test5.png')

    img_mark = findYellowMark(img)

    cv2.namedWindow("Image")
    cv2.imshow("Image", img)
    cv2.namedWindow("Image2")
    cv2.imshow("Image2", img_mark)

    cv2.waitKey (0)
