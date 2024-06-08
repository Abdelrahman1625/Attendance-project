import os
import shutil
import random


def split_folder_contents(source_folder, dest_folder1, dest_folder2, split_ratio=0.2):
    # Ensure the source and destination folders exist
    if not os.path.exists(source_folder):
        print(f"The source folder {source_folder} does not exist.")
        return

    # Iterate through each directory in the source folder
    for subdir in os.listdir(source_folder):
        subdir_path = os.path.join(source_folder, subdir)
        if os.path.isdir(subdir_path):
            # Prepare directories in the destination folders
            dest_subdir1 = os.path.join(dest_folder1, subdir)
            dest_subdir2 = os.path.join(dest_folder2, subdir)
            os.makedirs(dest_subdir1, exist_ok=True)
            os.makedirs(dest_subdir2, exist_ok=True)

            # List all files in the current subdirectory
            files = [f for f in os.listdir(subdir_path) if os.path.isfile(
                os.path.join(subdir_path, f))]
            random.shuffle(files)  # Shuffle to distribute files randomly

            # Calculate the index for splitting files
            split_index = int(len(files) * split_ratio)

            # Move 20% of files to the first destination subfolder
            for file in files[:split_index]:
                shutil.move(os.path.join(subdir_path, file),
                            os.path.join(dest_subdir1, file))

            # Move the remaining 80% of files to the second destination subfolder
            for file in files[split_index:]:
                shutil.move(os.path.join(subdir_path, file),
                            os.path.join(dest_subdir2, file))

    print("Files have been successfully split into",
        dest_folder1, "and", dest_folder2)


# Example usage
source_folder = 'D:/projects/image project/dataset/frame'
# Will contain 20% of each folder's files
dest_folder1 = 'D:/projects/image project/dataset/testing'
# Will contain the remaining 80% of each folder's files
dest_folder2 = 'D:/projects/image project/dataset/training'
split_folder_contents(source_folder, dest_folder1, dest_folder2)
