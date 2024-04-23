import os

# Load all txt files in directory into the same list
def read_txt_all(directory):
    txt_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            txt_files += read_txt(os.path.join(directory, filename))
    return txt_files

# Load txt into a list
def read_txt(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines()]