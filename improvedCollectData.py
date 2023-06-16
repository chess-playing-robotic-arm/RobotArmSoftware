import cv2 as cv
import numpy as np
from square import Square
from boardDetectFun import crop, readPoints, writeOutSquares
from utils.image_comparator import mse
import pandas as pd
import openpyxl

ROWS = 8
COLS = 8

def main():
    cap = cv.VideoCapture(1)
    _, img = cap.read()

    is_setup = True
    board_img = []

    points = readPoints()

    workbook = openpyxl.load_workbook('data.xlsx')

    # Select the sheet to append data to
    sheet = workbook.active

    for i in range(ROWS +1):
        points[i] = sorted(points[i], reverse=True)

    square_id = 64

    board_img = [
        [
            Square(
                p1=points[i][j],
                p2=points[i][j+1],
                p3=points[i+1][j],
                p4=points[i+1][j+1],
                position=square_id
            )
            for j in range(COLS)
        ]
        for i in range(ROWS)
    ]

    board_img = np.transpose(board_img)
    board_img = np.flip(board_img, 1)
    board_img = np.flip(board_img, 0)

    square_id = 1
    for i in range(ROWS):
        for j in range(COLS):
            board_img[i][j].position = square_id
            square_id += 1

    index = 129
    prev_img = img.copy()
    while is_setup:
        _, img = cap.read()
        sqRow = []
        sqs = []
        oldSqRow = []
        oldSqs = []
      
        print('Setup started!')
        for i in range(8):
            for j in range(8):
                sq = crop(img, board_img[i][j],True)
                oldSq = crop(prev_img,board_img[i][j],True)
                result = mse(sq,oldSq)
                isSame = result < 200
                data = [result, isSame, board_img[i][j].position]
                sheet.append(data)
                sqRow.append(sq)
                oldSqRow.append(oldSq)
            sqs.append(sqRow)
            oldSqs.append(oldSqRow)
            sqRow = []
            oldSqRow = []

                

        print('Press "s" to save squares.')
        writeOutSquares(sqs,'./raw/',index=index)
        writeOutSquares(oldSqs,'./raw/',index=index,isOld=True)
        print('Continue? (y/n)')
        choice = input()
        if choice == 'n':
            is_setup = False
            workbook.save('data.xlsx')
            break
        else:
            prev_img = img
            _, img = cap.read()
            index += 64
            is_setup = True

    cv.destroyAllWindows()

if __name__ == '__main__':
    main()