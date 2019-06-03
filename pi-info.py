import configparser

from flask import Flask

from Credentials import Credentials
from MqttClient import MqttClient

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')
credentials = Credentials(config['MQTT-BROKER']['MQTT_USERNAME'], config['MQTT-BROKER']['MQTT_PASSWORD'])
host = config['MQTT-BROKER']['MQTT_HOST']
mqttClient = MqttClient(credentials, host)


@app.route("/")
def home():
    return "Hello, World!\nThe current temperature is: " + mqttClient.latest_message + " C"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9080)
