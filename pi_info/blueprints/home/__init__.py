from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from pi_info.statusbar import refresh_statusbar

home = Blueprint('home', __name__,
                 template_folder='templates')


@home.route('/home', defaults={'page': 'index'})
@home.route('/home/<page>', methods=['GET'])
def show_home(page):
    try:
        statusbar = refresh_statusbar()
        return render_template('home/%s.html' % page, active='home', statusbar=statusbar )
    except TemplateNotFound:
        abort(404)
