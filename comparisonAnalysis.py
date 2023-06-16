import os

import cv2
import openpyxl


from utils.image_comparator import color_comparison, compare_image

workbook = openpyxl.load_workbook('differentColor.xlsx')

    # Select the sheet to append data to
sheet = workbook.active

folder_path = './different'  # Path to the folder containing the image pairs

# Get the list of files in the folder
files = os.listdir(folder_path)

# Sort the files to ensure consistent ordering
files.sort()

# Iterate over the files in pairs
for file_name in files:
    if file_name.endswith('.png'):
        # Check if the file has a corresponding "numberold.png" file
        old_file = file_name[:-4] + 'old.png'
        if old_file in files:
            current_file_path = os.path.join(folder_path, file_name)
            old_file_path = os.path.join(folder_path, old_file)

            # Perform further processing with the image pair
            # For example, you can use libraries like PIL or OpenCV to work with the images
            # Here's a basic example using PIL to print the file names
            print("Current file:", current_file_path)
            print("Old file:", old_file_path)

            current_img = cv2.imread(current_file_path)
            prev_img = cv2.imread(old_file_path)

            lst_comparison_values = color_comparison(current_img,prev_img)
            print(lst_comparison_values)
            print()
            sheet.append([file_name[:-4],lst_comparison_values[0],lst_comparison_values[1],lst_comparison_values[2],lst_comparison_values[3]])

            # You can replace the print statements with your desired processing logic
workbook.save('differentColor.xlsx')