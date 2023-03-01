from stockfish import Stockfish

stockfish = Stockfish(path="D:\stockfish\stockfish-windows-2022-x86-64-avx2.exe")


def evaluatePos(fen):
    if(stockfish.is_fen_valid(fen)):
        best_move = stockfish.get_best_move()
        evaluation = stockfish.get_evaluation() 
        return [best_move,evaluation]

    
while(1):
    print(stockfish.get_board_visual())
    move = input()
    stockfish.make_moves_from_current_position([move])
    enginMove = stockfish.get_best_move()
    print(enginMove)
    stockfish.make_moves_from_current_position([enginMove])

    