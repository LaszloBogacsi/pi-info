from datetime import datetime

from flask import Flask
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)
topic = "sensor/temperature"
topic2 = "system"
latest_message = ""


def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK Returned code=",rc)
    else:
        print("Bad connection Returned code=",rc)
    client.subscribe(topic)
    client.publish(topic2, "STARTING SERVER")
    client.publish(topic2, "CONNECTED")


def on_message(client, userdata, message):
    json_message = json.loads(message.payload)
    json_message["timestamp"] = str(datetime.now())
    print(json_message)
    # decoded_message = str(message.payload.decode("utf-8"))
    global latest_message
    latest_message = json_message
    client.publish(topic2, str(json_message))


@app.route("/")
def home():
    return "Hello, World!\nThe current temperature is: " + latest_message + " C"


if __name__ == "__main__":
    client = mqtt.Client()
    # localhost = "localhost"
    host_on_pi = "192.168.1.205"
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set("<username here>", "<password here>")
    client.connect(host_on_pi)
    client.loop_start()
    app.run(host='0.0.0.0', port=9080)



