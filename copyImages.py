import os
import shutil

# Source folder containing the PNG pictures
source_folder = './raw'

# Destination folder for unique pictures
destination_folder = './similar'

# Folder to check for duplicates
check_folder = './different'

# Get the list of files in the source folder
source_files = os.listdir(source_folder)

# Create the destination folder if it doesn't exist
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Iterate over each file in the source folder
for file_name in source_files:
    if file_name.endswith('.png'):
        # Check if the file exists in the check folder
        if file_name in os.listdir(check_folder):
            print(f"Duplicate file found: {file_name}")
        else:
            # Copy the file to the destination folder
            source_file_path = os.path.join(source_folder, file_name)
            destination_file_path = os.path.join(destination_folder, file_name)
            shutil.copy2(source_file_path, destination_file_path)
            print(f"Unique file copied: {file_name}")
