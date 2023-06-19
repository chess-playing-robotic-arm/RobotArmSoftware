import base64
import cv2
import numpy as np

import json

import sys
sys.path.insert(0,"..")

from boardDetectFun import crop
from defmodel import myModel
from message_broker.broker import RabbitMQ

producer = RabbitMQ('pred')
consumer = RabbitMQ('image')




def predict(img, board_img):
        
    classNames = ['b', 'k', 'n', 'p', 'q', 'r',
                  '_', 'B', 'K', 'N', 'P', 'Q', 'R']
    print('*************************Loading AI Model*********************')
    model = myModel()
    print('*************************Initializing Robotic Arm*********************')

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
    return pred


def handler(msg):
    print(f'msg is received')
    x = base64.decodebytes(msg.tobytes())
    nparr = np.fromstring(x, np.uint8)
    img = cv2.imdecode(nparr, flags=1)
    print(img)
    print(type(img))
    # nparr = np.fromstring(msg, np.int32)
    # img = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)
    # print(img)
    print('*************************predicting***********************')
    # best_move, evaluation = evaluatePos(msg["fen"])
    # pred = predict(img,board_img=board_img)
    # print(pred)
    
    # msg = {'fen':msg['fen'],'best_move':best_move,'eval':evaluation,'time':current_time}
    # producer.send(json.dumps(msg))

consumer.consume(handler=handler)