import json
import os
from Source.model import Character

def reset_characters():
    character_files_path = 'Character_templates'
    characters = load_data(Character, character_files_path)
    save_data(characters, Character)

# Load data of the specified class type
def load_data(class_type, file_path=None):
    data = {}
    if file_path is None:
        file_path = f'{class_type.__name__}_files'
    data_files = os.listdir(file_path)
    for file in data_files:
        with open(os.path.join(file_path, file)) as f:
            item = json.load(f)
            data[item['title']] = class_type(**item)
    return data

# Save data of the specified class type
def save_data(data, class_type, file_path=None):

    if file_path is None:
        directory = f'{class_type.__name__}_files'
    else:
        directory = file_path

    if not os.path.exists(directory):
        os.makedirs(directory)  # Ensure the directory exists

    for title, item in data.items():

        file_path = os.path.join(directory, f'{title}.json')

        with open(file_path, 'w') as f:
            # Use vars() to convert the class instance to a dictionary
            item_dict = vars(item)
            json.dump(item_dict, f, indent=4)

# Load txt into a list
def load_txt(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines()]
        