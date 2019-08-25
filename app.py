import os

from flask import Flask, g

from pi_info.Credentials import Credentials


def get_mqtt_client():
    return mqtt_client


from pi_info.blueprints.home import home
from pi_info.blueprints.lights import lights
from pi_info.blueprints.rooms import rooms
from pi_info.blueprints.sensors import sensors
from pi_info.blueprints.tube_status import tube_status
from pi_info.mqtt.MqttClient import MqttClient
from pi_info.mqtt.message_handler import MessageHandler
from pi_info.repository import init_app_db
from pi_info.repository.sensor_data_repository import save_sensor_data

root_folder = os.path.abspath(os.path.dirname(__file__))
project_folder = os.path.join(root_folder, 'pi_info')
template_dir = os.path.join(project_folder, 'templates')
static_dir = os.path.join(project_folder, 'static')

mqtt_client = None


def create_app(config_file='config.cfg'):
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir, root_path=root_folder)
    app.config.from_pyfile(config_file)
    with app.app_context():
        if app.config['ONLINE']:
            global mqtt_client
            mqtt_client = init_mqtt(app)
        init_app_db(app)
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

    return app


def init_mqtt(app) -> MqttClient:
    handlers = [MessageHandler('sensor/temperature', save_sensor_data)]
    if 'mqtt_client' not in g:
        return MqttClient(Credentials(app.config['MQTT_USERNAME'], app.config['MQTT_PASSWORD']), app.config['MQTT_HOST'], handlers)
