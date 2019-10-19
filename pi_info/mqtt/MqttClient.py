import json
import logging
from datetime import datetime

import paho.mqtt.client as mqtt

logger = logging.getLogger('MqttClient')

class MqttClient:

    def __init__(self, credentials, host, message_handlers):
        self.topic_handler = {handler.topic: handler for handler in message_handlers}
        client = mqtt.Client()
        self.client = client
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.on_publish = self.on_publish
        client.username_pw_set(credentials.username, credentials.password)
        try:
            logger.debug('Connecting to mqtt broker on {} ...'.format(host))
            client.connect(host)
            client.loop_start()
        except:
            logger.warning('"connection to mqtt client on {} has failed"'.format(host))

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.debug('Connected OK Returned code = {}'.format(rc))

        else:
            logger.warning('Bad connection Returned code = {}'.format(rc))
        for topic in self.topic_handler.keys():
            client.subscribe(topic)

    def on_message(self, client, userdata, message):
        json_message = json.loads(message.payload)
        json_message["timestamp"] = str(datetime.now())
        json_message["topic_origin"] = message.topic
        if message.topic in self.topic_handler:
            handler = self.topic_handler[message.topic].handler
            handler(self.get_message(json_message)) # TODO: the handler should know how to read the message, if not this is the only message format it van read.
        else:
            raise RuntimeError('no handler found for topic: ' + message.topic)

        print(json_message)

    def on_publish(self, client, userdata, mid):
        print(mid)

    def publish(self, topic, payload):
        print(payload)
        self.client.publish(topic=topic, payload=payload)

    def get_message(self, message):
        return {"timestamp": message['timestamp'],
                "values" : [
                    {"type": "temperature", "value":  message['temperature']},
                    {"type": "humidity", "value":  message['humidity']}
                ],
                "status": message['status'],
                "sensor_id": message['sensor_id']}
