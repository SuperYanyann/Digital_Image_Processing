'''
 * Copyright 2018/10/30 Yan Wang.
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * Author: Yan Wang <dieqi317@gmail.com>
 * step1: 2018/10/30 data processing
 * step2: 2018/11/08 finish a simple measures classification algorithm
 * step3: 2019/11/09 optimized classification algorithm
 *
 * Attention : if you want to use the code, you should add a "-----..." in first line
 *            I revise "txt" already,you can use mine directly
 '''
import cv2
from matplotlib import pyplot as plt
import numpy as np
import math
from PIL import Image, ImageDraw, ImageFont

# read the file and get the box in each frame
# reture the list of the box
def read_box_location(box_dir):
    src_box_file = open(box_dir,"r")
    lines = src_box_file.readlines()
    box_len = len(lines)
    box_one_frame = []
    box_video = []
    frame_num = 0
    flag = 0

    for line in lines:
        if (line == "-----------------------------------\n"):
            frame_num = frame_num + 1
        else:
            box_one_line = line.split()
            #print box_one_line
            if flag == frame_num:
                box_one_frame.append(box_one_line)
            else:
                flag = flag + 1
                box_video.append(box_one_frame)
                box_one_frame = []

    return box_video

# change the str_num in the box to the float for counting
def str_2_float(box_video):
    len_box = np.shape(box_video)[0]

    for i in range(len_box):
        len_box_each_frame = np.shape(box_video[i])[0]
        for j in range(len_box_each_frame):
            for k in range(4):
                box_video[i][j][k] = float(box_video[i][j][k])

    return box_video

# get the center of box in each frame
# 4 parameter in label : x y w h
def get_box_center(video_capture,box_video):
    len_box = np.shape(box_video)[0]
    video_size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                  int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    box_center_video = []

    for i in range(len_box):
        len_box_each_frame = np.shape(box_video[i])[0]
        box_center_frame = []
        for j in range(len_box_each_frame):
            temp_box_center = (int(box_video[i][j][0] * video_size[0]),
                               int(box_video[i][j][1] * video_size[1]))
            box_center_frame.append(temp_box_center)
        box_center_video.append(box_center_frame)

    return box_center_video

# get the area of box
def get_box_area(box,video_size):
    box_w = box[2] * video_size[0]
    box_h = box[3] * video_size[1]
    box_area = box_w * box_h
    return box_area

# judge whether the two rectangles intersect
def whether_intersect(box1,box2,video_size):
    if (abs(box1[0] - box2[0])) < (box1[2] + box2[2]) and (abs(box1[1] - box2[1])) < (box1[3] + box2[3]):
        flag = 1
    else:
        flag = 0

    return flag

# count the overlapping area between two bounding box
# 4 parameter in box : x y w h
# overlapping_area = w' * h'
#  w' = ((w1 + w2 )/2 - |x1 - x2|) * video_size_width
#  h' = ((h1 + h2 )/2 - |y1 - y2|) * video_size_height
def get_overlapping_area(box1,box2,video_size):
    flag = whether_intersect(box1,box2,video_size)
    if (flag == 1):
        overlapping_w = ((box1[2] + box2[2] )/2 - abs(box1[0] - box2[0])) * video_size[0]
        overlapping_y = ((box1[3] + box2[3] )/2 - abs(box1[1] - box2[1])) * video_size[1]
        overlapping_area = overlapping_w * overlapping_y
    else :
        overlapping_area = -1

    return overlapping_area

# find the corresponding tracker for the measure using "overlapping area"
# the function just finish one measure's work
# one measure is a box in the frame,not all boxes in the frame
# if max_area > minimal_overlapping_area_ratio reture the index of tracker,else reture flag -1
def one_measure_to_tracker(trackers_list,measure,video_size):
    num_tracker = np.shape(trackers_list)[0]
    minimal_overlapping_area_ratio = 0.4
    max_overlapping_area = 0
    tracker_area = 0
    max_overlapping_ratio = 0
    # find the max overlapping_area of the measure
    for tracker_index in range(num_tracker):
        num_box_tracker = np.shape(trackers_list[tracker_index])[0]
        temp_overlapping_area = get_overlapping_area(trackers_list[tracker_index][num_box_tracker -1 ],measure,video_size)
        if temp_overlapping_area > 0:
            if temp_overlapping_area > max_overlapping_area:
                max_overlapping_area = temp_overlapping_area
                max_area_index = tracker_index
                tracker_area = get_box_area(trackers_list[tracker_index][num_box_tracker -1],video_size)
    # get the max ratio
    if (tracker_area != 0 ):
        max_overlapping_ratio = max_overlapping_area / tracker_area
    # judge max_area > "minimal_overlapping_area_ratio" or not
    if max_overlapping_ratio > minimal_overlapping_area_ratio:
        corresponding_tracker = max_area_index
    else:
        corresponding_tracker = -1

    return corresponding_tracker

# find the corresponding tracker for all measure in one frame
# reture the tracker index list
def frame_measure_to_tracker(trackers_list,measure_list,video_size):
    num_measure = np.shape(measure_list)[0]
    corresponding_trackers_list = []

    for i in range(num_measure):
        temp_index = one_measure_to_tracker(trackers_list,measure_list[i],video_size)
        corresponding_trackers_list.append(temp_index)
    return corresponding_trackers_list

# initializate the tracker
def tracker_initialization(box_video):
    num_initializing_box = np.shape(box_video[0])[0]
    box_video_trackers = []

    for i in range(num_initializing_box):
        temp_tracker = []
        temp_tracker.append(box_video[0][i])
        box_video_trackers.append(temp_tracker)
    return box_video_trackers

# add measures one frame to trackers_list
def add_measure_to_trackers(trackers_list,box_video,frame_index,video_size):
    measure_list = box_video[frame_index]
    num_measure_frame = np.shape(measure_list)[0]
    measure_to_tracker_list = frame_measure_to_tracker(trackers_list,measure_list,video_size)
    for measure_index in range(num_measure_frame):
        tracker_index = measure_to_tracker_list[measure_index]
        if (tracker_index == -1):
            temp_tracker = []
            temp_tracker.append(measure_list[measure_index])
            trackers_list.append(temp_tracker)
        else :
            trackers_list[tracker_index].append(measure_list[measure_index])
    return trackers_list

# draw the points in each tracker by different colors
def draw_frame_track(trackers_list,frame,video_size):
    # the list define the color used to draw the points
    # choose the color from tool: http://tool.oschina.net/commons?type=3
    # I choose 16 colors looks different
    track_color_list = [(135,206,255),(0, 255, 0),(119,136,153),(25,25,112),
                        (178,34,34),(218,112,214),(123,104,238),(0,206,209),
                        (132,112,255),(0,191,255),(238,221,130),(188,143,143),
                        (244,164,96),(250,128,114),(255,20,147),(205,96,144)]

    num_tracker = np.shape(trackers_list)[0]
    opearte_frame = frame.copy()

    for tracker_index in range(num_tracker):
        num_points = np.shape(trackers_list[tracker_index])[0]
        for point_index in range(num_points):
            temp_point_x = int(trackers_list[tracker_index][point_index][0] * video_size[0])
            temp_point_y = int(trackers_list[tracker_index][point_index][1] * video_size[1])
            opearte_frame = cv2.circle(opearte_frame, (temp_point_x, temp_point_y), 4,
                                                       track_color_list[tracker_index], -1)

    return opearte_frame

# video operate
# trackers_list : record the boxes in each tracker,use box to show the feature of the tracker
def video_operate(video_capture,output_name,box_video):
    # get the fps and size of video
    video_fps = video_capture.get(cv2.CAP_PROP_FPS)
    video_size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                  int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # point out how to encode videos
    video_writer = cv2.VideoWriter(output_name,cv2.VideoWriter_fourcc(*'XVID'), video_fps, video_size)
    # initializate the tracker
    trackers_list = tracker_initialization(box_video)
    frame_index = 0
    # read frame from video
    success, frame = video_capture.read()
    # operate in each frame
    while success:
        opearte_frame = frame.copy()
        # classify the measures(boxes) and add measures(boxes) in frame to the trackers_list
        trackers_list = add_measure_to_trackers(trackers_list,box_video,frame_index,video_size)
        # draw the points in each tracker
        opearte_frame = draw_frame_track(trackers_list,opearte_frame,video_size)
        # write the photo with mark into the ouput video
        video_writer.write(opearte_frame)

        success, frame = video_capture.read()
        frame_index = frame_index + 1
        print frame_index
        print np.shape(trackers_list)[0]

if __name__ == '__main__':
    # get the path of vedio and box_location
    vedio_dir = "data/test1.mp4"
    box_dir = "data/result_video1.txt"
    output_name = "step2_result1.mp4"

    # read the video
    video_capture = cv2.VideoCapture(vedio_dir)
    # video_operate
    # get the box_list of the video
    box_video = read_box_location(box_dir)
    box_video = str_2_float(box_video)
    # classify measure in each frame to trackers and draw all trackers
    video_operate(video_capture,output_name,box_video)
