import json


def json_to_dict(filename: str):
    with open(filename, "r") as file:
        return json.load(file)


def get_json_structure(filename: str):
    file = open(filename, "r")
    data = json.load(file)

    structure = get_dict_structure(data)

    with open(filename.removesuffix(".json") + "_structure.json", "w") as file:
        json.dump(structure, file, indent=4)


def get_dict_structure(data):
    structure = dict()
    if not isinstance(data, (list, dict)):
        return str(type(data)).split("'")[1]

    if isinstance(data, list):
        return [get_dict_structure(data[0])] if data else []

    for key, value in data.items():
        if isinstance(value, (list, dict)):
            structure[key] = get_dict_structure(data[key])
        else:
            type_str = str(type(value)).split("'")[1]
            structure[key] = type_str
    return structure


def get_top_level(data):
    for key, value in data.items():
        if not isinstance(value, (dict, list)):
            yield key, value
