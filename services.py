import json


def get_settings():
    with open('settings.json', "r", encoding='utf-8') as settings_file:
        return json.load(settings_file)


def change_settings(data):
    if isinstance(data, str):
        data = json.loads(data)
    with open('settings.json', "w", encoding='utf-8') as settings_file:
        json.dump(data, settings_file)


def change_settings_field(field, value):
    data = get_settings()
    data[field] = value
    with open('settings.json', "w", encoding='utf-8') as settings_file:
        json.dump(data, settings_file)


def normalize_number(number):
    number = number.replace("+", "")
    number = "".join([c for c in number if c.isdigit()])
    if number[0] == "8":
        number = number.replace("8", "7", 1)
    return number
