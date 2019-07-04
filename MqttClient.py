import json
import paho.mqtt.client as mqtt
from datetime import datetime
from sensor_data_repository import save_sensor_data


class MqttClient:

    def __init__(self, credentials, host):
        self.topic = "sensor/temperature"
        self.topic2 = "system"
        self.latest_message = ""

        client = mqtt.Client()
        self.client = client
        # localhost = "localhost"
        host_on_pi = "192.168.1.205"
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.on_publish = self.on_publish
        client.username_pw_set("lbhautmqttuser", "Q$L#s#$SXv^U=?5S8XrE")
        try:
            client.connect(host)
            client.loop_start()
        except:
            print("connection to mqtt client on " + host + " has failed")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("connected OK Returned code=", rc)
        else:
            print("Bad connection Returned code=", rc)
        client.subscribe(self.topic)
        client.publish(self.topic2, "STARTING SERVER")
        client.publish(self.topic2, "CONNECTED")

    def on_message(self, client, userdata, message):
        json_message = json.loads(message.payload)
        json_message["timestamp"] = str(datetime.now())
        json_message["topic_origin"] = message.topic
        save_sensor_data(self.get_message(json_message))

        print(json_message)
        self.latest_message = json_message
        client.publish(self.topic2, str(json_message))

    def on_publish(self, client, userdata, mid):
        print(mid)

    def publish(self, topic, payload):
        self.client.publish(topic=topic, payload=payload)

    def get_message(self, message):
        return {"timestamp": message['timestamp'],
                "values" : [
                    {"type": "temperature", "value":  message['temperature']},
                    {"type": "humidity", "value":  message['humidity']}
                ],
                "status": message['status'],
                "sensor_id": message['sensor_id']}
