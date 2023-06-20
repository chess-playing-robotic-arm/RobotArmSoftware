from chess import Piece
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
        piece_type = stockfish.get_what_is_on_square(best_move[:2])
        if(piece_type ==Stockfish.Piece.WHITE_QUEEN or piece_type == Stockfish.Piece.BLACK_QUEEN or piece_type == Stockfish.Piece.WHITE_KING or piece_type == Stockfish.Piece.BLACK_KING):
            evaluation = 'k'
        else:
            evaluation = 'p'
        # evaluation = stockfish.get_evaluation() 
        return best_move,evaluation
    else:
        return "0" ,"0"

def handler(msg):
    if(type(msg) == None): return
    print(f'{msg} is received')
    msg = json.loads(msg)
    best_move, evaluation = evaluatePos(msg['fen'])
    if(best_move == 0):
        print('illegal move')
        msg = {'fen':'0','best_move':'0'}
        producer.send(json.dumps(msg))
    else:

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        msg = {'fen':msg['fen'],'best_move':best_move,'eval':evaluation,'time':current_time}
        producer.send(json.dumps(msg))
        print('msg sent')

consumer.consume(handler=handler)