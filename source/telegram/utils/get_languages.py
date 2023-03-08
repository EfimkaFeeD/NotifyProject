import json
import os


def get():
    response = {}
    for file in list(os.walk('telegram/assets/languages'))[0][2]:
        with open(f'telegram/assets/languages/{file}', encoding='utf-8') as json_file:
            data = json.load(json_file)
            response[data['meta']['name']] = data['data']
    return response
