import json

def read_test_data():
    with open('tests/test_data.json', 'r') as rf:
        data = json.load(rf)
    return data

