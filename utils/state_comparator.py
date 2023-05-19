import cv2

# Load the two images you want to compare
img1 = cv2.imread("images/test01.png")
img2 = cv2.imread("images/wqtest03.png")

# Convert the images to grayscale
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Calculate the absolute difference between the two grayscale images
diff = cv2.absdiff(gray1, gray2)


# Apply a threshold to the absolute difference image to create a binary image
thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)[1]


cv2.imshow("Difference Image", diff)
cv2.imshow('Threshold',thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()
# Calculate the percentage of the pixels in the binary image that are white
percentage_diff = cv2.countNonZero(thresh) / thresh.size * 100

print(percentage_diff)

# Compare the percentage of differing pixels to a threshold value
if percentage_diff > 30:
    print("The images have changed significantly")
else:
    print("The images are practically the same")
