api_key = "92334de0a0f6939c969570a910190823"
north_acton = {
    "lat": "51.523134",
    "lon": "-0.261312"
}
lat = "lat=" + north_acton["lat"]
lon = "&lon=" + north_acton["lon"]
metric_units = "&units=metric"
api = "&APPID=" + api_key
params = lat + lon + metric_units + api
url = "https://api.openweathermap.org/data/2.5/weather?" + params


class CurrentWeather(object):
    def __init__(self, main, description, temperature, icon):
        self.icon = icon
        self.temperature = temperature
        self.description = description
        self.main = main


def create_current_weather(data):
    w = data["weather"][0]
    m = data["main"]
    return CurrentWeather(main=w["main"], description=w["description"], icon=w["icon"], temperature=m["temp"])


def get_current_weather_info() -> [CurrentWeather]:
    try:
        # with request.urlopen(url=url) as response:
        #     data = response.read()
        #     json_weather_data = json.loads(data)
        #     return create_current_weather(json_weather_data)
        return None
    except:
        print("could not connect to openweather api")
        return None
