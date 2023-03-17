
def boardToFen(board):
    fen = ''
    empty = 0
    for rows in board:
        for piece in rows:
            if piece.isletter() and empty == 0:
                fen += piece
            elif piece.isletter() and empty != 0:
                fen += str(empty)
                empty = 0
            elif piece == '_':
                empty += 1
        if empty != 0:
            fen += str(empty)
            empty = 0
        fen += '/'

    return fen

