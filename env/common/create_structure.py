import os
import string
import shutil

def create_structure(path, dir_number=1, file_number=1, depth=1):
    """
    Creating a specified 'depth' of nesting levels with 'dir_number' directories (dirA to dirZ)
    and 'file_number' files (file0.log to file9.log, file0.txt to file9.txt).
    """
    def create_files(path, files):
        for file_name in files:
            file_path = os.path.join(path, file_name)
            with open(file_path, 'w') as f:
                f.write(f'This is {file_name}\n')  # Optional content

    # Safely remove the base directory if it exists
    if os.path.exists(path):
        shutil.rmtree(path)

    # Limit the number of directories to 26 (A-Z) and files to 10 (0-9)
    dir_number = (dir_number - 1) % 26 + 1
    file_number = (file_number - 1) % 10 + 1

    # Generate directory names (dirA, dirB, ..., dirZ)
    dir_names = [f'dir{letter}' for letter in string.ascii_uppercase[:dir_number]]

    # Generate file names (file0.txt, file1.txt, ..., file9.txt and file0.log, file1.log, ..., file9.log)
    txt_files = [f'file{digit}.txt' for digit in range(file_number)]
    log_files = [f'file{digit}.log' for digit in range(file_number)]

    # Create the directories and files in the base path
    for dir_name in dir_names:
        current_dir_path = os.path.join(path, dir_name)
        os.makedirs(current_dir_path, exist_ok=True)

        # Create .txt and .log files in the current directory
        create_files(current_dir_path, txt_files)
        create_files(current_dir_path, log_files)

        # If depth is greater than 1, create nested directories and files
        if depth > 1:
            create_structure(current_dir_path, dir_number, file_number, depth - 1)

    # Create .txt and .log files in the base path as well
    create_files(path, txt_files)
    create_files(path, log_files)

# Example usage
#create_structure('test_structure', dir_number=5, file_number=3, depth=2)
