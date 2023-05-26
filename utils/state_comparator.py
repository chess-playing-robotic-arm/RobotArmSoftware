import os
import cv2
import multiprocessing

import numpy as np

from boardDetectFun import crop


def check_image_change(old_img, new_img, board, start_row, end_row, result_queue):
    for i in range(start_row, end_row):
        for j in range(8):
            # print(f'i: {i}, j: {j}')
            old_square = crop(old_img, board[i][j])
            new_square = crop(new_img, board[i][j])
            gray1 = cv2.cvtColor(old_square, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(new_square, cv2.COLOR_BGR2GRAY)
            # os.makedirs('./output/')
            # new_file_name = f'./output/{str(board[i][j].position)}n.png'
            # prev_file_name = f'./output/{str(board[i][j].position)}p.png'
            
            # cv2.imwrite(new_file_name, new_square)
            # cv2.imwrite(prev_file_name, old_square)
            mean_intensity = np.mean(gray1)
            mean_intensity2 = np.mean(gray2)
            # Calculate the absolute difference between the two grayscale images
            # diff = cv2.absdiff(gray1, gray2)
            # # Apply a threshold to the absolute difference image to create a binary image
            # thresh = cv2.threshold(diff, 40, 255, cv2.THRESH_TOZERO)[1]
            # percentage_diff = cv2.countNonZero(thresh) / thresh.size * 100
            percentage_diff = abs(mean_intensity - mean_intensity2)
            if percentage_diff > 1:
                result_queue.put(board[i][j])
                # print(f"The {board[i][j].position} image have changed significantly")
            # else:
                # print(f"The {board[i][j].position} image have Not changed")
                # return
            # print(percentage_diff)    

    


def parallel_image_change_detection(old_img, new_img, board):
    num_processes = multiprocessing.cpu_count()
    result_queue = multiprocessing.Queue()

    processes = []
    rows_per_process = 8 // num_processes
    # print(f'Number of Processes: {num_processes}')
    # print(f'rows per process: {rows_per_process}')
    for i in range(num_processes):
        start_row = i * rows_per_process
        end_row = (i + 1) * rows_per_process
        # print(f'Start row : {start_row}')
        # print(f'End row: {end_row}')

        p = multiprocessing.Process(target=check_image_change, args=(old_img, new_img ,board, start_row, end_row, result_queue))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    differing_images = []
    while not result_queue.empty():
        images = result_queue.get()
        differing_images.append(images)

    return differing_images