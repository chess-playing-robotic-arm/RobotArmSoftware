import numpy as np
import cv2 as cv
from boardDetectFun import detectRedCorners, drawExtractedSquare, drawPoints, readPoints, drawOrderedPoints
from detectBoard import detectBoard
import argparse

# * constants
CANNY_LOWER_THRESHOLD = 100
CANNY_UPPER_THRESHOLD = 200
IMAGE_SIZE = (1028,768)


# Create a new parser
parser = argparse.ArgumentParser(description='Detecting the chess board')

# Add options and arguments to the parser
parser.add_argument('-m', '--mode', help='Select the mode (setup(s) - marking dots(m))', required=True)
parser.add_argument('-o', '--os', help='Select OS (w-m-l)', required=True)
parser.add_argument('-i', '--input', help='Path to input file', required=False)

# Parse the command-line arguments
args = parser.parse_args()

# Access the values of the options and arguments
#* get images from the files 
def useFileImage(path):
    img = cv.imread(path)
    img = cv.resize(img,IMAGE_SIZE)
    return img

def useCamera():
    if(args.os == "w"):
        cap = cv.VideoCapture(1)
    elif(args.os == "m"):
        cap = cv.VideoCapture('http://192.168.1.10:8080/video')
    else:
        camera_id="/dev/video1"
        cap = cv.VideoCapture(camera_id, cv.CAP_V4L2)
        
    return cap

def setup():
    setup = True


    # * chose how to obtain the image 
    if(args.input == None):
        cap = useCamera()
    else:
        img = useFileImage(args.input)

    
    if(args.mode == 's'):
        print('Setup mode is Selected')
        print('Press S to setup')
    else:
        print('Selected mode is Showing the points') 

    while setup:
        _, img = cap.read()
        # img = cv.resize(img,(1080,720))
        if(args.mode == 's'):
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            edges = cv.Canny(gray, CANNY_LOWER_THRESHOLD, CANNY_LOWER_THRESHOLD, apertureSize=3)
            coord = detectRedCorners(img)
            cornerPoints = drawExtractedSquare(img, np.array(coord))
            # p1,p2,p3,p4 = cornerPoints.points
            drawPoints(img,cornerPoints.points)
            cv.imshow('img', img)
            cv.imshow('canny',edges)

        else:
            
            points = readPoints()
            drawOrderedPoints(img,points)
            cv.imshow('img', img)
            
        keyCode = cv.waitKey(10) & 0xFF
        if keyCode == ord('q'):
            print('Quitting')
            break
        elif keyCode == ord('s'):
            detectBoard(img)
            print('Try again ? (y/n)')
            choice = input()
            if choice == 'y':
                setup = True
            else:
                setup = False
    cap.release()
    cv.destroyAllWindows()


setup()
