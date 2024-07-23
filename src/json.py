import json

def load_json_config(file_path):
    """
    Load a JSON file and return its contents as a dictionary.
    
    :param file_path: Path to the JSON file.
    :return: Dictionary containing the JSON data.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return None
