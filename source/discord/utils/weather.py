import requests
from discord_keys import API_KEY

# Получаем координаты по названию города
cityname_response = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q=Санкт-Петербург,RU&appid={API_KEY}')
city_name_json = cityname_response.json()[0]
coords = [city_name_json['lat'], city_name_json['lon']]

# Получаем данные о погоде
response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={coords[0]}&lon={coords[1]}&appid={API_KEY}&lang=ru&units=metric')
response_json = response.json()

for key, value in response_json.items():
    print(f'{key}: {value}')

print('Тип погоды:', response_json['weather'][0]['description'].capitalize())
print('Температура:', response_json['main']['temp'], '°C')
print('Ощущается как:', response_json['main']['feels_like'], '°C')
print('Минимальная температура:', response_json['main']['temp_min'], '°C Максимальная температура:', response_json['main']['temp_max'], '°C')
print('Влажность:', response_json['main']['humidity'], '%')
print('Давление:', response_json['main']['pressure'], 'мм рт. ст.')
print('Ветер:', response_json['wind']['speed'], 'м/c', response_json['wind']['deg']) #TODO написать логику направления ветра по градусу
print('Видимость:', response_json['visibility'], 'м')
weather_img = response_json['weather'][0]['icon']
print('Иконка:')
print(f'http://openweathermap.org/img/wn/{weather_img}.png')
