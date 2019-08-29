import decimal
import json
from datetime import datetime, timedelta

from flask import Blueprint, render_template, abort, request, make_response, url_for, current_app, redirect
from jinja2 import TemplateNotFound

from pi_info.data.data_normaliser import get_data_for_resolution, make_minute_resolution_data
from pi_info.data.room import Room
from pi_info.data.sensors import SENSORS, get_sensor_by_id, SensorType
from pi_info.repository.SensorData import SensorData
from pi_info.repository.sensor_data_repository import load_sensor_data_for, load_current_sensor_data
from pi_info.repository.sensor_repository import save_sensor, load_all_sensors
from pi_info.statusbar import refresh_statusbar

sensors = Blueprint('sensors', __name__,
                    template_folder='templates')


@sensors.route('/sensors', defaults={'page': 'status'})
@sensors.route('/sensors/<page>', methods=['GET'])
def show_sensors(page):
    try:
        statusbar = refresh_statusbar()
        buttons = get_buttons(selected=page)
        enriched_with_current_values = [{**get_displayed_sensor_data(load_current_sensor_data(sensor), sensor), **sensor} for
                                        sensor in SENSORS]
        return render_template('sensors/%s.html' % page, active='sensors', sensors=enriched_with_current_values,
                               statusbar=statusbar, buttons=buttons)
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
        statusbar = refresh_statusbar()
        return render_template('sensor/index.html', active='sensors', sensor=sensor, statusbar=statusbar,
                               selected=timerange, api_base_url=current_app.config['API_BASE_URL'])
    except TemplateNotFound:
        abort(404)


@sensors.route('/sensors/new', methods=['GET'])
def new_sensor():
    try:
        sensor_types = [type.value.title() for type in SensorType]
        locations = [room.value.title() for room in Room]
        statusbar = refresh_statusbar()
        return render_template('sensors/new.html', active='sensors', statusbar=statusbar, sensor_types=sensor_types,
                               locations=locations)
    except TemplateNotFound:
        abort(404)


@sensors.route('/sensors/save', methods=['POST'])
def save_new():
    try:
        type = request.form['type'].lower()
        location = request.form['location'].lower()
        name = request.form['name']
        code = request.form['code']
        sampling_rate = request.form['sampling-rate']
        last_id = load_all_sensors()[0].get('id') if len(load_all_sensors()) > 0 else 100
        new_id = last_id + 1
        sensor_to_save = {
            "id": new_id,
            "type": type,
            "name": name,
            "code": code,
            "sampling_rate": sampling_rate,
            "location": location
        }
        save_sensor(sensor_to_save)
        return redirect(url_for('sensors.show_sensors', _method='GET'))
    except TemplateNotFound:
        abort(404)


def get_unit_by_type(type):
    type_unit = {
        'temperature': '°C',
        'humidity': '%'
    }
    return type_unit.get(type, '')


def get_displayed_sensor_data(sensor_data, sensor):
    if sensor_data is not None:
        display_data = [
            dict(
                formatted_value="{} {}".format(value['value'], get_unit_by_type(value['type'])),
                type=value['type'].capitalize()
            ) for value in sensor_data.values
        ]
    else:
        display_data = [{}]
        sensor_data = SensorData.get_empty()
    is_active = dict(is_active=sensor_data.published_time > datetime.now() - timedelta(minutes=(10 * sensor['sampling_rate_mins'])))

    return dict(data=sensor_data, display_data=display_data, **is_active)


def get_buttons(selected):
    status_button = {"url": url_for('sensors.show_sensors', page='status'),
                     "active_status": 'active' if selected == 'status' else '', "icon_type": '',
                     "button_text": "STATUS"}
    list_button = {"url": url_for('sensors.show_sensors', page='list'),
                   "active_status": 'active' if selected == 'list' else '', "icon_type": 'list icon',
                   "button_text": "LIST"}
    graph_button = {"url": url_for('sensors.show_sensors', page='graph'),
                    "active_status": 'active' if selected == 'graph' else '', "icon_type": 'chart bar icon',
                    "button_text": "GRAPH"}
    return [status_button, list_button, graph_button]


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
        "today": 30,  # every 30 mins, 48 datapoints
        "week": 360,  # every 6 hours, 28 datapoints
        "month": 1440,  # every 1 day, 28-31 datapoints
        "year": 10080,  # every week, 52 datapoints
        "all": 10080
    }
    int_id = int(sensor_id)
    sensor = get_sensor_by_id(int_id)
    all_sensor_data = load_sensor_data_for(sensor, timerange)

    resolution_mins = timerange_resolution_mins.get(timerange)
    all_sensor_data_by_resolution = get_data_for_resolution(make_minute_resolution_data(all_sensor_data),
                                                            resolution_mins)
    outbound_all_sensor_data_by_resolution = list(map(lambda d: datetime_key_fix(d), all_sensor_data_by_resolution))
    all_data = {"sensor_data": outbound_all_sensor_data_by_resolution}

    json_string = json.dumps(all_data, default=default_conv)
    response = make_response(json_string)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
