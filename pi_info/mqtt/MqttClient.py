import json
import logging
from datetime import datetime

import paho.mqtt.client as mqtt

from pi_info.mqtt.handlers import AbstractMessageHandler

logger = logging.getLogger('MqttClient')


class MqttClient:
    message_handlers: [AbstractMessageHandler]

    def __init__(self, credentials, host, message_handlers):
        client = mqtt.Client()
        self.client = client
        self.message_handlers = message_handlers
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

        topics = list(set(handler.topic for handler in self.message_handlers))
        self.subscribe_to_topics(topics)

    def subscribe_to_topics(self, topics):
        for topic in topics:
            self.client.subscribe(topic)

    def on_message(self, client, userdata, message):
        json_message = json.loads(message.payload)
        json_message["timestamp"] = str(datetime.now())
        json_message["topic_origin"] = message.topic

        handlers = self.find_handlers(message.topic)
        for handler in handlers:
            handler.parse_message_and_handle(json_message)

        print(json_message)

    def on_publish(self, client, userdata, mid):
        print(mid)

    def publish(self, topic, payload):
        print(payload)
        self.client.publish(topic=topic, payload=payload)

    def find_handlers(self, topic):
        return [handler for handler in self.message_handlers if handler.can_handle(topic)]
