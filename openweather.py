import math
from datetime import datetime
from temperature_repository import load_current_temperature


def refresh_statusbar():
    current_temperature = load_current_temperature()
    statusbar_data = {
        "current_temperature": {
            "indoor": current_temperature.temperature,
            "since": convert_to_ago(current_temperature.published_time)
        },
        "current_weather": {
            "temp": 20,
            "symbol": '',
            "since": ''
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

