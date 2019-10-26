from pi_info.mqtt.handlers import AbstractMessageHandler


class RelayStatusMessageHandler(AbstractMessageHandler):

    @property
    def topic(self):
        return "switch/status"

    def parse_message(self, raw_message):
        return raw_message

    def handle(self, parsed_message):
        print(parsed_message)

