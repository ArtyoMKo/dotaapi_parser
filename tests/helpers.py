import json


def read_test_data():
    with open("tests/test_data.json", "r", encoding="utf-8") as read_file:
        data = json.load(read_file)
    return data
