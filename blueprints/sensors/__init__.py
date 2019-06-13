import decimal
import json
from datetime import datetime

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from sensors import SENSORS
from statusbar import refresh_statusbar
from temperature_repository import load_all_temperature

sensors = Blueprint('sensors', __name__,
                    template_folder='templates')


@sensors.route('/sensors', defaults={'page': 'index'})
@sensors.route('/sensors/<page>')
def show_sensors(page):
    try:
        statusbar = refresh_statusbar()
        return render_template('sensors/%s.html' % page, sensors=SENSORS, statusbar=statusbar)
    except TemplateNotFound:
        abort(404)


@sensors.route('/sensors/sensor', defaults={'page': 'index'})
@sensors.route('/sensors/sensor/<page>')
def show_sensor(page):
    try:
        all_temperature = load_all_temperature()
        statusbar = refresh_statusbar()
        return render_template('sensor/%s.html' % page, temperatures=all_temperature, statusbar=statusbar)
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
    all_temp = load_all_temperature()
    json_string = json.dumps(all_temp, default=default_conv)
    return json_string
