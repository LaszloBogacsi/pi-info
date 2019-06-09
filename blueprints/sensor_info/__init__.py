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