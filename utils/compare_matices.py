
import chess

import sys
sys.path.insert(0,"..")
from fenUtils import boardToFen, matrix_to_fen, matrix_to_fen2




def get_legal_captures(square, board):
    legal_captures = []
    piece = board.piece_at(square)
    print(piece)
    if piece is not None:
        for move in board.legal_moves:
          
            if board.is_capture(move) and move.from_square == square:
                legal_captures.append(move.to_square)
    return legal_captures

def fromSquare(square):
    chess_map = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
    return [abs(int(square[1]) - 8),chess_map[square[0]]]


def compareMatrices(old_matrix,new_matrix):
    diff_lst = []
    for i in range(8):
        for j in range(8):
            if new_matrix[i][j] != old_matrix[i][j]:
                if(new_matrix[i][j] == 1):
                    type_of_change = 1   
                else:
                    type_of_change = 0
                print(f"Difference at position ({i}, {j})")
                diff_lst.append([i,j,type_of_change])
    return diff_lst


# prev_matrix = [ [1,1,1,1,1,1,1,1],
#                 [1,1,1,1,1,1,0,1],
#                 [0,0,0,0,0,0,0,0],
#                 [0,0,0,0,0,0,1,0],
#                 [0,0,0,1,0,0,0,0],
#                 [0,0,0,0,0,0,0,0],
#                 [1,1,1,0,1,1,1,1],
#                 [1,1,1,1,1,1,1,1]  ]

# main_matrix = [ ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
#                 ['p', 'p', 'p', 'p', 'p', 'p', '_', 'p'],
#                 ['_', '_', '_', '_', '_', '_', '_', '_'],
#                 ['_', '_', '_', '_', '_', '_', 'p', '_'],
#                 ['_', '_', '_', 'P', '_', '_', '_', '_'],
#                 ['_', '_', '_', '_', '_', '_', '_', '_'],
#                 ['P', 'P', 'P', '_', 'P', 'P', 'P', 'P'],
#                 ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'] ]

# current_matrix = [  [1,1,1,1,1,1,1,1],
#                     [1,1,1,1,1,1,0,1],
#                     [0,0,0,0,0,0,0,0],
#                     [0,0,0,0,0,0,1,0],
#                     [0,0,0,1,0,0,0,0],
#                     [0,0,0,0,0,0,0,0],
#                     [1,1,1,0,1,1,1,1],
#                     [1,1,0,1,1,1,1,1]]

# diff = compareMatrices(prev_matrix,current_matrix)



# if(len(diff) == 2):
#     if(diff[0][2] == 0):
#         piece_type = main_matrix[diff[0][0]][diff[0][1]]
#         main_matrix[diff[0][0]][diff[0][1]] = '_'
#         main_matrix[diff[1][0]][diff[1][1]] = piece_type     
#     else:
#         piece_type = main_matrix[diff[1][0]][diff[1][1]]
#         main_matrix[diff[0][0]][diff[0][1]] = piece_type
#         main_matrix[diff[1][0]][diff[1][1]] = '_'  
    
# elif(len(diff) == 1):
#     print(diff)
#     piece_type = main_matrix[diff[0][0]][diff[0][1]]
#     temp_fen = matrix_to_fen2(main_matrix)
#     board = chess.Board()
#     board.set_fen(temp_fen)
#     print(board)
   
#     square = chess.square(diff[0][1],abs(diff[0][0] - 7 ))

#     print(f'square : {chess.square_name(square)}')
#     captures = get_legal_captures(square, board)
#     print(captures)
#     for capture in captures:
#         print(chess.square_name(capture))
#     if(len(captures) == 1):
#         i,j = fromSquare(chess.square_name(captures[0]))
#         main_matrix[diff[0][0]][diff[0][1]] = '_'
#         main_matrix[i][j] = piece_type

  


# print(piece_type)
    
# for row in main_matrix:
#     print(row)
# new_fen = matrix_to_fen2(main_matrix)
# print(new_fen)
#     # producer.send(new_fen)
# armTurn = True