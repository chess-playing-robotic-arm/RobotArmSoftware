
import cv2
import numpy as np
from boardDetectFun import crop, drawOrderedPoints, readPoints

from square import Square

cap = cv2.VideoCapture(1)
setup = True


board_img = []
board_row = []

points = readPoints()

for i in range(9):
    points[i] = sorted(points[i],reverse=True)

square_id = 64

for i in range(8):
    for j in range(8):
        p1 = points[i][j]
        p2 = points[i][j+1]
        p3 = points[i+1][j]
        p4 = points[i+1][j+1]
        square = Square(p1=p1, p2=p2, p3=p3, p4=p4, position=square_id)
        
        square_id -= 1
        board_row.append(square)
    board_img.append(board_row)
    board_row = []

board_img = np.transpose(board_img)

# board_img = np.flip(board_img, 1)
# board_img = np.flip(board_img, 0)

square_id = 1

for i in range(8):
    for j in range(8):
        board_img[i][j].position = square_id
        square_id += 1
        

while setup:
    _, img = cap.read()
    # img = cv.resize(img,(1080,720))
    
            
    for i in range(8):
        sq = crop(img, board_img[0][i])
        cv2.imshow(f'{board_img[0][i]}', sq)
            
    keyCode = cv2.waitKey(10) & 0xFF
    if keyCode == ord('q'):
        print('Quitting')
        break
    
cap.release()
cv2.destroyAllWindows()



