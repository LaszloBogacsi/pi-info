from enum import Enum

from flask import Blueprint, render_template, abort, request, redirect, url_for, json
from jinja2 import TemplateNotFound
from sensors import Room
from statusbar import refresh_statusbar
lights = Blueprint('lights', __name__,
                  template_folder='templates')
client = None


def set_message_client(c):
    global client
    client = c


class LightType(Enum):
    TABLE_LAMP = 'table_lamp'


class LightStatus(Enum):
    ON = 'ON'
    OFF = 'OFF'

light1 = {"light_id": "1", "name": "Light 1", "location": Room.LIVING_ROOM.value, "type": LightType.TABLE_LAMP, "current_status": LightStatus.OFF}
light2 = {"light_id": "2", "name": "Light 2", "location": Room.LIVING_ROOM.value, "type": LightType.TABLE_LAMP, "current_status": LightStatus.OFF}
LIGHTS = [light1, light2]

@lights.route('/lights', defaults={'page': 'index'})
@lights.route('/lights/<page>', methods=['GET'])
def show_lights(page):
    light_id = request.args.get('light_id', None)
    status = request.args.get('status')
    if light_id is not None:
        next(light for light in LIGHTS if light["light_id"] == light_id)["current_status"] = LightStatus(status)
    try:
        statusbar = refresh_statusbar()
        return render_template('lights/%s.html' % page, active='lights', lights=LIGHTS, statusbar=statusbar)
    except TemplateNotFound:
        abort(404)


def publish(topic, payload):
    if client is not None:
        client.publish(topic=topic, payload=payload)
    else:
        print("can not publish message")


@lights.route('/lights/light')
def light_status():
    light_id = request.args.get('light_id', "1")
    status = request.args.get('status', 'OFF')
    status = "ON" if status == "OFF" else "OFF"
    payload = "{\"status\":\"" + status + "\",\"relay_id\":\"" + light_id + "\"}"
    topic = "switch/relay"
    publish(topic, payload)
    return redirect(url_for('lights.show_lights', status=status, light_id=light_id))