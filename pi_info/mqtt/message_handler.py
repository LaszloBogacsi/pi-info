class MessageHandler:
    def __init__(self, topic, handler, message_parser) -> None:
        self._message_parser = message_parser
        self.handler = handler
        self.topic = topic

    def parse_message(self, message):
        return self._message_parser(message)