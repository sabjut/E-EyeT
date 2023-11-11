#! /usr/bin/env python3
import os
import shutil

def copy_mp4_files(src_dir, dst_dir):
    # Create the destination directory if it does not exist
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    # Walk through all subdirectories in the source directory
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            # Check if the file is an .mp4 file
            if file.endswith('.mp4'):
                src_file_path = os.path.join(root, file)
                dst_file_path = os.path.join(dst_dir, file)

                # Copy the file to the destination directory
                shutil.copy2(src_file_path, dst_file_path)
                print(f"Copied: {src_file_path} -> {dst_file_path}")

# Define the source and destination directories
src_directory = "../data/pixie"
dst_directory = "static"

copy_mp4_files(src_directory, dst_directory)
