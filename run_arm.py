import time
import cv2 as cv
import numpy as np
import threading
import serial 
import json
import queue
# from chessboard import display
 

from boardDetectFun import crop, drawOrderedPoints, drawPoints, readPoints, writeOutSquares
from defmodel import myModel
from fenUtils import boardToFen, matrix_to_fen
from square import Square
from utils.image_comparator import compare_images, is_same_image, is_similar
from utils.state_comparator import parallel_image_change_detection

from datetime import datetime


from message_broker.broker import RabbitMQ
from control_arm.arm_model.arm import Arm


producer = RabbitMQ('fen')
consumer = RabbitMQ('bestMove')

arduino = serial.Serial('COM3', 9600, timeout=0.1)
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
    board_img = np.flip(board_img, 1)
    board_img = np.flip(board_img, 0)

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
    print(msg)
    # Todo: translate stockfish moves into arm commands
    command = ['d2','d4']
    shared_queue.put(command)



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

    
   
    running = True
    armTurn = True
    threshold = 5 
    
    board_img = initialize()
    
    prev_frame = img.copy()

    while running:
        ret, img = cap.read()
        if(not armTurn):
            # Todo : look for a change then set armTurn back to true
            continue
        print('*************************AI Model is predicting...*********************')
        sq_row = []
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
                pred_row.append(y)
                sqRow.append(sq)
            sqs.append(sq_row)
            pred.append(pred_row)
            pred_row = []
            sqRow = []
        
        for i in range(8):
            for j in range(8):
                print(pred[i][j], end="   ")
            print()

        fen = matrix_to_fen(pred)
        print(fen)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        msg = {"fen":fen,"time":current_time}
        producer.send(json.dumps(msg))
        
        print('---------------- Going to sleep waiting for stockfish')
        time.sleep(2)

        if(shared_queue.not_empty):
            command = shared_queue.get()
            arm.make_move(command[0],command[1],'p',False)
            armTurn = False


        t = time.process_time()
        for i in range(8):
            for j in range(8):
                sq = crop(img, board_img[i][j],True)
                oldSq = crop(prev_frame,board_img[i][j])
                result = is_similar(sq,oldSq)
        elapsed_time = time.process_time() - t

        print(f'it took: {elapsed_time}')
        
      
        prev_frame = img.copy()

        userInput = input('continue ? ')
        double_value = float(userInput)
        if userInput == 'n':
            running = False
            # display.terminate()
        else:
            threshold = double_value
            running = True
            # display.terminate()
       

    cap.release()
    cv.destroyAllWindows()
    thread.join()


if __name__ == "__main__":
    main()