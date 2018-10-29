'''
 * Copyright 2018/10/23 Yan Wang.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * Author: Yan Wang <dieqi317@gmail.com>
 *
 '''

import cv2
from matplotlib import pyplot as plt
import numpy as np
import math

# histogram equalization in RGB
def equalize_histogram(img):
    (ch_b, ch_g, ch_r) = cv2.split(img)
    ch_bH = cv2.equalizeHist(ch_b)
    ch_gH = cv2.equalizeHist(ch_g)
    ch_rH = cv2.equalizeHist(ch_r)
    img_equal = cv2.merge((ch_bH, ch_gH, ch_rH))
    return img_equal

# draw match between two img
def draw_matches(img1,kps_img1,img2,kps_img2,matches):
    # get shape of img
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    vis = np.zeros((max(h1, h2), w1 + w2, 3), np.uint8)
    # add two img
    vis[:h1, :w1] = img1
    vis[:h2, w1:w1 + w2] = img2
    # get the match point in two img
    p1 = [kpp.queryIdx for kpp in matches]
    p2 = [kpp.trainIdx for kpp in matches]
    post1 = np.int32([kps_img1[pp].pt for pp in p1])
    post2 = np.int32([kps_img2[pp].pt for pp in p2]) + (w1, 0)
    # draw the line
    for (x1, y1), (x2, y2) in zip(post1, post2):
        cv2.line(vis, (x1, y1), (x2, y2), (0,0,255))
    # show the matches
    cv2.imwrite("match.jpg",vis)
    cv2.namedWindow("match",cv2.WINDOW_NORMAL)
    cv2.imshow("match", vis)


# find homography by SIFT
def get_homography(img1,img2):
    # initialize SIFT
    sift = cv2.xfeatures2d.SIFT_create()

    # find keypoints
    (kps_img1,features_img1) = sift.detectAndCompute(img1,None)
    (kps_img2,features_img2) = sift.detectAndCompute(img2,None)

    # feature matching
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(features_img1,features_img2,k=2)

    #use distance to judge whether match can Use
    verified_matches = []
    for loop1,loop2 in matches:
        # add to array only if it's a good match
        if loop1.distance < 0.5 * loop2.distance:
            verified_matches.append(loop1)

    draw_matches(img1,kps_img1,img2,kps_img2,verified_matches)

    img1_pts = []
    img2_pts = []

    # add matching points to transform_array
    for match in verified_matches:
        img1_pts.append(kps_img1[match.queryIdx].pt)
        img2_pts.append(kps_img2[match.trainIdx].pt)
    img1_pts = np.float32(img1_pts).reshape(-1,1,2)
    img2_pts = np.float32(img2_pts).reshape(-1,1,2)

    # get homography matrix
    homography_M,mask = cv2.findHomography(img1_pts,img2_pts,cv2.RANSAC,5.0)

    return homography_M

# use the keypoints to stitch the images
# learn the foundation in https://github.com/pavanpn/Image-Stitching
def stitch_image(img2,img1,homography_M):
    # get width and height of input images
    img1_w,img1_h = img1.shape[:2]
    img2_w,img2_h = img2.shape[:2]

    # get the canvas dimesions
    img1_dims = np.float32([[0,0],[0,img1_w],[img1_h,img1_w],[img1_h,0]]).reshape(-1,1,2)
    src_img2_dims = np.float32([[0,0],[0,img2_w],[img2_h,img2_w],[img2_h,0]]).reshape(-1,1,2)

    # get relative perspective of second image
    img2_dims = cv2.perspectiveTransform(src_img2_dims,homography_M)

    # resulting dimensions
    result_dims = np.concatenate((img1_dims,img2_dims),axis = 0)

    # Calculate dimesions of match points
    [x_min,y_min] = np.int32(result_dims.min(axis=0).ravel() - 1)
    [x_max,y_max] = np.int32(result_dims.max(axis=0).ravel() + 1)

    # Create output array after affine transformation
    transform_dist = [-x_min,-y_min]
    transform_array = np.array([[1,0,transform_dist[0]],
                                [0,1,transform_dist[1]],
                                [0,0,1]])

    # warp images to get the resulting image
    result_img = cv2.warpPerspective(img2,transform_array.dot(M),
                                    (x_max - x_min, y_max - y_min))
    result_img[transform_dist[1]:img1_w + transform_dist[1],
               transform_dist[0]:img1_h + transform_dist[0]] = img1

    return result_img

if __name__ == '__main__':
    # get the path of img
    img1_path = "data/test1.jpeg"
    img2_path = "data/test2.jpeg"
    output_name = "result.jpg"

    # read the aim img
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    # equalize histogram
    img1_equal = equalize_histogram(img1)
    img2_equal = equalize_histogram(img2)

    # use SIFT and knnMatch to get  homography
    M = get_homography(img1_equal,img2_equal)

    # stitch image
    result_image = stitch_image(img1_equal,img2_equal,M)

    # write the result to the output
    cv2.imwrite(output_name,result_image)

    # show the result image
    cv2.imshow('result_img',result_image)
    cv2.waitKey()
