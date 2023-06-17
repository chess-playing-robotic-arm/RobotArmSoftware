def boardToFen(board):
    fen = ''
    empty = 0
    for rows in board:
        for piece in rows:
            if piece.isalpha() and empty == 0:
                fen += piece
            elif piece.isalpha() and empty != 0:
                fen += str(empty)
                empty = 0
            elif piece == '_':
                empty += 1
        if empty != 0:
            fen += str(empty)
            empty = 0
        fen += '/'

    return fen

matrix = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "_", "p", "p", "p"],
    ["_", "_", "_", "_", "_", "_", "_", "_"],
    ["_", "_", "_", "_", "p", "_", "_", "_"],
    ["_", "_", "_", "_", "_", "_", "_", "_"],
    ["_", "_", "_", "P", "_", "_", "_", "_"],
    ["P", "P", "P", "_", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"]
]


def matrix_to_fen(matrix):
    fen = ""
    empty_count = 0
    for row in reversed(matrix):
        for square in row:
            if square == "_":
                empty_count += 1
            else:
                if empty_count > 0:
                    fen += str(empty_count)
                    empty_count = 0
                fen += {
                    'p': 'P',
                    'n': 'N',
                    'b': 'B',
                    'r': 'R',
                    'q': 'Q',
                    'k': 'K',
                    'P': 'p',
                    'N': 'n',
                    'B': 'b',
                    'R': 'r',
                    'Q': 'q',
                    'K': 'k'
                }[square]
        if empty_count > 0:
            fen += str(empty_count)
            empty_count = 0
        fen += "/"
    fen = fen[:-1]  # Remove last "/"
    fen += " w - - 0 1"  # Add player turn,
    
    return fen

def matrix_to_fen2(matrix):
    fen = ''
    for row in matrix:
        empty_count = 0
        for cell in row:
            if cell == '_':
                empty_count += 1
            else:
                if empty_count > 0:
                    fen += str(empty_count)
                    empty_count = 0
                fen += cell
        if empty_count > 0:
            fen += str(empty_count)
        fen += '/'
    fen = fen[:-1]  # Remove the trailing '/'
    return fen
# print(matrix_to_fen(matrix))


