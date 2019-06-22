import decimal
import json
from datetime import datetime

from flask import Blueprint, render_template, abort, request, make_response
from jinja2 import TemplateNotFound

from humidity_repository import load_humidity_for
from sensors import SENSORS, get_sensor_by_id
from statusbar import refresh_statusbar
from temperature_repository import load_all_temperature, load_temperature_for

sensors = Blueprint('sensors', __name__,
                    template_folder='templates')


@sensors.route('/sensors', defaults={'page': 'index'})
@sensors.route('/sensors/<page>', methods=['GET'])
def show_sensors(page):
    try:
        statusbar = refresh_statusbar()
        return render_template('sensors/%s.html' % page, active='sensors', sensors=SENSORS, statusbar=statusbar)
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
        if sensor is not None:
            sensor_temperature = load_temperature_for(sensor, timerange)
        statusbar = refresh_statusbar()
        return render_template('sensor/index.html', active='sensors',sensor=sensor, temperatures=sensor_temperature, statusbar=statusbar)
    except TemplateNotFound:
        abort(404)


def default_conv(o):
    if isinstance(o, datetime):
        return o.isoformat()
    if isinstance(o, decimal.Decimal):
        dec = decimal.Decimal(o)
        return float(dec)
    return o.__dict__

@sensors.route('/sensor/data')
def get_data():
    sensor_id = int(request.args.get('sensor_id', 100))
    timerange = request.args.get('timerange', 'today')
    int_id = int(sensor_id)
    sensor = get_sensor_by_id(int_id)
    all_temp = load_temperature_for(sensor, timerange)

    resolution_mins = 30
    # get_data_for_resolution(make_minute_resolution_data(all_temp), resolution_mins)

    all_humidity = load_humidity_for(sensor, timerange)
    all_data = {"temperatures": all_temp, "humidities": all_humidity}
    json_string = json.dumps(all_data, default=default_conv)
    response = make_response(json_string)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
