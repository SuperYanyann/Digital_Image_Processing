'''
 * Copyright 2018/9/6 Yan Wang.
 *
 * Use to locate and cut the QRcode int the photo
 *
 '''

import cv2
from matplotlib import pyplot as plt
import numpy as np
import math

# find the PositionDetectionPattern of the QRCode
# learn from https://blog.callmewhy.com/2016/04/23/opencv-find-qrcode-position/
def find_PositionDetectionPattern(operating_img):
    # change img into gray
    gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # Gaussian
    gb_img = cv2.GaussianBlur(gray_img,(5,5),0)
    # threshold
    # ! learn from https://blog.csdn.net/kellen_f/article/details/81667315
    # ! cv2.THRESH_OTSU+cv2 :  https://blog.csdn.net/on2way/article/details/46812121
    # ! cv2.THRESH_OTSU+cv2 is helpful
    (T, threshold_img) = cv2.threshold(gb_img, 0, 255, cv2.THRESH_OTSU+cv2.THRESH_BINARY)
    # Canny
    edge_img = cv2.Canny(threshold_img,100,200)

    # ! find Position Detection Pattern
    img_fc, contours, hierarchy = cv2.findContours(edge_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    hierarchy = hierarchy[0]
    found = []
    for i in range(len(contours)):
        k = i
        c = 0
        while hierarchy[k][2] != -1:
            k = hierarchy[k][2]
            c = c + 1
        if c >= 5:
            found.append(i)
    PDP_img = img.copy()
    PDP = []
    for i in found:
        PDP.append(contours[i])
        cv2.drawContours(PDP_img,contours,i,(0,0,255),3)

    return PDP_img,PDP

# get the distance of two points
def get_distance(Point1, Point2):
    return int(math.sqrt(pow((Point1[0] - Point2[0]), 2) + pow((Point1[1] - Point2[1]),2)))

# use PDP to find the TimingPattern of img
# Attention : to continue ...
def find_TimingPattern(img , PDP):
    # find the minimum rectangle bounding box of outline
    box_PDP_img = img.copy()
    boxes = []
    for i in range(3):
        rect = cv2.minAreaRect(PDP[i])
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        box_PDP_img = cv2.drawContours(box_PDP_img,[box],0,(0,255,0),3)
        box = map(tuple, box)
        boxes.append(box)

    return box_PDP_img

# find the Minimum rectangle bounding box of three PositionDetectionPattern
# to determine the location of QRCode
def determine_location_QRcode(img , PDP):
    QRcode_location_img = img.copy()
    all_PDP = []
    for i in range(3):
        temp_PDP = PDP[i]
        for sublist in temp_PDP:
            for point in sublist:
                all_PDP.append(point)

    all_PDP = np.array(all_PDP)
    rect = cv2.minAreaRect(all_PDP)
    box_QR = cv2.boxPoints(rect)
    box_QR = np.array(box_QR)

    cv2.polylines(QRcode_location_img,np.int32([box_QR]),True,(0,255,0),10)

    return QRcode_location_img,box_QR

# Image rotation
# location_QR are the four points in the QRcode's corners
#             and the order is left_down , left_up , right_up, right_down
#             use two point to count the angle which the img should rotate
def rotate_cut_img(img , location_QR):

    after_rotation_img = img.copy()
    angle = 0.00
    (img_high , img_weight) = img.shape[:2]
    scale = 1

    # use four points to count the center of the square
    # the point is the center of rotateion
    point_x_all = 0
    point_y_all = 0
    for i in range(4):
        point_x_all = point_x_all + location_QR[i][0]
        point_y_all = point_y_all + location_QR[i][1]
    center_x = point_x_all / 4
    center_y = point_y_all / 4
    center = (center_x,center_y)

    # count the angle which img should rotate
    left_down_point = location_QR[0]
    right_down_point = location_QR[3]
    angle_tan = (right_down_point[1] - left_down_point[1]) / (right_down_point[0] - left_down_point[0])
    temp_angle = math.atan(angle_tan) * 180 / math.pi
    if (abs(temp_angle - angle) > 0.01):
        angle = temp_angle


    # count the new four points of the QRCode
    temp_weight_all = 0
    temp_weight_all = temp_weight_all + get_distance(location_QR[0],location_QR[3])
    for i in range(3):
        temp_weight_all = temp_weight_all + get_distance(location_QR[i],location_QR[i+1])
    QRcode_weight = temp_weight_all / 4

    '''
    new_location_QR = location_QR
    new_location_QR[0] = [center_x - QRcode_weight/2 , center_y - QRcode_weight/2]
    new_location_QR[1] = [center_x - QRcode_weight/2 , center_y + QRcode_weight/2]
    new_location_QR[2] = [center_x + QRcode_weight/2 , center_y + QRcode_weight/2]
    new_location_QR[3] = [center_x + QRcode_weight/2 , center_y - QRcode_weight/2]
    '''

    # rotate the img
    motion = cv2.getRotationMatrix2D(center, angle, scale)
    after_rotation_img = cv2.warpAffine(img, motion, (img_weight, img_high))
    after_cut_img = after_rotation_img[int(center_y - QRcode_weight/2) : int(center_y + QRcode_weight/2),
                                       int(center_x - QRcode_weight/2) : int(center_x + QRcode_weight/2)]

    return after_cut_img


if __name__ == '__main__':
    img = cv2.imread('Date/test2.jpeg')

    (PDP_img,PDP) = find_PositionDetectionPattern(img)
    #box_PDP_img = find_TimingPattern(img, PDP)
    (QRcode_location_img,box_QRcode) = determine_location_QRcode(img , PDP)
    after_rotation_img  = rotate_cut_img(img , box_QRcode)

    cv2.namedWindow("Image")
    cv2.imshow("Image", QRcode_location_img)
    cv2.namedWindow("Image2")
    cv2.imshow("Image2", after_rotation_img)

    cv2.waitKey (0)
