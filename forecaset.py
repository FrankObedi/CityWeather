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

    forecast = Forecast()
    # print(response)
    current_date = response['list'][0].get('dt_txt').split(' ')[0]

    # time stemps counter
    time_stamps_counter = 0
    prev = current_date

    # set default min and max temperature variables
    min_temp = 999
    max_temp = 0

    # get todays date to compare with first time stamp in api response
    today = str(datetime.datetime.today())

    start = 1
    if today != current_date:
        start = 0
    rain_icon = None
    for i in range(start, len(response['list'])):
        # compare to see it time stemp is from same date
        date = response['list'][i]['dt_txt'].split(' ')[0]
        if date == prev:
            # find min temp
            if response['list'][i]['main']['temp'] < min_temp:
                min_temp = response['list'][i]['main']['temp']
            # find max temp
            if response['list'][i]['main']['temp'] > max_temp:
                max_temp = response['list'][i]['main']['temp']
                icon_code = response['list'][i]['weather'][0]['icon']
                icon = f'https://openweathermap.org/img/wn/{icon_code}@2x.png'

            if response['list'][i]['weather'][0]['icon'] == '10d':
                rain_icon_code = response['list'][i]['weather'][0]['icon']
                rain_icon = f'https://openweathermap.org/img/wn/{rain_icon_code}@2x.png'
            # increment time stamp counter
            time_stamps_counter += 1

            # check if we went through all time stamps of give date
            if time_stamps_counter == 7:
                if rain_icon != None:
                    icon = rain_icon
                if time_stamps_counter == 7:

                    # create a new day object and add it to forecast object
                    forecast.add_day(
                        Day(get_day_time(date, True), round(max_temp), round(min_temp), icon))

                    # reset time stamps counter
                    time_stamps_counter = 0

        # if date is not same as previous one then a new time date has been found
        # now we want to find the min_temp and max_temp from the new date's time stamps
        else:
            min_temp = response['list'][i]['main']['temp']
            max_temp = response['list'][i]['main']['temp']
        prev = response['list'][i]['dt_txt'].split(' ')[0]

    print(forecast.length)
    return forecast
