import json
import os
from tqdm import tqdm


def flatten_dict(data, parent_key="", sep="_"):
    """
    Flattens a nested dictionary into a single-level dictionary.

    Args:
        data (dict): The dictionary to flatten.
        parent_key (str): The prefix for keys in the flattened dictionary.
        sep (str): The separator to use between keys.

    Returns:
        dict: A flattened dictionary.
    """
    items = []
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    items.extend(
                        flatten_dict(item, f"{new_key}{sep}{i}", sep=sep).items()
                    )
                else:
                    items.append((f"{new_key}{sep}{i}", item))
        else:
            items.append((new_key, v))
    return dict(items)


def json_to_dict(filename: str):
    with open(filename, "r") as file:
        data = json.load(file)
    return data


def get_json_structure(filename: str):
    file = open(filename, "r")
    data = json.load(file)

    structure = get_dict_structure(data)

    return structure


def get_dict_structure(data):
    structure = dict()
    if not isinstance(data, (list, dict)):
        return str(type(data)).split("'")[1]

    if isinstance(data, list):
        if not data:
            return []

        if not isinstance(data[0], dict):
            return [get_dict_structure(data[0])]

        max_key = len(flatten_dict(data[0]))
        max_item = data[0]
        for item in data[1:]:
            current_key = len(flatten_dict(item))
            if current_key > max_key:
                max_key = current_key
                max_item = item

        return [get_dict_structure(max_item)]

    for key, value in data.items():
        if isinstance(value, (list, dict)):
            structure[key] = get_dict_structure(data[key])
        else:
            type_str = str(type(value)).split("'")[1]
            structure[key] = type_str
    return structure


def get_dir_json_structure(dir_path, max_files=None):
    structure = dict()
    num = 0
    try:
        filenames = os.listdir(dir_path)
        if max_files is not None:
            filenames = filenames[:max_files]

        for filename in tqdm(filenames, desc="Processing files"):
            filepath = os.path.join(dir_path, filename)
            if not os.path.isfile(filepath):
                continue
            file_structure = get_json_structure(filepath)

            compare_dict(structure, file_structure)
            num += 1
    except KeyboardInterrupt:
        print(f"\nTerminated after {num} files compared")
    finally:
        with open("structure.json", "w") as file:
            json.dump(structure, file, indent=4)


def compare_dict(st, fst):
    if not isinstance(st, dict) or not isinstance(fst, dict):
        return

    for key, value in fst.items():
        if isinstance(value, dict):
            if key not in st or not st[key]:
                st[key] = {}
                compare_dict(st[key], value)
        elif isinstance(value, list):
            if key not in st or not st[key]:
                if value:
                    if isinstance(value[0], dict):
                        st[key] = [{}]
                        compare_dict(st[key][0], value[0])
                    else:
                        st[key] = value
                else:
                    st[key] = value

        else:
            if key not in st or not st[key]:
                st[key] = value


def get_top_level(data):
    for key, value in data.items():
        if not isinstance(value, (dict, list)) and value is not None:
            yield key, value
