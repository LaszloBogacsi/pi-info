import datetime
import json
from urllib import request

from enum import Enum

from dateutil.relativedelta import relativedelta

app_id = "e52f129c"
api_key = "2a6a3161872d2a2ae3863ac26ea718d7"

api = "app_key=" + api_key + "&app_id=" + app_id
params = api
url = "https://api.tfl.gov.uk/line/mode/tube/status"
one_line_url = lambda line_id: "https://api.tfl.gov.uk/Line/" + line_id + "/Status?" + params
all_lines_url = "https://api.tfl.gov.uk/Line/Mode/tube/Status?" + params
future_status_one_line = lambda line, from_date, to_date: "https://api.tfl.gov.uk/Line/" + line + "/Status/" + from_date +"/to/"+ to_date + "?" + params


class CurrentStatus(object):
    def __init__(self, tube_line, description, reason='', disruption_category='', additional_info=''):
        self.tube_line = tube_line
        self.additional_info = additional_info
        self.disruption_category = disruption_category
        self.reason = reason
        self.description = description


def get_data_for_line(line, data):
    return next((x for x in data if x["id"] == line.id.val), None)


def create_current_tube_status(data, all_lines):
    return list((map(lambda line: create_line_info(get_data_for_line(line, data), line)[0], all_lines)))


def make_statuses(status, line):
    disruption = status.get('disruption', {})
    return CurrentStatus(
        tube_line=line,
        description=status.get("statusSeverityDescription", ''),
        reason=status.get("reason", ''),
        disruption_category=disruption.get('categoryDescription', ''),
        additional_info=disruption.get('additionalInfo', '')
    )


def create_line_info(line_info, tube_line):
    line_statuses = line_info.get("lineStatuses", [{}])
    return list(map(lambda status: make_statuses(status, tube_line), line_statuses))


class Tube(Enum):
    def __init__(self, val):
        self.val = val

    BAKERLOO = 'bakerloo',
    CENTRAL = ('central'),
    CIRCLE = 'circle',
    DISTRICT = 'district',
    HAMMERSMITH_AND_CITY = 'hammersmith-city',
    JUBILEE = 'jubilee',
    METROPOLITAN = 'metropolitan',
    NORTHERN = 'northern',
    PICCADILLY = 'piccadilly',
    VICTORIA = 'victoria',
    WATERLOO_AND_CITY = 'waterloo-city'


class TubeLine():
    def __init__(self, id, name, colour_code):
        self.colour_code = colour_code
        self.name = name
        self.id = id


bakerloo = TubeLine(Tube.BAKERLOO, "Bakerloo", "#B36305")
central = TubeLine(Tube.CENTRAL, "Central", "#E32017")
circle = TubeLine(Tube.CIRCLE, "Circle", "#FFD300")
district = TubeLine(Tube.DISTRICT, "District", "#00782A")
hammersmith_and_city = TubeLine(Tube.HAMMERSMITH_AND_CITY, "Hammersmith & City", "#F3A9BB")
jubilee = TubeLine(Tube.JUBILEE, "Jubilee", "#A0A5A9")
metropolitan = TubeLine(Tube.METROPOLITAN, "Metropolitan", "#9B0056")
northern = TubeLine(Tube.NORTHERN, "Northern", "#000000")
piccadilly = TubeLine(Tube.PICCADILLY, "Piccadilly", "#003688")
victoria = TubeLine(Tube.VICTORIA, "Victoria", "#0098D4")
waterloo_and_city = TubeLine(Tube.WATERLOO_AND_CITY, "Waterloo & city", "#95CDBA")

TUBE_LINES_ORDERED = [bakerloo, central, circle, district, hammersmith_and_city, jubilee, metropolitan,
                      northern, piccadilly, victoria, waterloo_and_city]


def get_current_tube_status(tube_line):
    with request.urlopen(url=one_line_url(tube_line.id.val)) as response:
        data = response.read()
        json_tube_data = json.loads(data)
        return create_line_info(json_tube_data[0], tube_line)


def get_all_current_tube_status():
    with request.urlopen(url=all_lines_url) as response:
        data = response.read()
        json_tube_data = json.loads(data)
        return create_current_tube_status(json_tube_data, TUBE_LINES_ORDERED)


def get_future_status_for(tube_line):
    today = datetime.date.today()
    two_weeks_from_now = str(today + relativedelta(weeks=0))
    two_month_from_now = str((today + relativedelta(months=5)))
    with request.urlopen(url=future_status_one_line(tube_line.id.val, two_weeks_from_now, two_month_from_now)) as response:
        data = response.read()
        json_tube_data = json.loads(data)
        return create_line_info(json_tube_data[0], tube_line)
