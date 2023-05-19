import cv2
import multiprocessing

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

def check_image_change(old_state, new_state, start_row, end_row, result_queue):
    for i in range(start_row, end_row):
        for j in range(8):
            gray1 = cv2.cvtColor(old_state[i][j], cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(new_state[i][j], cv2.COLOR_BGR2GRAY)
            # Calculate the absolute difference between the two grayscale images
            diff = cv2.absdiff(gray1, gray2)
            # Apply a threshold to the absolute difference image to create a binary image
            thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)[1]
            percentage_diff = cv2.countNonZero(thresh) / thresh.size * 100
            if percentage_diff > 30:
                result_queue.put(new_state[i][j])
                # print("The images have changed significantly")
            else:
                return
            # print(percentage_diff)

    # Compare the percentage of differing pixels to a threshold value
    
        # print("The images are practically the same")

    


def parallel_image_change_detection(old_board, new_board):
    num_processes = multiprocessing.cpu_count()
    result_queue = multiprocessing.Queue()

    processes = []
    rows_per_process = 8 // num_processes

    for i in range(num_processes):
        start_row = i * rows_per_process
        end_row = (i + 1) * rows_per_process

        p = multiprocessing.Process(target=check_image_change, args=(old_board, new_board,start_row,end_row, result_queue))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    differing_images = []
    while not result_queue.empty():
        images = result_queue.get()
        differing_images.extend(images)

    return differing_images