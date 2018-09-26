'''
 * Copyright 2018/9/22 Yan Wang.
 *
 * cut the Yellow Mark in the video
 *
 '''

import cv2
from matplotlib import pyplot as plt
import numpy as np
import math

def find_yellow_mark(img):
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

def video_operate(video_location,output_name):
    video_capture = cv2.VideoCapture(video_location)
    # get the fps and size of video
    video_fps = video_capture.get(cv2.CAP_PROP_FPS)
    video_size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                  int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # point out how to encode videos
    video_writer = cv2.VideoWriter(output_name,cv2.VideoWriter_fourcc(*'XVID'), video_fps, video_size)
    # read frame from video
    success, frame = video_capture.read()
    while success:
        opearte_frame = frame.copy()
        # find the yellow mark of the photo
        frame_mark = find_yellow_mark(opearte_frame)
        # write the photo with mark into the ouput video
        video_writer.write(frame_mark)
        success, frame = video_capture.read()

if __name__ == '__main__':
    # write the location of the aim video
    video_location = 'data/data1.avi'
    # write the name of the output video
    output_name = 'output1.avi'
    # operate the video
    video_operate(video_location,output_name)

    cv2.waitKey (0)
