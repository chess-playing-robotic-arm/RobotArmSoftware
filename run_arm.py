import time
import chess
import cv2 as cv
import numpy as np
import threading
import serial 
import json
import queue

 

from boardDetectFun import crop, drawOrderedPoints, drawPoints, readPoints, writeOutSquares
from defmodel import myModel
from fenUtils import boardToFen, matrix_to_fen, matrix_to_fen2
from square import Square
# from utils.image_comparator import compare_images, is_same_image, is_similar

from datetime import datetime


from message_broker.broker import RabbitMQ
from control_arm.arm_model.arm import Arm
from testChessBoard import fen_to_board_matrix, normalMatrixToBitMatrix
from utils.compare_matices import compareMatrices, fromSquare, get_legal_captures
from utils.uic_to_arm import uciToArmCommands





producer = RabbitMQ('fen')
consumer = RabbitMQ('bestMove')


arduino = serial.Serial('COM7', 9600, timeout=0.1)
shared_queue = queue.Queue()




def initialize():
    print('***********************Initializing***********************')
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
    
    # board_img = np.flip(board_img, 1)
    # board_img = np.flip(board_img, 0)

    square_id = 1

    for i in range(8):
        for j in range(8):
            board_img[i][j].position = square_id
            square_id += 1
    return board_img






def sendToArduino(pos,motor):       
    try:
        command = str(motor) + str(pos) + '|'
        print('Motor : ' + str(motor) + ' Angle : ' + str(pos))
        arduino.write(str(command).encode())
    except:
        arduino.close()


def whenBestMoveAvailable(msg):
    bestMove = msg['best_move']
    print(bestMove)
    # Todo: translate stockfish moves into arm commands
    command = uciToArmCommands(bestMove)
    print(command)
    shared_queue.put(command)


def updateMatrix(main_matrix,diff):
    if(len(diff) == 2):
            
       
        if(diff[0][2] == 0):
            piece_type = main_matrix[diff[0][0]][diff[0][1]]
            main_matrix[diff[0][0]][diff[0][1]] = '_'
            main_matrix[diff[1][0]][diff[1][1]] = piece_type     
        else:
            piece_type = main_matrix[diff[1][0]][diff[1][1]]
            main_matrix[diff[0][0]][diff[0][1]] = piece_type
            main_matrix[diff[1][0]][diff[1][1]] = '_'  
        
    elif(len(diff) == 1):

        print(diff)
        piece_type = main_matrix[diff[0][0]][diff[0][1]]
        temp_fen = matrix_to_fen2(main_matrix)
        board = chess.Board()
        board.set_fen(temp_fen)
        print(board)
    
        square = chess.square(diff[0][1],abs(diff[0][0] - 7 ))

        print(f'square : {chess.square_name(square)}')
        captures = get_legal_captures(square, board)
        print(captures)
        for capture in captures:
            print(chess.square_name(capture))
        if(len(captures) == 1):
            i,j = fromSquare(chess.square_name(captures[0]))
            main_matrix[diff[0][0]][diff[0][1]] = '_'
            main_matrix[i][j] = piece_type
        elif(len(captures) > 1):
            for captures in captures:
                print(capture)

    

    return main_matrix
     


def startListening():
    consumer.consume(handler=whenBestMoveAvailable)

          
 
def main():
    
    thread = threading.Thread(target=startListening)
    thread.start()

    print('*************************Loading AI Model*********************')
    model = myModel()

    print('*************************Initializing Robotic Arm*********************')
    arm = Arm(arduino_conn= arduino,gripper_is_open=True)
    
    classNames = ['b', 'k', 'n', 'p', 'q', 'r',
                  '_', 'B', 'K', 'N', 'P', 'Q', 'R']

    cap = cv.VideoCapture(1)
    ret, img = cap.read()

    prev_matrix = [ [1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1] ]
    
    main_matrix = [ ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                    ['_', '_', '_', '_', '_', '_', '_', '_'],
                    ['_', '_', '_', '_', '_', '_', '_', '_'],
                    ['_', '_', '_', '_', '_', '_', '_', '_'],
                    ['_', '_', '_', '_', '_', '_', '_', '_'],
                    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'] ]
   
    running = True
    armTurn = True
    threshold = 5 
    isFirst = True
    
    board_img = initialize()
    
    prev_frame = img.copy()

    while running:
        if(isFirst):
            isFirst = False
            arm.make_move('d2','d4','p',False)
            main_matrix[6][3] = '_'
            main_matrix[4][3] = 'P'
            prev_matrix[6][3] = 0
            prev_matrix[4][3] = 1
            armTurn = False
            for i in range(8):
                for j in range(8):
                    print(prev_matrix[i][j], end="   ")
                print()
            time.sleep(5)
            for i in range(8):
                for j in range(8):
                    print(main_matrix[i][j], end="   ")
                print()

        for i in range(20):
            ret, img = cap.read()
        
        while(not armTurn):
            print('*************************AI Model is predicting...*********************')
            sqRow = []
            sqs = []
            pred_row = []
            pred = []
            for i in range(8):
                for j in range(8):
                    sq = crop(img, board_img[i][j])
                    sqR = np.expand_dims(sq, axis=0)
                    x = model(sqR, training=False)
                    y = np.argmax(x, axis=1)
                    y = classNames[int(y)]
                    if (y != '_'):
                        pred_row.append(1)
                    else:
                        pred_row.append(0)
                    # drawPoints(img,boardimg[i][j].points())
                    sqRow.append(sq)
                sqs.append(sqRow)
                pred.append(pred_row)
                pred_row = []
                sqRow = []

            print('printing the prediction matrix')
            for i in range(8):
                for j in range(8):
                    print(pred[i][j], end="   ")
                print()
            
            diff = compareMatrices(prev_matrix,pred)

            main_matrix = updateMatrix(main_matrix=main_matrix,diff=diff)
            new_fen = matrix_to_fen2(main_matrix)
            new_fen += " w - - 0 1" 
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            msg = {"fen":new_fen,"time":current_time}
            producer.send(json.dumps(msg))
            
            print('---------------- Going to sleep waiting for stockfish')
            
            armTurn = True

            time.sleep(5)
        
        if(shared_queue.not_empty):
            command = shared_queue.get()
            if(len(diff) == 2):
                arm.make_move(command[0],command[1],'p',False)
            elif(len(diff) == 1):
                arm.make_move(command[1],'o','p',False)
                time.sleep(1)
                arm.make_move(command[0],command[1],'p',False)
            else:
                arm.make_move(command[0],command[1],'p',False)
            armTurn = False
            board = chess.Board(new_fen)
            uciMove = f'{command[0]}{command[1]}'
            board.push_uci(uciMove)
            board.turn = chess.WHITE
            newFen = board.fen()
            
            main_matrix = fen_to_board_matrix(newFen)
            prev_matrix = normalMatrixToBitMatrix(main_matrix,prev_matrix)

            for row in main_matrix:
                print(row)
            
            for row in prev_matrix:
                print(row)

            print('going to sleep')
            time.sleep(10)
            print('good morning')

        prev_frame = img.copy()

        # print('*************************AI Model is predicting...*********************')
        # sq_row = []
        # sqs = []
        # pred_row = []
        # pred = []
        # for i in range(8):
        #     for j in range(8):
        #         sq = crop(img, board_img[i][j])
        #         sqR = np.expand_dims(sq, axis=0)
        #         x = model(sqR, training=False)
        #         y = np.argmax(x, axis=1)
        #         y = classNames[int(y)]
        #         pred_row.append(y)
        #         sqRow.append(sq)
        #     sqs.append(sq_row)
        #     pred.append(pred_row)
        #     pred_row = []
        #     sqRow = []
        
        # for i in range(8):
        #     for j in range(8):
        #         print(pred[i][j], end="   ")
        #     print()

        # fen = matrix_to_fen(pred)
        # print(fen)
        # now = datetime.now()
        # current_time = now.strftime("%H:%M:%S")
        # msg = {"fen":fen,"time":current_time}
        # producer.send(json.dumps(msg))
        
        # print('---------------- Going to sleep waiting for stockfish')
        # time.sleep(2)

        # if(shared_queue.not_empty):
        #     command = shared_queue.get()
        #     arm.make_move(command[0],command[1],'p',False)
        #     armTurn = False


        # t = time.process_time()
        # for i in range(8):
        #     for j in range(8):
        #         sq = crop(img, board_img[i][j],True)
        #         oldSq = crop(prev_frame,board_img[i][j])
        #         result = is_similar(sq,oldSq)
        # elapsed_time = time.process_time() - t

        # print(f'it took: {elapsed_time}')
        
      
        # prev_frame = img.copy()

        # userInput = input('continue ? ')
        # double_value = float(userInput)
        # if userInput == 'n':
        #     running = False
        #     # display.terminate()
        # else:
        #     threshold = double_value
        #     running = True
        #     # display.terminate()
       

    cap.release()
    cv.destroyAllWindows()
    thread.join()


if __name__ == "__main__":
    main()