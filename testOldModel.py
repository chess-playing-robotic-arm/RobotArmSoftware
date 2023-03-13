import cv2
from defmodel import myModel
import glob
import numpy as np


cv_img = []
pred = []

for img in glob.glob("input/data/WQ/*.png"):
    n= cv2.imread(img)
    cv_img.append(n)


print(f' number of images loaded : {len(cv_img)}')


model = myModel()
    
print('*************************MODEL LOADED*********************')
classNames = ['b', 'k', 'n', 'p', 'q', 'r',
                '_', 'B', 'K', 'N', 'P', 'Q', 'R']



print('model is ready. Start predicting')

for img in cv_img:
    # resized = cv2.resize(img,(128,128))
    sqR = np.expand_dims(img, axis=0)
    x = model(sqR, training=False)
    y = np.argmax(x,axis=1)
    y = classNames[int(y)]
    pred.append(y)

print(pred)

number_of_correct_preds = 0
for prediction in pred:
    if(prediction == 'Q'):
        number_of_correct_preds += 1

accuracy = (number_of_correct_preds / len(cv_img)) * 100

print(accuracy)
