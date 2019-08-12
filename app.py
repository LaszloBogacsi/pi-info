import os

from flask import Flask

from pi_info.blueprints.home import home
from pi_info.blueprints.lights import lights
from pi_info.blueprints.rooms import rooms
from pi_info.blueprints.sensors import sensors
from pi_info.blueprints.tube_status import tube_status

project_folder = os.path.join((os.path.abspath(os.path.dirname(__file__))), 'pi_info')
template_dir = os.path.join(project_folder, 'templates')
static_dir = os.path.join(project_folder, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.register_blueprint(home)
app.register_blueprint(lights)
app.register_blueprint(sensors)
app.register_blueprint(tube_status)
app.register_blueprint(rooms)


@app.template_filter('formatdatetime')
def format_datetime(value, format="%d %b %Y %I:%M %p"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return value.strftime(format)

