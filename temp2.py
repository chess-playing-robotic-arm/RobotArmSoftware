import chess

from fenUtils import matrix_to_fen2
from utils.compare_matices import compareMatrices, fromSquare, get_legal_captures


def updateMatrix(main_matrix,diff):
    if(len(diff) == 2):
            
       
        if(diff[0][2] == 0):
            piece_type = main_matrix[diff[0][0]][diff[0][1]]
            main_matrix[diff[0][0]][diff[0][1]] = '_'
            main_matrix[diff[1][0]][diff[1][1]] = piece_type     
        else:
            piece_type = main_matrix[diff[1][0]][diff[1][1]]
            main_matrix[diff[0][0]][diff[0][1]] = piece_type
            main_matrix[diff[1][0]][diff[1][1]] = '_'  
        
    elif(len(diff) == 1):

        print(diff)
        piece_type = main_matrix[diff[0][0]][diff[0][1]]
        temp_fen = matrix_to_fen2(main_matrix)
        board = chess.Board()
        board.set_fen(temp_fen)
        print(board)
    
        square = chess.square(diff[0][1],abs(diff[0][0] - 7 ))

        print(f'square : {chess.square_name(square)}')
        captures = get_legal_captures(square, board)
        print(captures)
        for capture in captures:
            print(chess.square_name(capture))
        if(len(captures) == 1):
            i,j = fromSquare(chess.square_name(captures[0]))
            main_matrix[diff[0][0]][diff[0][1]] = '_'
            main_matrix[i][j] = piece_type
        elif(len(captures) > 1):
            for captures in captures:
                print(capture)

    print(f'the piece is: {piece_type}')

    return main_matrix, piece_type


prev_matrix = [ [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,0,0,1],
                [0,0,0,0,0,1,0,0],
                [0,0,0,0,0,0,1,0],
                [0,0,0,1,1,0,0,0],
                [0,0,0,0,0,0,0,0],
                [1,1,1,0,0,1,1,1],
                [1,1,1,1,1,1,1,1] ]
    
main_matrix = [ ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                ['p', 'p', 'p', 'p', 'p', '_', '_', 'p'],
                ['_', '_', '_', '_', '_', 'p', '_', '_'],
                ['_', '_', '_', '_', '_', '_', 'p', '_'],
                ['_', '_', '_', 'P', 'P', '_', '_', '_'],
                ['_', '_', '_', '_', '_', '_', '_', '_'],
                ['P', 'P', 'P', '_', '_', 'P', 'P', 'P'],
                ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'] ]

prev = [[1,1,1,1,1,1,1,1],
        [1,1,1,1,1,0,0,1],
        [0,0,0,0,0,1,0,0],
        [0,0,0,0,0,0,1,0],
        [0,0,0,1,1,0,0,0],
        [0,0,0,0,0,0,0,0],
        [1,1,1,0,0,1,1,1],
        [1,1,1,1,1,1,1,1] ]
diff = compareMatrices(prev_matrix,pred)

main_matrix,piece_type = updateMatrix(main_matrix=main_matrix,diff=diff)