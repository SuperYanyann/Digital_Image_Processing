# Images Stitching
Author:Yan Wang  <dieqi317@gmail.com> <br>
Date: 2018 10 29 <br>

## Introduction
The program is used to stitch two images, then draw the lines between same features in two images. <br>
Using SIFT to find the homography,using knnMatch to implement feature matching.

## Method
The steps to achieve images stitching  are:

- read two images
- equalize histogram in RGB
- find keypoints in each image by SIFT
- feature matching
- use distance to find the good matches
- draw good match between two img
- warp perspective to stitch images

## Result
### test1
matches:<br>
![photo1](http://p33eqsoxi.bkt.clouddn.com/image/stitch_Images/match6.jpg) <br>
result: <br>
![photo2](http://p33eqsoxi.bkt.clouddn.com/image/stitch_Images/result6.jpg) <br>

### test2
matches:<br>
![photo3](http://p33eqsoxi.bkt.clouddn.com/image/stitch_Images/match2.jpg) <br>
result: <br>
![photo4](http://p33eqsoxi.bkt.clouddn.com/image/stitch_Images/result2.jpg) <br>
