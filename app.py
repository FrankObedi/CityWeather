from flask import Flask, render_template
from flask import request
import requests
from forecaset import get_forecast
from currentWeather import get_current
import os
from dotenv import load_dotenv


def configure():
    load_dotenv()


app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def home():
    configure()  # load api key

    city = None

    if request.method == 'POST':
        city = request.form.get('city')

    if city == None:
        return render_template('welcome.html')

    # get current data
    weather_api = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'
    weather_response = requests.get(weather_api.format(
        city, os.getenv('API_KEY'))).json()

    # get forecast data
    forecast_apa = 'https://api.openweathermap.org/data/2.5/forecast?q={}&appid={}&units=metric'
    forecast_response = requests.get(forecast_apa.format(
        city, os.getenv('API_KEY'))).json()

    # erro message when city is not found
    if forecast_response.get('cod') != '200' or weather_response.get('cod') != 200:
        return render_template('404.html', city=city)

    current_weather = get_current(weather_response, os.getenv('API_KEY'))
    forecast = get_forecast(forecast_response)

    return render_template('results.html', forecast=forecast, current_weather=current_weather)


if __name__ == '__main__':
    app.run()
