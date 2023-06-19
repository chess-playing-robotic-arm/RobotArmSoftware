import chess
import numpy as np


def fen_to_board_matrix(fen):
    ranks = fen.split()[0].split('/')
    board_matrix = [['_' for _ in range(8)] for _ in range(8)]
    rank_index = 0

    for rank in ranks:
        file_index = 0
        for char in rank:
            if char.isdigit():
                file_index += int(char)
            else:
                board_matrix[7 - rank_index][file_index] = char
                file_index += 1
        rank_index += 1
    
    
    board_matrix= np.flip(board_matrix, 1)
    board_matrix= np.flip(board_matrix, 0)
    board_matrix= np.flip(board_matrix, 1)
    return board_matrix


def normalMatrixToBitMatrix(normalMatrix,bitMatrix):
    for i in range(8):
        for j in range(8):
            if(normalMatrix[i][j] == '_'):
                bitMatrix[i][j] = 0
            else:
                bitMatrix[i][j] = 1 
    return bitMatrix
    

# # # Example usage
# fen = "rnbqkbnr/ppppp1pp/8/5p2/3P4/8/PPP1PPPP/RNBQKBNR w - - 0 1"
# board = chess.Board(fen)

# board.push_uci('b1c3')
# print(board)
# board.turn = chess.WHITE
# newFen = board.fen()

# print(newFen)

m = [[1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 0, 1, 1, 1, 1, 1],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 1, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 0, 0],
[1, 1, 1, 1, 0, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 0, 1]]

m= np.flip(m, 1)
print(m)
# board_matrix = fen_to_board_matrix(newFen)
# board_matrix= np.flip(board_matrix, 0)
# board_matrix= np.flip(board_matrix, 1)

# for i in range(8):
#     for j in range(8):
#         if(board_matrix[i][j] == '_'):
#             prev_matrix[i][j] = 0
#         else:
#             prev_matrix[i][j] = 1 

# # Display the resulting board matrix
# for row in board_matrix:
#     print(row)

# for row in prev_matrix:
#     print(row)