import decimal
import json

from datetime import datetime
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from temperature_repository import load_all_temperature

sensor_info = Blueprint('sensor_info', __name__,
                        template_folder='templates')


@sensor_info.route('/sensorinfo', defaults={'page': 'index'})
@sensor_info.route('/sensorinfo/<page>')
def show(page):
    try:
        all_temperature = load_all_temperature()
        return render_template('sensor_info/%s.html' % page, temperatures=all_temperature)
    except TemplateNotFound:
        abort(404)


def default_conv(o):
    if isinstance(o, datetime):
        return o.isoformat()
    if isinstance(o, decimal.Decimal):
        dec = decimal.Decimal(o)
        return float(dec)
    return o.__dict__


@sensor_info.route('/sensorinfo/data')
def get_data():
    all_temp = load_all_temperature()
    json_string = json.dumps(all_temp, default=default_conv)
    return json_string
