from flask import Blueprint, render_template, abort, request, redirect, url_for
from jinja2 import TemplateNotFound

from pi_info.statusbar import refresh_statusbar
from pi_info.third_party.tfl_tube_status import get_all_current_tube_status, get_future_status_for, TUBE_LINES_ORDERED

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
            if tube_line is not None:
                future_status_for_line = get_future_status_for(tube_line)
                return render_template('tube_status/%s.html' % page, active='tube_status', statusbar=statusbar,
                                       tube_status=tube_status_all, lines=all_lines, future_status=future_status_for_line, selected_line=tube_line)
            return redirect(url_for('tube_status.show_tube_status', _method='GET'))
        except TemplateNotFound:
            abort(404)
