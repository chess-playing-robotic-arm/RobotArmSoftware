import numpy as np

import cv2 as cv
from boardDetectFun import readPoints, drawOrderedPoints

from detectBoard import detectBoard


def useFileImage(path):
    img = cv.imread(path)
    # print(img.shape)
    img = cv.resize(img,(1028,768))
    return img

def setup():
    setup = True
    # camera_id="/dev/video1"
    # cap = cv.VideoCapture(camera_id, cv.CAP_V4L2)
    # ret, img = cap.read()
    img = useFileImage('./input/05.jpg')
    
    # cap = cv.VideoCapture(1)
    font = cv.FONT_HERSHEY_SIMPLEX
    org = (50, 50)
    fontScale = 2
    color = (255, 0, 0)
    thickness = 2
    # print('Press S to setup')

    while setup:

        # points = readPoints()
           

        # ret, img = cap.read()
       
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        edges = cv.Canny(gray, 100, 200, apertureSize=3)
        # cv.imshow('img', img)
        # drawOrderedPoints(img,points)
        cv.imshow('img', img)
        cv.imshow('canny',edges)
        keyCode = cv.waitKey(10) & 0xFF
        if keyCode == ord('q'):
            print('quitting')
            # cap.release()
            break
        elif keyCode == ord('s'):
            # cv.imwrite('output/test.jpg',img)
            detectBoard(img)
            # print('Trying')
            print('Try again ? (y/n)')
            choice = input()
            if choice == 'y':
                setup = True
            else:
                setup = False
       
           

    # cap.release()
    cv.destroyAllWindows()


setup()
