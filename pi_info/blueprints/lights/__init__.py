import datetime
import random
from enum import Enum

from flask import Blueprint, render_template, abort, request, redirect, url_for, make_response, current_app
from jinja2 import TemplateNotFound

from app import get_mqtt_client, get_scheduler
from pi_info.data.lights import LIGHTS, LightStatus, get_light_by_id
from pi_info.repository.schedule_repository import save_schedule, load_all_schedules, update_schedule, delete_schedule
from pi_info.scheduling.Task import Task
from pi_info.statusbar import refresh_statusbar

lights = Blueprint('lights', __name__,
                   template_folder='templates')


class Weekday(Enum):
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6
    Sun = 7

    @staticmethod
    def get_all_weekdays():
        return [dict(key=v.value, value=v.name )for k, v in enumerate(Weekday)]


def get_buttons(selected):
    status_button = {"url": url_for('lights.show_lights', page='status'),
                     "active_status": 'active' if selected == 'status' else '', "icon_type": '',
                     "button_text": "STATUS"}
    list_button = {"url": url_for('lights.show_lights', page='list'),
                   "active_status": 'active' if selected == 'list' else '', "icon_type": 'list icon',
                   "button_text": "LIST"}
    return [status_button, list_button]


@lights.route('/lights', defaults={'page': 'status'})
@lights.route('/lights/<page>', methods=['GET'])
def show_lights(page):
    try:
        statusbar = refresh_statusbar()
        buttons = get_buttons(selected=page)
        all_schedules = load_all_schedules()
        device_ids = set(map(lambda i: i.device_id, all_schedules))
        schedules_by_ids = {}
        for id in device_ids:
            schedules_by_ids[id] = []
            for schedule in all_schedules:
                if schedule.device_id == id:
                    schedules_by_ids[id].append(schedule.__dict__)

        return render_template('lights/%s.html' % page, active='lights', lights=LIGHTS, statusbar=statusbar,
                               buttons=buttons, devices_schedules=schedules_by_ids, weekdays=Weekday.get_all_weekdays(),
                               api_base_url=current_app.config["API_BASE_URL"])
    except TemplateNotFound:
        abort(404)


def find_closest_time(schedule) -> datetime:
    current_time = datetime.datetime.now()
    time_to_run = schedule['time'].split(':')
    schedule_time = Time(int(time_to_run[0]), int(time_to_run[1]), int(time_to_run[2]))
    weekdays = list(int(day) for day in schedule['days'].split(',')) # "[1,2,3,4,7]"
    current_weekday = datetime.datetime.today().weekday() + 1
    today = current_weekday in weekdays
    scheduled_time = current_time.replace(hour=schedule_time.hour, minute=schedule_time.minute, second=schedule_time.second, microsecond=0)
    in_time = current_time < scheduled_time
    if today and in_time:
        return scheduled_time
    if not (today and in_time):
        deltas = []
        for day in weekdays:
            deltas.append(abs(day - current_weekday) if day - current_weekday != 0 else 7)
        closest_day = weekdays[max([i for i, v in enumerate(deltas) if v == min(deltas)])]
        closest_day_diff = closest_day - current_weekday if closest_day - current_weekday > 0 else closest_day + 7 - current_weekday
        the_time = scheduled_time.replace(day=current_time.day + closest_day_diff)
        return the_time


def delay_until_first_run(schedule) -> int:
    current_time = datetime.datetime.now()
    closest_time = find_closest_time(schedule)
    return (closest_time - current_time).seconds


class Time:

    def __init__(self, hour, minute, second) -> None:
        self.second = second
        self.minute = minute
        self.hour = hour


if __name__ == "__main__":
    dummy_schedule = {
        "schedule_id": "1",
        "device_id": 2,
        "status": "ON",
        "days": "1,2,3,4,5,6,7",
        "time": "12:00:00"
    }
    s = delay_until_first_run(dummy_schedule)
    print(s)


def make_action_func(status: str, device_id: str):
    def create_payload_and_publish():
        payload = "{\"status\":\"" + status + "\",\"relay_id\":\"" + device_id + "\"}"
        publish(get_mqtt_client(), "switch/relay", payload)
    return create_payload_and_publish


@lights.route('/lights/light/schedule', methods=['POST'])
def save_new_light_schedule():
    try:
        schedule = get_schedule_from_form(request)
        sched_id = save_schedule(schedule) if schedule['schedule_id'] == '' else update_schedule(schedule)
        id = "{}-{}-{}-{}".format(schedule['device_id'], schedule['time'], schedule['status'], sched_id)
        delay_in_sec = delay_until_first_run(schedule)
        action = make_action_func(schedule["status"], schedule["device_id"])
        get_scheduler().schedule_task(Task(id, delay_in_sec, action))
        return redirect(url_for('lights.show_lights', _method='GET'))
    except TemplateNotFound:
        abort(404)


@lights.route('/lights/light/schedule', methods=['GET'])
def delete_light_schedule():
    try:
        schedule_id = int(request.args['schedule_id'])
        delete_schedule(schedule_id)
        return redirect(url_for('lights.show_lights', _method='GET'))
    except TemplateNotFound:
        abort(404)


def publish(client, topic, payload):
    if client is not None:
        client.publish(topic=topic, payload=payload)
    else:
        print("can not publish message")


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
        return redirect(url_for(referer, page='list', status=status, light_id=light_id, filter=get_light_by_id(light_id)["location"].name))
    return redirect(url_for(referer, filter=get_light_by_id(light_id)["location"].name))


current_light_status = LightStatus.OFF


@lights.route('/lights/light-control')
def light_control():
    light_id = request.args.get('light_id', "1")
    status = request.args.get('status', 'OFF')
    updated_status = "ON" if status == "OFF" else "OFF"
    payload = "{\"status\":\"" + updated_status + "\",\"relay_id\":\"" + light_id + "\"}"
    publish(get_mqtt_client(), "switch/relay", payload)
    if light_id is not None:
        print("updating light status id:", light_id, "to ", updated_status)

        next(light for light in LIGHTS if str(light["light_id"]) == light_id)["current_status"] = LightStatus(updated_status)
        current_light_status = LightStatus(updated_status)
        print(current_light_status)
    print(payload)
    response = make_response(payload, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response


def get_schedule_from_form(request):
    return {
        "schedule_id": request.form['schedule-id'],
        "device_id": int(request.args['device_id']),
        "status": request.form['state'],
        "days": ",".join(request.form.getlist('weekday')),
        "time": request.form['time']
    }
