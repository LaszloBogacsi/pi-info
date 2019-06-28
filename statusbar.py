import math
from datetime import datetime

from openweather import get_current_weather_info
from sensor_data_repository import load_current_sensor_data
from tfl_tube_status import get_current_tube_status, central


def refresh_statusbar():
    return refresh_if_necessary()


last_refreshed = datetime.now()

statusbar_data_cache = None


def refresh_if_necessary():
    now = datetime.now()
    global statusbar_data_cache
    if (statusbar_data_cache is None or ((now - last_refreshed).seconds > 300)):
        statusbar_data_cache = reload_data()
        return statusbar_data_cache
    return statusbar_data_cache


def reload_data():
    current_sensor_data = load_current_sensor_data()
    current_temperature = next(value for value in current_sensor_data.values if value["type"] == "temperature")["value"]
    current_weather = get_current_weather_info()
    central_line_status = get_current_tube_status(central)[0]
    statusbar_data = {
        "current_temperature": {
            "indoor": current_temperature,
            "since": convert_to_ago(current_sensor_data.published_time)
        },
        "current_weather": {
            "temp": current_weather.temperature,
            "main": current_weather.main,
            "description": current_weather.description,
            "symbol_url": "http://openweathermap.org/img/w/" + current_weather.icon + ".png"
        },
        "tube_status": {
            "line_name": central_line_status.tube_line.name,
            "status": central_line_status.description
        }
    }
    return statusbar_data


def convert_to_ago(published_time):
    delta = datetime.now() - published_time

    ago = " ago"
    days = delta.days
    day_text = " day" if days == 1 else " days"
    day_display = str(days) + day_text + ago
    if days > 0:
        return day_display

    seconds = delta.seconds
    hour = math.floor(seconds / 3600)
    hour_text = " hour" if hour == 1 else " hours"
    hour_display = str(hour) + hour_text + ago
    if hour > 0:
        return hour_display

    minutes = math.floor(seconds % 3600 / 60)
    minutes_text = " min" if minutes == 1 else " mins"
    minutes_display = str(minutes) + minutes_text + ago
    if minutes > 0:
        return minutes_display

    seconds_text = " sec" if seconds == 1 else " secs"
    seconds_display = str(seconds) + seconds_text + ago
    if seconds > 0:
        return seconds_display
