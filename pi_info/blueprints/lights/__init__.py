import json
import logging
import time
from enum import Enum

from flask import Blueprint, render_template, abort, request, redirect, url_for, make_response, current_app
from jinja2 import TemplateNotFound

from app import get_mqtt_client, get_scheduler
from pi_info.blueprints.Weekday import Weekday
from pi_info.data.DeviceType import DeviceType
from pi_info.data.room import Room
from pi_info.repository.Device import Device
from pi_info.repository.DeviceStatus import DeviceStatus, Status
from pi_info.repository.DeviceWithStatus import DeviceWithStatus
from pi_info.repository.Group import Group
from pi_info.repository.Schedule import Schedule
from pi_info.repository.device_repository import load_all_devices, save_device, load_all_devices_with_status, \
    update_device, delete_device_by, load_device_with_status_by
from pi_info.repository.device_status_repository import save_device_status, update_device_status, \
    delete_device_status_for
from pi_info.repository.group_repository import save_group, load_all_groups, load_group_by, update_group
from pi_info.repository.schedule_repository import save_schedule, load_all_schedules, update_schedule, delete_schedule, \
    load_schedules_for
from pi_info.statusbar import refresh_statusbar

logger = logging.getLogger('lights blueprint')

lights = Blueprint('lights', __name__,
                   template_folder='templates')


# TODO: create group, edit group, delete group, group schedules
# TODO: group set schedule


def get_buttons(selected):
    status_button = {"url": url_for('lights.show_lights', page='status'),
                     "active_status": 'active' if selected == 'status' else '', "icon_type": '',
                     "button_text": "STATUS"}
    list_button = {"url": url_for('lights.show_lights', page='list'),
                   "active_status": 'active' if selected == 'list' else '', "icon_type": 'list icon',
                   "button_text": "LIST"}
    groups_button = {"url": url_for('lights.show_lights', page='groups'),
                     "active_status": 'active' if selected == 'groups' else '',
                     "icon_type": 'object group outline icon',
                     "button_text": "GROUPS"}
    add_new_button = {"url": url_for('lights.new_device') if selected == 'status' or selected == 'list' else url_for(
        'lights.new_group'),
                      "active_status": 'teal',
                      "icon_type": '',
                      "button_text": "ADD"
                      }
    return [status_button, list_button, groups_button, add_new_button]


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
        groups: [Group] = load_all_groups()
        return render_template('lights/%s.html' % page, active='lights', lights=all_devices, statusbar=statusbar,
                               buttons=buttons, devices_schedules=schedules_by_ids, weekdays=Weekday.get_all_weekdays(),
                               locations=locations, device_types=device_types, groups=groups,
                               api_base_url=current_app.config["API_BASE_URL"])
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


@lights.route('/lights/light/delete', methods=['GET'])
def remove_device():
    try:
        device_id = int(request.args['device_id'])
        schedules_to_remove: [Schedule] = load_schedules_for(device_id)
        for schedule in schedules_to_remove:
            delete_schedule(schedule.schedule_id)
            get_scheduler().cancel_task("{}-{}".format(device_id, schedule.schedule_id))
        delete_device_status_for(device_id)
        delete_device_by(device_id)

        return redirect(url_for('lights.show_lights', _method='GET'))
    except TemplateNotFound:
        abort(404)


@lights.route('/lights/new', methods=['GET'])
def new_device():
    try:
        statusbar = refresh_statusbar()
        locations = [room.value.title() for room in Room]
        device_types = [type.value.title() for type in DeviceType]
        sorted_devices = sorted(load_all_devices(), key=lambda s: s.device_id, reverse=True)
        next_id = sorted_devices[0].device_id + 1 if len(load_all_devices()) > 0 else 500

        return render_template('lights/new.html', active='lights', device_types=device_types, id=next_id,
                               locations=locations, statusbar=statusbar)
    except TemplateNotFound:
        abort(404)


@lights.route('/lights/groups/new', methods=['GET'])
def new_group():
    try:
        statusbar = refresh_statusbar()
        all_devices: [Device] = [device.as_dict() for device in load_all_devices()]
        return render_template('lights/new_group.html', active='lights', devices=all_devices, statusbar=statusbar,
                               api_base_url=current_app.config['API_BASE_URL'])
    except TemplateNotFound:
        abort(404)


@lights.route('/lights/groups/group/edit', methods=['GET'])
def edit_group():
    try:
        group_id = int(request.args['group_id'])
        statusbar = refresh_statusbar()
        group_to_edit: Group = load_group_by(group_id)
        all_devices: [Device] = [device.as_dict() for device in load_all_devices()]

        return render_template('lights/edit_group.html', active='lights', group=group_to_edit,
                               devices=all_devices, statusbar=statusbar,
                               api_base_url=current_app.config['API_BASE_URL'])
    except TemplateNotFound:
        abort(404)


def make_group_from(form) -> Group:
    ids = [int(id) for id in form['ids'].split(',')]
    delay = int(form['delay-in-ms'])
    group_id = form.get('group_id', None)
    return Group(group_id=group_id, name=form['group-name'], delay_in_ms=delay, ids=ids, status=Status.OFF)


@lights.route('/lights/groups/save-new', methods=['POST'])
def save_new_group():
    try:
        group: Group = make_group_from(request.form)
        save_group(group)
        return redirect(url_for('lights.show_lights', _method='GET', page='groups'))
    except TemplateNotFound:
        abort(404)

@lights.route('/lights/groups/group/update', methods=['POST'])
def save_edit_group():
    try:
        group: Group = make_group_from(request.form)
        update_group(group)
        return redirect(url_for('lights.show_lights', _method='GET', page='groups'))
    except TemplateNotFound:
        abort(404)


def save_device_and_initial_status(device: Device):
    save_device(device)
    save_device_status(DeviceStatus(device.device_id, Status.OFF))


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


@lights.route('/lights/light-control')
def light_control():
    light_ids = json.loads(request.args.get('light_ids', []))
    if not isinstance(light_ids, list):
        light_ids = [light_ids]
    delay = int(request.args.get('delay', 0))
    group_id = request.args.get('group_id', None)
    status = request.args.get('status', 'OFF')
    updated_status = "ON" if status == "OFF" else "OFF"
    payloads = []
    for id in light_ids:
        payload = "{{\"status\":\"{}\",\"device_id\":\"{}\"}}".format(updated_status, id)
        json_payload = json.dumps(payload)
        publish(get_mqtt_client(), "switch/relay", json_payload)
        print("updating light status id:", id, "to ", updated_status)
        update_device_status(DeviceStatus(id, Status(updated_status)))
        payloads.append(payload)
        time.sleep(delay / 1000.0)
    if group_id:
        group = load_group_by(int(group_id))
        updated_group = Group(group.group_id, group.name, group.delay_in_ms, group.ids, Status(updated_status))
        update_group(updated_group)

    print(payloads)
    response = make_response(json.dumps(payloads), 200)
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response


@lights.route('/lights/data')
def lights_data():
    light_id = request.args.get('light_id', None)
    group_id = request.args.get('group_id', None)
    payload = {
        'group_status': None,
        'single_device_status': None
    }
    if group_id:
        group = load_group_by(int(group_id))
        payload['group_status'] = group.status.value
    if light_id:
        device = load_device_with_status_by(int(light_id))
        payload['single_device_status'] = device.status.value

    print(payload)
    response = make_response(payload, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response


def make_device_from_form(form):
    return Device(int(form['device_id']), form['name'], form['location'].lower(), form['type'].lower())


def get_schedule_from_form(req):
    sched_id = int(req.form['schedule-id']) if req.form['schedule-id'] != '' else None
    return Schedule(sched_id, int(req.args['device_id']), req.form['state'], ",".join(req.form.getlist('weekday')),
                    req.form['time'])
