import cv2 as cv
import numpy as np
from boardDetectFun import *
from constants import *



def detectBoard(img):
    
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(gray, CANNY_LOWER_THRESHOLD, CANNY_UPPER_THRESHOLD, apertureSize=3)
    coord = detectRedCorners(img)
    cornerPoints = drawExtractedSquare(img, np.array(coord))
    p1,p2,p3,p4 = cornerPoints
    mask = np.zeros_like(img)
    cv.fillPoly(mask,[p1,p2,p3,p4],(255,255,255))
    masked_image = cv.bitwise_and(img, mask)
    # cv.imshow('mask', masked_image)
    
    gray = cv.cvtColor(masked_image, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(masked_image, CANNY_LOWER_LINE_THRESHOLD, CANNY_UPPER_LINE_THRESHOLD, apertureSize=3)
    lines = cv.HoughLines(edges, HOUGH_RHO, HOUGH_THETA, HOUGH_THRESHOLD)
    h_lines, v_lines = h_v_lines(lines)


    intersection_points = line_intersections(h_lines, v_lines)
    points = cluster_points(intersection_points)
    
    drawPoints(img,points)
    # center = (int(img.shape[1]/2), int(img.shape[0]/2))
    # newPoints = removeClosePoints(points, center, threshold=5)
    # drawPoints(img,newPoints,color = (0,0,255))
    # print(len(newPoints))
    print(f"Number of Detected points : ${len(points)}")

    if (len(points) == PERFECT_POINTS):
        print('It seems like a good fit!!')
        allRows = organizeSave(points)
        print('Saved to points.txt')
        print(len(allRows))
        
    else:
        print('try to position the board differently')
        cv.imshow('canny', edges)
        cv.imshow('image', img)
        cv.waitKey()
        

