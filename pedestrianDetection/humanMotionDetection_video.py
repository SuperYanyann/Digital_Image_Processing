'''
 * Copyright 2018/10/11 Yan Wang.
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

# some simlpe operate for each frame before finding people in it
def simlpe_operate(img):
    # change img into gray
    gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # Gaussian
    gb_img = cv2.GaussianBlur(gray_img,(5,5),0)
    # threshold
    (T, threshold_img) = cv2.threshold(gb_img, 0, 255, cv2.THRESH_OTSU+cv2.THRESH_BINARY)
    # Canny
    edge_img = cv2.Canny(threshold_img,100,200)

    return threshold_img

# use background to find the people in the picture
def find_people(gray_0,gray_1):
    img_size = gray_1.shape
    img_result = gray_1[:]
    # use a threshold value to judge whether the pixel is in "people" or not
    for i in range (0,img_size[0]):
        for j in range(0,img_size[1]):
            if (abs(gray_0[i][j] - gray_1[i][j]) > 50):
                img_result[i][j] = 0
            else:
                img_result[i][j] = 255
    # change the gray img to RGB for writing into the video
    img_result_RGB = cv2.cvtColor(img_result, cv2.COLOR_GRAY2BGR)

    return img_result_RGB

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

# find the background used to find the people
def getBackGround(video_location):
    video_capture = cv2.VideoCapture(video_location)
    # read frame from video
    success, frame = video_capture.read()
    standard_ground = frame
    standard_ground_temp = standard_ground.copy()
    threshold_standard_ground = simlpe_operate(standard_ground_temp)
    i = 0
    while success:
        i = i + 1
        print i
        opearte_frame = frame.copy()
        # find the yellow mark of the photo
        threshold_frame = simlpe_operate(opearte_frame)
        # update the Background by adding the new photo
        threshold_standard_ground = threshold_standard_ground*0.9 + threshold_frame*0.1
        # read  new frame
        success, frame = video_capture.read()

    threshold_standard_ground = threshold_standard_ground/i
    return threshold_frame



def video_operate(video_location,video_location_2,output_name):
    video_capture = cv2.VideoCapture(video_location)
    # get the fps and size of video
    video_fps = video_capture.get(cv2.CAP_PROP_FPS)
    video_size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                  int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # point out how to encode videos
    video_writer = cv2.VideoWriter(output_name,cv2.VideoWriter_fourcc(*'XVID'), video_fps, video_size)
    # read frame from video
    success, frame = video_capture.read()
    threshold_standard_ground = getBackGround(video_location_2)
    i = 0
    while success:
        i = i + 1
        print i
        opearte_frame = frame.copy()

        # find the yellow mark of the photo
        threshold_frame = simlpe_operate(opearte_frame)
        # find the people
        frame_mark = find_people(threshold_standard_ground,threshold_frame)
        # remove the noise
        frame_no_noise = noise_removal(frame_mark)
        # write the photo with mark into the ouput video
        video_writer.write(frame_no_noise)

        success, frame = video_capture.read()

if __name__ == '__main__':
    # input the location of test video
    # the second is used to get the background
    video_location = 'data/test4.mp4'
    video_location_bg = 'data/test4.mp4'
    # input the name of output video
    output_name = 'output4.avi'
    # operate the video
    video_operate(video_location,video_location_bg,output_name)

    cv2.waitKey (0)
