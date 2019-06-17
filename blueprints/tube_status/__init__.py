from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from statusbar import refresh_statusbar
from tfl_tube_status import get_all_current_tube_status, central, get_future_status_for

tube_status = Blueprint('tube_status', __name__,
                 template_folder='templates')


@tube_status.route('/tubestatus', defaults={'page': 'index'})
@tube_status.route('/tubestatus/<page>')
def show_tube_status(page):
    try:
        statusbar = refresh_statusbar()
        tube_status_all = get_all_current_tube_status()
        future_status_for_line = get_future_status_for(central)
        return render_template('tube_status/%s.html' % page, active='tube_status', statusbar=statusbar,
                               tube_status=tube_status_all, future_status=future_status_for_line )
    except TemplateNotFound:
        abort(404)
