

from stockfish import Stockfish



stockfish = Stockfish(path="D:\stockfish\stockfish-windows-2022-x86-64-avx2.exe",depth=20)


def evaluatePos(fen):
    if(stockfish.is_fen_valid(fen)):
        best_move = stockfish.get_best_move()
        evaluation = stockfish.get_evaluation() 
        return [best_move,evaluation]


enginMove = stockfish.get_best_move()
stockfish.make_moves_from_current_position([enginMove])
print(enginMove)
while(1):
    print(stockfish.get_board_visual())
    move = input()
    stockfish.make_moves_from_current_position([move])
    enginMove = stockfish.get_best_move()
    piece_type = stockfish.get_what_is_on_square(enginMove[:2])
    print(type(piece_type))
    if(piece_type ==Stockfish.Piece.WHITE_QUEEN or piece_type == Stockfish.Piece.BLACK_QUEEN or piece_type == Stockfish.Piece.WHITE_KING or piece_type == Stockfish.Piece.BLACK_KING):
        evaluation = 'k'
    else:
        evaluation = 'p'
    print(evaluation)
    # print(stockfish.get_what_is_on_square(enginMove[:2]))
    print(enginMove)
    stockfish.make_moves_from_current_position([enginMove])
    

    