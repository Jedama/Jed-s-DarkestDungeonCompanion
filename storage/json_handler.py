import json
import os

def read_json(path):

    # If the path does not end with '.json', add it
    if not path.endswith('.json'):
        path += '.json'

    try:
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f'File not found: {path}')
        return None 
    except json.JSONDecodeError:
        print(f'Error decoding JSON from: {path}')
        return None

def load_json(directory, from_dict_func):
    data_dict = {}

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            data = read_json(file_path)
            if data:
                for item in data:
                    obj = from_dict_func(item)
                    data_dict[obj.title] = obj  # Use a generic key or adjust as necessary
    return data_dict

def save_json(path, data):
    # If the path does not end with '.json', add it
    if not path.endswith('.json'):
        path += '.json'

    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def save_json_directory(directory, data_dict):
    os.makedirs(directory, exist_ok=True)
    for title, obj in data_dict.items():
        file_path = os.path.join(directory, f"{title}.json")
        save_json(file_path, obj.to_dict())