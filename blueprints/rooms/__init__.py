from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound

from room import Room
from statusbar import refresh_statusbar

rooms = Blueprint('rooms', __name__,
                 template_folder='templates')


def all_things_for_room(room):
    print(room)
    print(room)


@rooms.route('/rooms', defaults={'page': 'index'})
@rooms.route('/rooms/<page>', methods=['GET'])
def show_room(page):
    try:
        room = Room[request.args.get('room')]
        statusbar = refresh_statusbar()
        all_thing_per_room = all_things_for_room(room)
        return render_template('room/%s.html' % page, active='home', things=all_thing_per_room, statusbar=statusbar)
    except TemplateNotFound:
        abort(404)


