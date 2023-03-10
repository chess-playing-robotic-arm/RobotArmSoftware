from boardDetectFun import crop, readPoints, writeOutSquares
import numpy as np
from square import Square
import cv2 as cv



def main():
  
    cap = cv.VideoCapture(0)
    _, img = cap.read()
   
    setup = True
    board_img = []
    board_row = []



    points = readPoints()

    for i in range(9):
        points[i] = sorted(points[i], reverse=True)

    square_id = 64

    for i in range(8):
        for j in range(8):
            p1 = points[i][j]
            p2 = points[i][j+1]
            p3 = points[i+1][j]
            p4 = points[i+1][j+1]
            square = Square(p1=p1, p2=p2, p3=p3, p4=p4, position=square_id)
            square_id -= 1
            board_row.append(square)
        board_img.append(board_row)
        board_row = []

    board_img = np.transpose(board_img)
    board_img = np.flip(board_img, 1)
    board_img = np.flip(board_img, 0)

    square_id = 1
    for i in range(8):
        for j in range(8):
            board_img[i][j].position = square_id
            square_id += 1

    index = 23168
    while setup:
        print('setup started !!')
        sqRow = []
        sqs = []
        for i in range(8):
            for j in range(8):
                sq = crop(img, board_img[i][j])
                sqRow.append(sq)
            sqs.append(sqRow)
            sqRow = []

        print('s is pressed ')
        writeOutSquares(sqs,'./raw/',index=index)
        print('continue ? (y/n)')
        choice = input()
        if choice == 'n':
            setup = False

            break


        else:
            _, img = cap.read()
            index += 64
            setup = True

    cv.waitKey(0)
    cv.destroyAllWindows()



main()
