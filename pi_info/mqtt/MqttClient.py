import json
import paho.mqtt.client as mqtt
from datetime import datetime


class MqttClient:

    def __init__(self, credentials, host, message_handlers):
        self .topic_handler = {handler.topic: handler for handler in message_handlers}
        client = mqtt.Client()
        self.client = client
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.on_publish = self.on_publish
        client.username_pw_set(credentials.username, credentials.password)
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
        for topic in self.topic_handler.keys():
            client.subscribe(topic)

    def on_message(self, client, userdata, message):
        json_message = json.loads(message.payload)
        json_message["timestamp"] = str(datetime.now())
        json_message["topic_origin"] = message.topic
        if message.topic in self.topic_handler:
            handler = self.topic_handler[message.topic].handler
            handler(self.get_message(json_message))
        else:
            raise RuntimeError('no handler found for topic: ' + message.topic)

        print(json_message)

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
