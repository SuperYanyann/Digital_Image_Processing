# Pedestrian Detection
Author:Yan Wang  <dieqi317@gmail.com> <br>
Date: 2018 10 22 <br>
## Introduction
The program is used to realize 3D reconstruction <br>
Using calibration board to get camera parameters, then rebuild the object.

## Method
The steps to achieve 3D reconstruction are

- take some photo of object in different angles
- get the binary_img of these photo
- get "cameraParams" by "camera calibration",an APP in matlab
- load imgs and read the info of them
- orthodontic distortion
- build a cuboid surround the cuboid
- judge the point whether in the cuboid,if the point is not in one picture,the point is eliminated
- get the point of existence
- show the points of existence

## Details
I use Matlab to realize the function,if you want to test the code,you shoule pay attention to the path of img.
"get_gray_img.m" is used to get the binary_img of the src_img.<br>
"reconstruction_3D.m" is used to realize 3D reconstruction and show the result.<br>
You can see more detalls in [SuperYanyann's Blog](https://superyanyann.github.io/2018/10/22/Project-Reconstruction-3D/#more)

## Result
The corresponding points in each picture:<br>
![photo1](http://p33eqsoxi.bkt.clouddn.com/image/tif/3d/test/output1.JPG)<br>
The object we plan to rebuild:<br>
![photo1](http://p33eqsoxi.bkt.clouddn.com/image/tif/3d/test/output2.JPG)
