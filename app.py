import json
import logging
import os

from flask import Flask

from pi_info.Credentials import Credentials
from pi_info.scheduling.Scheduler import Scheduler


def get_mqtt_client():
    return mqtt_client


def get_scheduler():
    return scheduler


from pi_info.blueprints.home import home
from pi_info.blueprints.lights import lights, Weekday
from pi_info.blueprints.rooms import rooms
from pi_info.blueprints.sensors import sensors
from pi_info.blueprints.tube_status import tube_status
from pi_info.mqtt.MqttClient import MqttClient
from pi_info.mqtt.message_handler import MessageHandler
from pi_info.repository import init_app_db, Schedule
from pi_info.repository.sensor_data_repository import save_sensor_data
from pi_info.repository.schedule_repository import load_all_schedules

logger = logging.getLogger('app')

root_folder = os.path.abspath(os.path.dirname(__file__))
project_folder = os.path.join(root_folder, 'pi_info')
template_dir = os.path.join(project_folder, 'templates')
static_dir = os.path.join(project_folder, 'static')

mqtt_client = None
scheduler = Scheduler()


def create_app(config_file='config.cfg'):
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir, root_path=root_folder)
    app.config.from_pyfile(config_file)
    with app.app_context():
        if app.config['ONLINE']:
            global mqtt_client
            mqtt_client = init_mqtt(app)
        init_app_db(app)
    init_task_scheduler(load_all_schedules())
    app.register_blueprint(home)
    app.register_blueprint(lights)
    app.register_blueprint(sensors)
    app.register_blueprint(tube_status)
    app.register_blueprint(rooms)

    @app.template_filter('formatdatetime')
    def format_datetime(value, format="%d %b %Y %I:%M %p"):
        """Format a date time to (Default): d Mon YYYY HH:MM P"""
        if value is None:
            return "-"
        return value.strftime(format)

    @app.template_filter('toWeekday')
    def to_weekday(value):
        if value is None:
            return "-"
        try:
            days = value.split(',')
            if len(days) == len(Weekday):
                return 'Everyday'
            if len(days) == 5 and all(str(d) in days for d in range(1, 6)):
                return 'Weekdays'
            if len(days) == 2 and all(str(d) in days for d in range(6, 8)):
                return 'Weekends'
            return ", ".join([Weekday(int(day)).name for day in days])
        except:
            return value

    return app


def init_mqtt(app) -> MqttClient:
    handlers = [MessageHandler('sensor/temperature', save_sensor_data)]
    return MqttClient(Credentials(app.config['MQTT_USERNAME'], app.config['MQTT_PASSWORD']), app.config['MQTT_HOST'], handlers)


def create_action(status: str, device_ids: str, client, publisher):
    device_ids_arr = json.loads(device_ids)
    actions = []
    for device_id in device_ids_arr:
        def create_payload_and_publish():
            payload = "{{\"status\":\"{}\",\"device_id\":\"{}\"}}".format(status, device_id)
            publisher(client, "switch/relay", payload)
        actions.append(create_payload_and_publish)
    return actions


def init_task_scheduler(schedules: [Schedule]):
    logger.debug('Initializing {} tasks'.format(len(schedules)))

    for schedule in schedules:
        def publisher(client, topic, payload):
            if client is not None:
                client.publish(topic=topic, payload=payload)
            else:
                logger.error('can not publish message, client is not defined')

        scheduler.schedule_task_from_db(schedule, create_action(schedule.status, str(schedule.device_id), get_mqtt_client(), publisher))
