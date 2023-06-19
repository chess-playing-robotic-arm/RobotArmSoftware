from stockfish import Stockfish
from datetime import datetime
import time
import json

import sys
sys.path.insert(0,"..")

from message_broker.broker import RabbitMQ

producer = RabbitMQ('bestMove')
consumer = RabbitMQ('fen')

stockfish = Stockfish(path="D:\stockfish\stockfish-windows-2022-x86-64-avx2.exe",depth=20)


def evaluatePos(fen):

    print(fen)
    print('evaluating')
    if(stockfish.is_fen_valid(fen)):
        print('valid position')
        stockfish.set_fen_position(fen)
        
        best_move = stockfish.get_best_move()
        evaluation = stockfish.get_evaluation() 
        return best_move,evaluation


def handler(msg):
    if(type(msg) == None): return
    print(f'{msg} is received')
    msg = json.loads(msg)
    best_move, evaluation = evaluatePos(msg['fen'])
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    msg = {'fen':msg['fen'],'best_move':best_move,'eval':evaluation,'time':current_time}
    producer.send(json.dumps(msg))
    print('msg sent')

consumer.consume(handler=handler)