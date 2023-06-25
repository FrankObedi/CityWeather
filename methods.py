# helper functions module
import time
import datetime


def get_day_time(date_time_txt, just_day=False, just_time=False, with_month=False):
    date_time = date_time_txt.split(' ')
    year, mon, day = (int(x) for x in date_time[0].split('-'))
    date_obj = datetime.date(year, mon, day)
    day = date_obj.strftime("%A")

    # want the day to include day of week, month and day of month
    if with_month:
        day = f'{date_obj.strftime("%A")[:3]}, {date_obj.strftime("%B")[:3]} {date_obj.strftime("%d")}'

    # only want day of the week
    if just_day:
        return day

    time_24hr = date_time[1]
    t = time.strptime(time_24hr, "%H:%M:%S")
    time_12hr = time.strftime("%I:%M %p", t)
    day_time = f"{day}, {time_12hr}"

    # only want time in 12 hour format
    if just_time:
        return time_12hr

    # want day of week, month, day of month and time in 12 hr format
    return day_time
