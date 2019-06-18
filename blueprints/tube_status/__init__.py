from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound

from statusbar import refresh_statusbar
from tfl_tube_status import get_all_current_tube_status, central, get_future_status_for, TUBE_LINES_ORDERED

tube_status = Blueprint('tube_status', __name__,
                 template_folder='templates')


@tube_status.route('/tubestatus', defaults={'page': 'index'}, methods=['GET', 'POST'])
@tube_status.route('/tubestatus/<page>', methods=['GET', 'POST'])
def show_tube_status(page):
    statusbar = refresh_statusbar()
    tube_status_all = get_all_current_tube_status()
    all_lines = TUBE_LINES_ORDERED

    if request.method == 'GET':
        try:
            return render_template('tube_status/%s.html' % page, active='tube_status', statusbar=statusbar,
                                   tube_status=tube_status_all, lines=all_lines)
        except TemplateNotFound:
            abort(404)

    if request.method == 'POST':
        try:
            form_data = request.form
            tube_line = next((x for x in all_lines if x.id.val == form_data.get('line')), None)
            future_status_for_line = get_future_status_for(tube_line)
            return render_template('tube_status/%s.html' % page, active='tube_status', statusbar=statusbar,
                                   tube_status=tube_status_all, lines=all_lines, future_status=future_status_for_line )
        except TemplateNotFound:
            abort(404)

