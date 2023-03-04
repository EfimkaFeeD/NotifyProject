import requests
from discord_keys import API_KEY

# Получаем координаты по названию города
cityname_response = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q=Санкт-Петербург,RU&appid={API_KEY}')
city_name_json = cityname_response.json()[0]
coords = [city_name_json['lat'], city_name_json['lon']]

# Получаем данные о погоде
response_json = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={coords[0]}&lon={coords[1]}&appid={API_KEY}&lang=ru&units=metric').json()

for key, value in response_json.items():
    print(f'{key}: {value}')

print('Погода:', response_json['weather'][0]['description'].capitalize())
print('Температура:', response_json['main']['temp'], '°C')
print('Ощущается как:', response_json['main']['feels_like'], '°C')
print('Минимальная температура:', response_json['main']['temp_min'], '°C Максимальная температура:', response_json['main']['temp_max'], '°C')
print('Влажность:', response_json['main']['humidity'], '%')
print('Давление:', response_json['main']['pressure'], 'мм рт. ст.')
# Определяем направление ветра по градусам
wind_deg = int(response_json['wind']['deg'])
def get_wind_deg_name(wind):
    if wind in range(345, 361) or wind in range(0, 16):
        wind = 'северный'
    elif wind in range(16, 61):
        wind = 'северо-восточный'
    elif wind in range(61, 106):
        wind = 'восточный'
    elif wind in range(106, 151):
        wind = 'юго-восточный'
    elif wind in range(151, 196):
        wind = 'южный'
    elif wind in range(196, 241):
        wind = 'юго-западный'
    elif wind in range(241, 286):
        wind = 'западный'
    elif wind in range(286, 321):
        wind = 'северо-западный'
    return wind
wind_deg = get_wind_deg_name(wind_deg)
print('Ветер:', response_json['wind']['speed'], 'м/c', wind_deg)
print('Видимость:', response_json['visibility'], 'м')
weather_img = response_json['weather'][0]['icon']
print('Иконка:')
print(f'http://openweathermap.org/img/wn/{weather_img}.png')
