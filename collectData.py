from boardDetectFun import crop, drawOrderedPoints, readPoints, writeOutSquares
import numpy as np
from square import Square
import cv2 as cv



def main():
  
    cap = cv.VideoCapture(1)
    _, img = cap.read()
   
    setup = True
    boardimg = []
    boardrow = []

    boardimg = []
    boardrow = []
    index = 0

    points = readPoints()

    for i in range(9):
        points[i] = sorted(points[i], reverse=True)

    squareid = 64

    for i in range(8):
        for j in range(8):
            p1 = points[i][j]
            p2 = points[i][j+1]
            p3 = points[i+1][j]
            p4 = points[i+1][j+1]
            square = Square(p1=p1, p2=p2, p3=p3, p4=p4, position=squareid)
            squareid -= 1
            boardrow.append(square)
        boardimg.append(boardrow)
        boardrow = []

    boardimg = np.transpose(boardimg)
    boardimg = np.flip(boardimg, 1)
    boardimg = np.flip(boardimg, 0)

    squareid = 1
    for i in range(8):
        for j in range(8):
            boardimg[i][j].position = squareid
            squareid += 1

    index = 320
    while setup:
        print('setup started !!')
        sqRow = []
        sqs = []
        for i in range(8):
            for j in range(8):
                sq = crop(img, boardimg[i][j])
                sqRow.append(sq)
            sqs.append(sqRow)
            sqRow = []

        # cv.imshow('image',img)
        # keyCode = cv.waitKey(50) & 0xFF
        print('make your choice : ')
        userInput  = input()
        if(userInput == 'q'):
            print('quitting')
            cap.release()
            break
        elif(userInput == 's'):
            print('s is pressed ')
            writeOutSquares(sqs,'./raw/',index=index)
            print('continue ? (y/n)')
            choice = input()
            if choice == 'y':
                _, img = cap.read()
                index += 64
                setup = True

            else:
                setup = False

                break

    cv.waitKey(0)
    cv.destroyAllWindows()



main()
