from abc import ABC, abstractmethod


class AbstractMessageHandler(ABC):

    def __init__(self) -> None:
        super().__init__()

    @property
    @abstractmethod
    def topic(self):
        pass

    @abstractmethod
    def handle(self, parsed_message):
        pass

    @abstractmethod
    def parse_message(self, raw_message):
        pass

    def can_handle(self, topic) -> bool:
        return topic == self.topic

    def parse_message_and_handle(self, raw_message):
        self.handle(self.parse_message(raw_message))

