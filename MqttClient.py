import paho.mqtt.client as mqtt
import json
from datetime import datetime


class MqttClient:

    def __init__(self, credentials, host):
        self.topic = "sensor/temperature"
        self.topic2 = "system"
        self.latest_message = ""

        client = mqtt.Client()
        # localhost = "localhost"
        host_on_pi = "192.168.1.205"
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.username_pw_set("lbhautmqttuser", "Q$L#s#$SXv^U=?5S8XrE")
        client.connect(host)
        client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        if rc==0:
            print("connected OK Returned code=",rc)
        else:
            print("Bad connection Returned code=",rc)
        client.subscribe(self.topic)
        client.publish(self.topic2, "STARTING SERVER")
        client.publish(self.topic2, "CONNECTED")

    def on_message(self, client, userdata, message):
        json_message = json.loads(message.payload)
        json_message["timestamp"] = str(datetime.now())
        json_message["topic_origin"] = message.topic
        print(json_message)
        # decoded_message = str(message.payload.decode("utf-8"))

        self.latest_message = json_message
        client.publish(self.topic2, str(json_message))
