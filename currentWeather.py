import requests
from methods import get_day_time


class Current(object):
    def __init__(self, location: str, temp: int, feel: str, humidity: int, wind: int, icon: str, condition: str, air_quality: int):
        self.temp = temp
        self.feel = feel
        self.humidity = humidity
        self.wind = wind
        self.icon = icon
        self.condition = condition
        self.air_quality = air_quality
        self.location = location


def get_current(weather_response: str, API_KEY: str):

    # get long and lat coords
    lon = weather_response['coord']['lon']
    lat = weather_response['coord']['lat']

    # air quality api
    air_quality_api = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}'
    air_quality_response = requests.get(air_quality_api).json()

    # time api
    time_api = f'http://api.timezonedb.com/v2.1/get-time-zone?key=ZX5YGXBU5BOS&format=json&by=position&lat={lat}&lng={lon}'
    time_api_response = requests.get(time_api).json()

    current_time = ''
    # check status of time api response
    if time_api_response['status'] == "OK":
        # get time and convert time to 24hr format
        current_time = get_day_time(
            time_api_response['formatted'], with_month=True)

    air_quality = ''
    # check if error in the response
    if air_quality_response.get('cod') and air_quality_response.get('cod') != 200:
        air_quality = 'unavailable'
    else:
        air_quality = air_quality_response['list'][0]['main']['aqi']

    # extract data
    # location info
    location = {"city": weather_response['name'], "country": weather_response['sys']
                ['country'], "day_time": current_time}

    # current weather info
    temp = int(weather_response['main']['temp'])
    feel = int(weather_response['main']['feels_like'])
    humidity = int(weather_response['main']['humidity'])
    wind = int((weather_response['wind']['speed']) * 3.6)

    icon_code = weather_response['weather'][0]['icon']
    icon = f'https://openweathermap.org/img/wn/{icon_code}@2x.png'
    condition = weather_response['weather'][0]['description']

    # create current weather object
    current_weather = Current(location, temp, feel, humidity,
                              wind, icon, condition, air_quality)

    return current_weather
