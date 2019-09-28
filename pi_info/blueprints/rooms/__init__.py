from datetime import datetime, timedelta

from flask import Blueprint, render_template, abort, request, url_for
from jinja2 import TemplateNotFound

from pi_info.blueprints.Weekday import Weekday
from pi_info.data.DeviceType import DeviceType
from pi_info.data.room import Room
from pi_info.repository import Sensor
from pi_info.repository.DeviceWithStatus import DeviceWithStatus
from pi_info.repository.SensorData import SensorData
from pi_info.repository.device_repository import load_all_devices_with_status_by
from pi_info.repository.schedule_repository import load_all_schedules
from pi_info.repository.sensor_data_repository import load_current_sensor_data
from pi_info.repository.sensor_repository import load_sensors_by_room
from pi_info.statusbar import refresh_statusbar

rooms = Blueprint('rooms', __name__,
                  template_folder='templates')


def get_all_sensors_for(room: Room):
    return load_sensors_by_room(room)


def get_all_lights_for(room: Room):
    all_devices: [DeviceWithStatus] = [device.as_dict() for device in load_all_devices_with_status_by(room)]
    return all_devices


def all_things_for_room(room: Room):
    all_sensors_in_room = get_all_sensors_for(room)
    enriched_with_current_values = [{**get_displayed_sensor_data(load_current_sensor_data(sensor), sensor), **sensor.__dict__} for sensor in all_sensors_in_room]
    all_lights_in_room = get_all_lights_for(room)

    things = [
        {
            "title": "Sensors",
            "data": enriched_with_current_values
        },
        {
            "title": "Devices",
            "data": all_lights_in_room
        }
    ]

    return [thing for thing in things if len(thing['data']) > 0]


def get_displayed_sensor_data(sensor_data: SensorData, sensor: Sensor):
    if sensor_data is not None:
        display_data = [dict(formatted_value="{} {}".format(value['value'], get_unit_by_type(value['type'])), type=value['type'].capitalize()) for value in
                        sensor_data.values]
        is_active = dict(is_active=sensor_data.published_time > datetime.now() - timedelta(minutes=(10 * sensor.sampling_rate)))
    else:
        display_data = [{}]
        sensor_data = SensorData.get_empty()
        is_active = {"is_active": False}

    return dict(data=sensor_data, display_data=display_data, **is_active)


def get_unit_by_type(type):
    type_unit = {
        'temperature': '°C',
        'humidity': '%'
    }
    return type_unit.get(type, '')


def get_buttons(selected, room_filter):
    status_button = {"url": url_for('rooms.show_room', page='status', filter=room_filter), "active_status": 'active' if selected == 'status' else '', "icon_type": '',
                     "button_text": "STATUS"}
    list_button = {"url": url_for('rooms.show_room', page='list', filter=room_filter), "active_status": 'active' if selected == 'list' else '', "icon_type": 'list icon',
                   "button_text": "LIST"}
    graph_button = {"url": url_for('rooms.show_room', page='graph', filter=room_filter), "active_status": 'active' if selected == 'graph' else '',
                    "icon_type": 'chart bar icon',
                    "button_text": "GRAPH"}
    return [status_button, list_button, graph_button]


@rooms.route('/rooms', defaults={'page': 'status'})
@rooms.route('/rooms/<page>', methods=['GET'])
def show_room(page):
    try:
        room = Room[request.args.get('filter')]
        statusbar = refresh_statusbar()
        all_thing_per_room = all_things_for_room(room)
        locations = [{"display": room.value.title(), "value": room.value} for room in Room]
        device_types = [{"display": type.value.title(), "value": type.value} for type in DeviceType]
        buttons = get_buttons(selected=page, room_filter=room.name)
        all_schedules = load_all_schedules()
        device_ids = set(map(lambda i: i.device_id, all_schedules))
        schedules_by_ids = {}
        for id in device_ids:
            schedules_by_ids[id] = []
            for schedule in all_schedules:
                if schedule.device_id == id:
                    schedules_by_ids[id].append(schedule.__dict__)

        return render_template('room/%s.html' % page, active='home', room=room.value, things=all_thing_per_room,
                               devices_schedules=schedules_by_ids, weekdays=Weekday.get_all_weekdays(), statusbar=statusbar,
                               locations=locations, device_types=device_types, buttons=buttons)
    except TemplateNotFound:
        abort(404)
