'''
 * Copyright 2018/9/27 Yan Wang.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * Author: <dieqi317@gmail.com>
 *
 '''

import cv2
from matplotlib import pyplot as plt
import numpy as np
import math

# remove the noise
def noise_removal(frame):
    kernel = np.ones((3,3),np.uint8)
    # in test 1 and 2: erode 4 times (because the people is black, we shoule use dilate )
    # in test 3 and 4: erode 2
    img_erode = cv2.dilate(frame,kernel,iterations = 2)
    # in test 1 and 2: dilate 2 times (because the people is black, we shoule use erode )
    # in test 3 and 4: dilate 1
    img_erosion = cv2.erode(img_erode,kernel,iterations = 1)

    return img_erosion

# "img opening" useing function in opencv
def img_open(frame):
    kernel = np.ones((3,3),np.uint8)
    img_opening = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel)

    return img_opening

# some simlpe operate for each frame before finding people in it
def simple_operate(img):
    # change img into gray
    gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # Gaussian
    gb_img = cv2.GaussianBlur(gray_img,(7,7),0)
    # threshold
    (T, threshold_img) = cv2.threshold(gb_img, 0, 255, cv2.THRESH_OTSU+cv2.THRESH_BINARY)
    # Canny
    edge_img = cv2.Canny(threshold_img,100,200)

    return threshold_img

# use background to find the people in the picture
def find_people(gray_1,gray_2):
    img_size = gray_1.shape
    img_result = gray_1[:]
    # use a threshold value to judge whether the pixel is in "people" or not
    for i in range (0,img_size[0]):
        for j in range(0,img_size[1]):
            if (abs(gray_1[i][j] - gray_2[i][j]) > 10):
                img_result[i][j] = 123
    # change the gray img to RGB for writing into the video
    img_result_RGB = cv2.cvtColor(img_result, cv2.COLOR_GRAY2BGR)
    print img_result_RGB.shape
    return img_result_RGB


if __name__ == '__main__':
    img = cv2.imread('data/test_gray_1.png')
    # operate the video removing the noise
    img_erode = noise_removal(img)
    # img opening
    img_opening = img_open(img)
    # display the picture
    cv2.namedWindow("Image")
    cv2.imshow("Image", img)
    cv2.namedWindow("Image2")
    cv2.imshow("Image2", img_erode)
    cv2.namedWindow("Image3")
    cv2.imshow("Image3", img_opening)

    cv2.waitKey (0)
