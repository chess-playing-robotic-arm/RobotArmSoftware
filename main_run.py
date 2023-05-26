import time
import cv2 as cv
import numpy as np
# from chessboard import display
 

from boardDetectFun import crop, drawOrderedPoints, drawPoints, readPoints, writeOutSquares

from defmodel import myModel
from fenUtils import boardToFen, matrix_to_fen
from square import Square
from utils.state_comparator import parallel_image_change_detection


def main():
    # model = myModel()
    
    # print('*************************MODEL LOADED*********************')
    # classNames = ['b', 'k', 'n', 'p', 'q', 'r',
    #               '_', 'B', 'K', 'N', 'P', 'Q', 'R']

    cap = cv.VideoCapture(1)
    # cap = cv.VideoCapture(gstreamer_pipeline(), cv.CAP_GSTREAMER)
    # cap = cv.VideoCapture(0)
    ret, img = cap.read()
    
   
    setup = True
    board_img = []
    board_row = []

    points = readPoints()

    for i in range(9):
        points[i] = sorted(points[i],reverse=True)

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

    # print('model is ready. Start predicting')
    
    prev_frame = img.copy()
    # index = 20
    while setup:
        print('next iteration ....')
        for i in range(100):
            ret, img = cap.read()
            if not ret:
                continue
        
       
        if not ret:
            break   
        img = cv.resize(img,(1080,720))
        prev_frame = cv.resize(prev_frame,(1080,720))
        # cv.imshow('current Frame',img)
        # cv.imshow('previous Frame',prev_frame)

        # cv.imwrite('output/new.png',img)
        # cv.imwrite('output/prev.png',prev_frame)
        print('started')
        t = time.process_time()
        result = parallel_image_change_detection(old_img=prev_frame,new_img=img,board=board_img)
        elapsed_time = time.process_time() - t

        print(f'it took: {elapsed_time}')
        if len(result) == 0:
            print('no changes happened')
        else:
            for i in result:
                print(i.position)
      
        prev_frame = img.copy()

        userInput = input('continue ? ')
        if userInput == 'y':
            setup = True
            # display.terminate()
        else:
            setup = False
            # display.terminate()
       

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()