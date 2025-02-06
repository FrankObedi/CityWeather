import datetime
from methods import get_day_time


class Day(object):
    def __init__(self, day: str, max_temp: int, min_temp: int, icon: str):
        self.day = day
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.icon = icon


class Forecast(object):
    def __init__(self, day=None):
        self.days = [day]
        self.length = 0
        if day != None:
            self.length = 1

    def add_day(self, day):
        if self.length == 0:
            self.days[0] = day
        else:
            self.days.append(day)
        self.length += 1


def get_forecast(response):
    """
    Processes the weather forecast response from OpenWeatherMap API and creates a Forecast object.

    Args:
    response (dict): The response dictionary from the OpenWeatherMap forecast API.

    Returns:
    Forecast: A Forecast object containing Day objects for each day of the forecast.
    """
    
    forecast = Forecast()
    current_date = response['list'][0].get('dt_txt').split(' ')[0]    
    time_stamps_counter = 0
    prev = current_date    
    min_temp = 999
    max_temp = 0
    icon = "https://openweathermap.org/img/wn/01d@2x.png"  # Default sunny icon    
    today = str(datetime.datetime.today()) # Get the current date and time 
    start = 1
    rain_icon = None # Variable to store rain icon URL if present


    # Start from the second item if the forecast's date is not today's date
    if today != current_date:
        start = 0
    

    for i in range(start, len(response['list'])):
        date = response['list'][i]['dt_txt'].split(' ')[0]
        if date == prev: # If the date matches the previous one, process the data
            # Find the min and max temperatures
            if response['list'][i]['main']['temp'] < min_temp:
                min_temp = response['list'][i]['main']['temp']

            if response['list'][i]['main']['temp'] > max_temp or 'icon' not in locals():
                max_temp = response['list'][i]['main']['temp']
                icon_code = response['list'][i]['weather'][0]['icon']
                icon = f'https://openweathermap.org/img/wn/{icon_code}@2x.png'

             # Check if the icon represents rain, and update rain_icon if necessary
            if response['list'][i]['weather'][0]['icon'] == '10d':
                rain_icon_code = response['list'][i]['weather'][0]['icon']
                rain_icon = f'https://openweathermap.org/img/wn/{rain_icon_code}@2x.png'

            time_stamps_counter += 1 # Increment the counter for the time stamps processed

            if time_stamps_counter == 7: # If 7 time stamps are processed (daily forecast data)
                if rain_icon is not None: # If rain is detected, use the rain icon
                    icon = rain_icon

                # Add the current day's forecast to the forecast object
                forecast.add_day(
                    Day(get_day_time(date, True), round(max_temp), round(min_temp), icon)
                )

                time_stamps_counter = 0 # Reset the counter for the next day

        else: # If the date has changed, start processing a new date
            min_temp = response['list'][i]['main']['temp']
            max_temp = response['list'][i]['main']['temp']
            icon_code = response['list'][i]['weather'][0]['icon']
            icon = f'https://openweathermap.org/img/wn/{icon_code}@2x.png'

        prev = response['list'][i]['dt_txt'].split(' ')[0] # Update the previous date

    return forecast # Return the created Forecast object containing all processed days

