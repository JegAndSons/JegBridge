import json

def write_json_to_file(filename, data):
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)