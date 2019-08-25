from flask import Blueprint, render_template, abort, request, redirect, url_for, g, make_response, current_app
from jinja2 import TemplateNotFound

from app import get_mqtt_client
from pi_info.data.lights import LIGHTS, LightStatus, get_light_by_id
from pi_info.statusbar import refresh_statusbar

lights = Blueprint('lights', __name__,
                   template_folder='templates')


def get_buttons(selected):
    status_button = {"url": url_for('lights.show_lights', page='status'), "active_status": 'active' if selected == 'status' else '', "icon_type": '',
                     "button_text": "STATUS"}
    list_button = {"url": url_for('lights.show_lights', page='list'), "active_status": 'active' if selected == 'list' else '', "icon_type": 'list icon',
                   "button_text": "LIST"}
    return [status_button, list_button]


@lights.route('/lights', defaults={'page': 'status'})
@lights.route('/lights/<page>', methods=['GET'])
def show_lights(page):
    try:
        statusbar = refresh_statusbar()
        buttons = get_buttons(selected=page)
        return render_template('lights/%s.html' % page, active='lights', lights=LIGHTS, statusbar=statusbar, buttons=buttons,
                               api_base_url=current_app.config["API_BASE_URL"])
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

        next(light for light in LIGHTS if light["light_id"] == light_id)["current_status"] = LightStatus(updated_status)
        current_light_status = LightStatus(updated_status)
        print(current_light_status)
    print(payload)
    response = make_response(payload, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response
