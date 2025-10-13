
import json
import os


def update_jsons(file_path, data):
    """Update the JSON file at the given path with the provided data"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


def get_data_from_file(file_path):
    """
    Load data from a JSON file and return it as a dict or list. Return an empty list if the file does not exist or is empty.
    """
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as json_file:
        try:
            return json.load(json_file)
        except json.JSONDecodeError:
            return []
