import math
from datetime import datetime

from pi_info.data.lights import LIGHTS, LightStatus
from pi_info.repository.sensor_data_repository import load_current_sensor_data
from pi_info.third_party.openweather import get_current_weather_info
from pi_info.third_party.tfl_tube_status import get_current_tube_status, central

last_refreshed = datetime.now()

statusbar_data_cache = None


def refresh_statusbar():
    always_refresh()
    return refresh_if_necessary()


def refresh_if_necessary():
    now = datetime.now()
    global statusbar_data_cache
    if (statusbar_data_cache is None or ((now - last_refreshed).seconds > 300)):
        statusbar_data_cache = reload_data()
    return statusbar_data_cache


def always_refresh():
    if statusbar_data_cache is not None:
        statusbar_data_cache["lights_status"] = {"is_on": get_any_light_status()}


def get_current_sensor_data(data):
    data_row = next((value for value in data.values if value["type"] == "temperature"), None) if data is not None else None
    current_temp = data_row["value"] if data_row is not None else "N/A"
    time = convert_to_ago(data.published_time) if data_row is not None else "N/A"
    return {
        "current_temp": current_temp,
        "time": time
    }


def get_current_weather(data):
    temp = data.temperature if data is not None else "N/A"
    main = data.main if data is not None else "N/A"
    description = data.description if data is not None else "N/A"
    sym_url = data.icon if data is not None else ""
    return {
        "temp": temp,
        "main": main,
        "description": description,
        "symbol_url": "http://openweathermap.org/img/w/" + sym_url + ".png"
    }


def get_any_light_status():
    return True if next((light for light in LIGHTS if light["current_status"] == LightStatus.ON), None) is not None else False


def reload_data():
    current_sensor_data = get_current_sensor_data(load_current_sensor_data())
    current_weather = get_current_weather(get_current_weather_info())
    central_line_status = get_current_tube_status(central)[0]
    is_any_light_on = get_any_light_status()
    statusbar_data = {
        "current_temperature": {
            "indoor": current_sensor_data["current_temp"],
            "since": current_sensor_data["time"]
        },
        "current_weather": {
            "temp": current_weather["temp"],
            "main": current_weather["main"],
            "description": current_weather["description"],
            "symbol_url": current_weather["symbol_url"]
        },
        "tube_status": {
            "line_name": central_line_status.tube_line.name,
            "status": central_line_status.description
        },
        "lights_status": {
            "is_on": is_any_light_on
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
