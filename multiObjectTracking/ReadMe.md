# Multi-Object Tracking
Author:Yan Wang  <dieqi317@gmail.com> <br>
Date: 2018 11 09 <br>

## Introduction
The program is used to find the tracks of multi-object, then draw all trackers in different colors. <br>
Pay attention, I and my teammate use [yolo](https://pjreddie.com/darknet/yolo/) to get the boundingbox of passerby and output the txt to record the data of boundingbox in each frame of the video.Then use the txt to classify the measures and draw the trackers. <br>

## Method
The steps to achieve Multi-Object Tracking are:

- read the file and get the box in each frame
- initializate the tracker
- find the corresponding tracker for one measure using "overlapping area"
- find the corresponding tracker for all measure in one frame
- loop all frame in the video
- draw the points in each tracker by different colors

## Result
The output of the code is a video,because the result is dynamic.I just intercept one frame to show. <br>

### test1
![test1](http://p33eqsoxi.bkt.clouddn.com/video1_result1.png)  <br>

### test2
![test2](http://p33eqsoxi.bkt.clouddn.com/video1_result2.png)  <br>

### test3
![test3](http://p33eqsoxi.bkt.clouddn.com/video1_result3.png)  <br>
