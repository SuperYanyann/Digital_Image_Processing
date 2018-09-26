import cv2
from matplotlib import pyplot as plt
import numpy as np

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
    for i in found:
        cv2.drawContours(PDP_img,contours,i,(0,0,255),3)

    return PDP_img


if __name__ == '__main__':
    img = cv2.imread('Date/test.png')
    PDP_img = find_PositionDetectionPattern(img)

    cv2.namedWindow("Image")
    cv2.imshow("Image", PDP_img)
    '''
    cv2.namedWindow("Image2")
    cv2.imshow("Image2", edge_img)
    cv2.namedWindow("Image3")
    cv2.imshow("Image3", threshold_img)
    '''
    cv2.waitKey (0)
