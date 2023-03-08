import json


with open('telegram/assets/secure/config.json') as file:
    data = json.load(file)
    TOKEN = data['token']
