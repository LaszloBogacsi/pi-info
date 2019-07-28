class MessageHandler:
    def __init__(self, topic, handler) -> None:
        self.handler = handler
        self.topic = topic
