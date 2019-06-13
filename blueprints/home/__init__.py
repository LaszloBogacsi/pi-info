from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

home = Blueprint('home', __name__,
                 template_folder='templates')


@home.route('/home', defaults={'page': 'index'})
@home.route('/home/<page>')
def show(page):
    try:
        return render_template('home/%s.html' % page)
    except TemplateNotFound:
        abort(404)