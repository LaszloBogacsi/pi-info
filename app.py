from flask import Flask

from pi_info.blueprints.home import home
from pi_info.blueprints.lights import lights
from pi_info.blueprints.rooms import rooms
from pi_info.blueprints.sensors import sensors
from pi_info.blueprints.tube_status import tube_status


app = Flask(__name__)
app.register_blueprint(home)
app.register_blueprint(lights)
app.register_blueprint(sensors)
app.register_blueprint(tube_status)
app.register_blueprint(rooms)

