import cv2 as cv
import numpy as np
from chessboard import display
 

from boardDetectFun import crop, drawOrderedPoints, drawPoints, readPoints, writeOutSquares

from defmodel import myModel
from fenUtils import boardToFen, matrix_to_fen
from square import Square



# def gstreamer_pipeline(
#     capture_width=1280,
#     capture_height=720,
#     display_width=960,
#     display_height=540,
#     framerate=120,
#     flip_method=0,
# ):
#     return (
#         "nvarguscamerasrc ! "
#         "video/x-raw(memory:NVMM), "
#         "width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
#         "nvvidconv flip-method=%d ! "
#         "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
#         "videoconvert ! "
#         "video/x-raw, format=(string)BGR ! appsink drop=True"
#         % (
#             capture_width,
#             capture_height,
#             framerate,
#             flip_method,
#             display_width,
#             display_height,
#         )
#     )


def main():
    model = myModel()
    
    print('*************************MODEL LOADED*********************')
    classNames = ['b', 'k', 'n', 'p', 'q', 'r',
                  '_', 'B', 'K', 'N', 'P', 'Q', 'R']

    # cap = cv.VideoCapture(gstreamer_pipeline(), cv.CAP_GSTREAMER)
    cap = cv.VideoCapture(0)
    ret, img = cap.read()
   
    setup = True
    boardimg = []
    boardrow = []

    points = readPoints()
    for i in range(9):
        points[i] = sorted(points[i],reverse=True)
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

    print('model is ready. Start predicting')
    
    # index = 20
    while setup:
        ret, img = cap.read()
        sqRow = []
        sqs = []
        predrow = []
        pred = []
        for i in range(8):
            for j in range(8):
                sq = crop(img, boardimg[i][j])
                sqR = np.expand_dims(sq, axis=0)
                x = model(sqR, training=False)
                y = np.argmax(x, axis=1)
                y = classNames[int(y)]
                if (y != '_'):
                    predrow.append(1)
                else:
                    predrow.append(0)
                # drawPoints(img,boardimg[i][j].points())
                sqRow.append(sq)
            sqs.append(sqRow)
            pred.append(predrow)
            predrow = []
            sqRow = []
        
        for i in range(8):
            for j in range(8):
                print(pred[i][j], end="   ")
            print()

        # fen = matrix_to_fen(pred)
        # game_board = display.start(fen=fen)
        # display.update(fen, game_board)
        print('write out images ? (Y/n)')
        x = input()
        if (x == 'y'):
            writeOutSquares(sqs,'./tests/',index=0)

        print('continue Predicting ?')
        userInput = input()
        if userInput == 'y':
            setup = True
            display.terminate()
        else:
            setup = False
            display.terminate()
       

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
