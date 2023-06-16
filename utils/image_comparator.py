import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import imagehash
from PIL import Image

def preprocess_image(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive thresholding to enhance contrast
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # Apply image smoothing to reduce noise
    blurred = cv2.GaussianBlur(thresh, (3, 3), 0)
    
    return blurred


def similar_structure(current_image, previous_image):
   
    similarity_score = similarity = ssim(current_image, previous_image, multichannel=True,channel_axis=-1)

    return similarity_score
    

def color_comparison(current,prev):
    difference = cv2.subtract(current, prev)
    b, g, r = cv2.split(difference)
    nonZeroB = cv2.countNonZero(b)
    nonZeroG = cv2.countNonZero(g)
    nonZeroR = cv2.countNonZero(r)
    return [nonZeroB,nonZeroG,nonZeroR,nonZeroB+nonZeroG+nonZeroR]



def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err


def compare_image(current,prev):
    sim = similar_structure(current_image=current,previous_image=prev)
    err = mse(current,prev)
    return [sim,err] 




def is_same_image(image1, image2, threshold=5):
    img1 = Image.fromarray(image1)
    img2 = Image.fromarray(image2)

    # Load and compute image hashes
    hash1 = imagehash.average_hash(img1)
    hash2 = imagehash.average_hash(img2)
    
    # Compare the image hashes
    difference = hash1 - hash2
    print(difference)
    
    # Check if the difference is below the threshold
    if difference <= threshold:
        return True  # Images are considered the same
    else:
        return False  # Images are considered different
    





def main():
  # Read the current image of the chessboard.
  current_image = cv2.imread('images/11089.png')

  # Get the previous image of the chessboard.
  previous_image = cv2.imread('images/97.png')

  # Compare the two images.
  similarity = mse(current_image, previous_image)
  print(similarity)

  # If the images are similar, then we don't need to pass them to the model to identify the pieces.
  if similarity < 200:
    print('The images are similar. We don\'t need to pass them to the model.')
  else:
    print('The images are not similar. We need to pass them to the model.')

if __name__ == '__main__':
  main()