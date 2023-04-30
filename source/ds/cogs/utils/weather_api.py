"""
Файл для получения и обработки данных с OpenWeatherAPI
"""
import requests
from .secret.discord_keys import WEATHER_KEY
from datetime import datetime as dt
from deep_translator import GoogleTranslator


# Получение координат по названию города
def get_city_coords(city_name):
    city_name_json = requests.get(f'http://api.openweathermap.org/geo/1.0/'
                                  f'direct?q={city_name}&appid={WEATHER_KEY}'
                                  ).json()[0]
    coords = [city_name_json['lat'], city_name_json['lon']]
    return coords


# Получение данных о текущей погоде
def get_current_weather(coords):
    response_json = requests.get(f'https://api.openweathermap.org/data/2.5/'
                                 f'weather?lat={coords[0]}&lon={coords[1]}&'
                                 f'appid={WEATHER_KEY}&lang=ru&'
                                 f'units=metric').json()
    return response_json


# Получение данных о погоде каждые 3 часа на 5 дней вперед
def get_hourly_weather(coords):
    response_json = requests.get(f'https://api.openweathermap.org/data/2.5/'
                                 f'forecast/?lat={coords[0]}&lon={coords[1]}&'
                                 f'appid={WEATHER_KEY}&lang=ru&'
                                 f'units=metric').json()
    return response_json


# Определение направления ветра по градусам
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


# Перевод с английского на русский
def en_to_ru(text):
    return GoogleTranslator(source='en', target='ru').translate(text=text)


# Вывод данных о текущей погоде
def current_weather(response_json):
    current = []
    wind_deg = int(response_json['wind']['deg'])
    wind_deg = get_wind_deg_name(wind_deg)

    current.append(str(en_to_ru(f"{response_json['name']}, "
                                f"{response_json['sys']['country']}")))
    current_time = dt.utcfromtimestamp(response_json['dt'] +
                                       response_json['timezone'])
    current.append(en_to_ru(current_time.strftime('%A %d/%m/%Y %H:%M:%S')))
    current.append(response_json['weather'][0]['description'].capitalize())
    current.append(response_json['main']['temp'])
    current.append(response_json['main']['feels_like'])
    current.append(response_json['main']['temp_min'])
    current.append(response_json['main']['temp_max'])
    current.append(response_json['main']['humidity'])
    current.append(response_json['main']['pressure'])
    current.append(str(str(response_json['wind']['speed']) + ' м/c ' +
                       wind_deg))
    current.append(response_json['visibility'])
    sunrise_time = dt.utcfromtimestamp(response_json['sys']['sunrise'] +
                                       response_json['timezone'])
    sunset_time = dt.utcfromtimestamp(
        response_json['sys']['sunset'] + response_json['timezone'])
    current.append(sunrise_time.strftime('%d.%m.%Y %H:%M:%S'))
    current.append(sunset_time.strftime('%d.%m.%Y %H:%M:%S'))
    weather_img = response_json['weather'][0]['icon']
    current.append(f'http://openweathermap.org/img/wn/{weather_img}@2x.png')
    current.append(en_to_ru(dt.now().strftime('%A %d/%m/%Y %H:%M:%S')))
    return current


# Вывод данных о погоде каждые 3 часа на 5 дней вперед
def hourly_weather(response_json):
    hourly = [str(en_to_ru(f"{response_json['city']['name']}, "
                           f"{response_json['city']['country']}"))]
    for data in response_json['list']:
        tmp = []
        wind_deg = int(data['wind']['deg'])
        wind_deg = get_wind_deg_name(wind_deg)
        current_time = dt.utcfromtimestamp(data['dt'] +
                                           response_json['city']['timezone'])
        tmp.append(en_to_ru(current_time.strftime('%A %d/%m/%Y %H:%M:%S')))
        tmp.append(data['weather'][0]['description'].capitalize())
        tmp.append(data['main']['temp'])
        tmp.append(data['main']['feels_like'])
        tmp.append(data['main']['temp_min'])
        tmp.append(data['main']['temp_max'])
        tmp.append(data['main']['humidity'])
        tmp.append(data['main']['pressure'])
        tmp.append(str(str(data['wind']['speed']) + ' м/c ' + str(wind_deg)))
        tmp.append(data['visibility'])
        sunrise_time = dt.utcfromtimestamp(response_json['city']['sunrise'] +
                                           response_json['city']['timezone'])
        sunset_time = dt.utcfromtimestamp(
            response_json['city']['sunset'] + response_json['city']['timezone'])
        tmp.append(sunrise_time.strftime('%d.%m.%Y %H:%M:%S'))
        tmp.append(sunset_time.strftime('%d.%m.%Y %H:%M:%S'))
        weather_img = data['weather'][0]['icon']
        tmp.append(f'http://openweathermap.org/img/wn/{weather_img}@2x.png')
        tmp.append(en_to_ru(dt.now().strftime('%A %d/%m/%Y %H:%M:%S')))
        hourly.append(tmp)
    return hourly
