import logging
from enum import Enum

from flask import Blueprint, render_template, abort, request, redirect, url_for, make_response, current_app
from jinja2 import TemplateNotFound

from app import get_mqtt_client, get_scheduler
from pi_info.blueprints.Weekday import Weekday
from pi_info.data.DeviceType import DeviceType
from pi_info.data.lights import LIGHTS, LightStatus, get_light_by_id
from pi_info.data.room import Room
from pi_info.repository.Device import Device
from pi_info.repository.DeviceStatus import DeviceStatus, Status
from pi_info.repository.DeviceWithStatus import DeviceWithStatus
from pi_info.repository.Schedule import Schedule
from pi_info.repository.device_repository import load_all_devices, save_device, load_all_devices_with_status, \
    update_device
from pi_info.repository.device_status_repository import save_device_status, update_device_status
from pi_info.repository.schedule_repository import save_schedule, load_all_schedules, update_schedule, delete_schedule
from pi_info.statusbar import refresh_statusbar

logger = logging.getLogger('lights blueprint')

lights = Blueprint('lights', __name__,
                   template_folder='templates')


# TODO: delete device form, delete scheduled times for device
# TODO: create group, edit group, delete group, group schedules


def get_buttons(selected):
    status_button = {"url": url_for('lights.show_lights', page='status'),
                     "active_status": 'active' if selected == 'status' else '', "icon_type": '',
                     "button_text": "STATUS"}
    list_button = {"url": url_for('lights.show_lights', page='list'),
                   "active_status": 'active' if selected == 'list' else '', "icon_type": 'list icon',
                   "button_text": "LIST"}
    add_new_button = {"url": url_for('lights.new_device'),
                      "active_status": 'teal',
                      "icon_type": '',
                      "button_text": "ADD"
                      }
    return [status_button, list_button, add_new_button]


@lights.route('/lights', defaults={'page': 'status'})
@lights.route('/lights/<page>', methods=['GET'])
def show_lights(page):
    try:
        statusbar = refresh_statusbar()
        buttons = get_buttons(selected=page)
        locations = [{"display": room.value.title(), "value": room.value} for room in Room]
        device_types = [{"display": type.value.title(), "value": type.value} for type in DeviceType]
        all_schedules = load_all_schedules()
        device_ids = set(map(lambda i: i.device_id, all_schedules))
        schedules_by_ids = {}
        for id in device_ids:
            schedules_by_ids[id] = []
            for schedule in all_schedules:
                if schedule.device_id == id:
                    schedules_by_ids[id].append(schedule.__dict__)
        all_devices: [DeviceWithStatus] = [device.as_dict() for device in load_all_devices_with_status()]
        return render_template('lights/%s.html' % page, active='lights', lights=all_devices, statusbar=statusbar,
                               buttons=buttons, devices_schedules=schedules_by_ids, weekdays=Weekday.get_all_weekdays(),
                               locations=locations, device_types=device_types, api_base_url=current_app.config["API_BASE_URL"])
    except TemplateNotFound:
        abort(404)


def default_conv(o):
    if isinstance(o, Enum):
        return o.value
    return o.__dict__


def make_action_func(status: str, device_id: str, client, publisher):
    def create_payload_and_publish():
        payload = "{\"status\":\"" + status + "\",\"relay_id\":\"" + device_id + "\"}"
        publisher(client, "switch/relay", payload)

    return create_payload_and_publish


@lights.route('/lights/light/schedule', methods=['POST'])
def save_new_light_schedule():
    try:
        schedule: Schedule = get_schedule_from_form(request)
        sched_id = save_schedule(schedule) if schedule.schedule_id is None else update_schedule(schedule)
        action = make_action_func(schedule.status, str(schedule.device_id), get_mqtt_client(), publish)
        get_scheduler().schedule_task_from_form(schedule.device_id, sched_id, schedule.time, schedule.days, action)
        return redirect(url_for('lights.show_lights', _method='GET'))
    except TemplateNotFound:
        abort(404)


@lights.route('/lights/light/edit', methods=['POST'])
def edit_device():
    try:
        device: Device = make_device_from_form(request.form)
        update_device(device)
        return redirect(url_for('lights.show_lights', _method='GET'))
    except TemplateNotFound:
        abort(404)


@lights.route('/lights/light/schedule', methods=['GET'])
def delete_light_schedule():
    try:
        schedule_id = int(request.args['schedule_id'])
        device_id = int(request.args['device_id'])
        delete_schedule(schedule_id)
        get_scheduler().cancel_task("{}-{}".format(device_id, schedule_id))
        print(len(get_scheduler().schedules))
        return redirect(url_for('lights.show_lights', _method='GET'))
    except TemplateNotFound:
        abort(404)


@lights.route('/lights/new', methods=['GET'])
def new_device():
    try:
        statusbar = refresh_statusbar()
        locations = [room.value.title() for room in Room]
        device_types = [type.value.title() for type in DeviceType]
        sorted_devices = sorted(load_all_devices(), key=lambda s: s.id, reverse=True)
        next_id = sorted_devices[0].id + 1 if len(load_all_devices()) > 0 else 500

        return render_template('lights/new.html', active='lights', device_types=device_types, id=next_id, locations=locations, statusbar=statusbar)
    except TemplateNotFound:
        abort(404)


def save_device_and_initial_status(device):
    save_device(device)
    save_device_status(DeviceStatus(device.id, Status.OFF))


@lights.route('/lights/save', methods=['POST'])
def save_new():
    try:
        device = make_device_from_form(request.form)
        save_device_and_initial_status(device)
        return redirect(url_for('lights.show_lights', _method='GET'))
    except TemplateNotFound:
        abort(404)


def publish(client, topic, payload):
    if client is not None:
        client.publish(topic=topic, payload=payload)
    else:
        logger.warning("can not publish message, client is not defined")


@lights.route('/lights/light', defaults={'page': ''})
@lights.route('/lights/light/<page>')
def light_status(page):
    light_id = request.args.get('light_id', "1")
    referer = request.args.get('referer', "lights.show_lights")
    status = request.args.get('status', 'OFF')
    status = "ON" if status == "OFF" else "OFF"
    payload = "{\"status\":\"" + status + "\",\"relay_id\":\"" + light_id + "\"}"
    publish(get_mqtt_client(), "switch/relay", payload)
    if light_id is not None:
        next(light for light in LIGHTS if light["light_id"] == light_id)["current_status"] = LightStatus(status)
    if page == 'list':
        return redirect(url_for(referer, page='list', status=status, light_id=light_id,
                                filter=get_light_by_id(light_id)["location"].name))
    return redirect(url_for(referer, filter=get_light_by_id(light_id)["location"].name))


current_light_status = LightStatus.OFF


@lights.route('/lights/light-control')
def light_control():
    light_id = request.args.get('light_id', "1")
    status = request.args.get('status', 'OFF')
    updated_status = "ON" if status == "OFF" else "OFF"
    payload = "{\"status\":\"" + updated_status + "\",\"device_id\":\"" + light_id + "\"}"
    publish(get_mqtt_client(), "switch/relay", payload)
    if light_id is not None:
        print("updating light status id:", light_id, "to ", updated_status)
        update_device_status(DeviceStatus(int(light_id), Status(updated_status)))

    print(payload)
    response = make_response(payload, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response


def make_device_from_form(form):
    return Device(int(form['device_id']), form['name'], form['location'].lower(), form['type'].lower())


def get_schedule_from_form(req):
    sched_id = int(req.form['schedule-id']) if req.form['schedule-id'] != '' else None
    return Schedule(sched_id, int(req.args['device_id']), req.form['state'], ",".join(req.form.getlist('weekday')), req.form['time'])
