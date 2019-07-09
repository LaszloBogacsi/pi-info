import decimal
import json
from datetime import datetime

from flask import Blueprint, render_template, abort, request, make_response
from jinja2 import TemplateNotFound

from data.data_normaliser import get_data_for_resolution, make_minute_resolution_data
from sensor_data_repository import load_sensor_data_for
from sensors import SENSORS, get_sensor_by_id
from statusbar import refresh_statusbar

sensors = Blueprint('sensors', __name__,
                    template_folder='templates')


@sensors.route('/sensors', defaults={'page': 'status'})
@sensors.route('/sensors/<page>', methods=['GET'])
def show_sensors(page):
    try:
        statusbar = refresh_statusbar()
        return render_template('sensors/%s.html' % page, active='sensors', sensors=SENSORS, statusbar=statusbar, selected=page)
    except TemplateNotFound:
        abort(404)


@sensors.route('/sensors/sensor', methods=['GET'])
def show_sensor():
    sensor_id = int(request.args.get('sensor_id', 100))
    timerange = request.args.get('timerange', 'today')
    try:
        sensor = None
        if sensor_id is None:
            print('invalid sensor id')
        else:
            int_id = int(sensor_id)
            sensor = get_sensor_by_id(int_id)
        # if sensor is not None:
            # sensor_temperature = next(value.values for value in load_sensor_data_for(sensor, timerange) if value["type"] == "temperature")["value"]
        statusbar = refresh_statusbar()
        return render_template('sensor/index.html', active='sensors',sensor=sensor, statusbar=statusbar, selected=timerange)
    except TemplateNotFound:
        abort(404)


def default_conv(o):
    if isinstance(o, datetime):
        return o.isoformat()
    if isinstance(o, decimal.Decimal):
        dec = decimal.Decimal(o)
        return float(dec)
    return o.__dict__


def datetime_key_fix(o):
    if isinstance(o, dict):
        for key in o:
            o[key] = datetime_key_fix(o[key])
            if type(key) is datetime:
                o[key.isoformat()] = o[key]
                del o[key]
    return o


@sensors.route('/sensor/data')
def get_data():
    sensor_id = int(request.args.get('sensor_id', 100))
    timerange = request.args.get('timerange', 'today')
    timerange_resolution_mins = {
        "today": 30, # every 30 mins, 48 datapoints
        "week": 360, # every 6 hours, 28 datapoints
        "month": 1440, # every 1 day, 28-31 datapoints
        "year": 10080 # every week, 52 datapoints
    }
    int_id = int(sensor_id)
    sensor = get_sensor_by_id(int_id)
    all_sensor_data = load_sensor_data_for(sensor, timerange)

    resolution_mins = timerange_resolution_mins.get(timerange)
    all_sensor_data_by_resolution = get_data_for_resolution(make_minute_resolution_data(all_sensor_data), resolution_mins)
    outbound_all_sensor_data_by_resolution = list(map(lambda d: datetime_key_fix(d), all_sensor_data_by_resolution))
    all_data = {"sensor_data": outbound_all_sensor_data_by_resolution}

    json_string = json.dumps(all_data, default=default_conv)
    response = make_response(json_string)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

