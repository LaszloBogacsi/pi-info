from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

sensor_info = Blueprint('sensor_info', __name__,
                        template_folder='templates')


@sensor_info.route('/sensorinfo', defaults={'page': 'index'})
@sensor_info.route('/sensorinfo/<page>')
def show(page):
    try:
        stuff = "My stuff"
        return render_template('sensor_info/%s.html' % page, stuff=stuff)
    except TemplateNotFound:
        abort(404)