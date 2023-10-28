from abc import ABC, abstractmethod
import log_message_pb2


class MessageProcessor(ABC):
    """
    The abstract class for processing messages.
    A custom message processor can inherit from this class and overwrite the process method
    """

    @abstractmethod
    async def process(self, message_bytes: bytes):
        pass


class MessagePrinter(MessageProcessor):

    async def process(self, message_bytes: bytes) -> None:
        """
        Parse the message and print that to the stout
        :param message_bytes: message
        :return: None
        """
        # Parse the protobuf message
        message = log_message_pb2.LogMessage()
        message.ParseFromString(message_bytes)

        log_message_str = (f"LogLevel: {message.log_level}, Logger: {message.logger}, "
                           f"MAC: {':'.join(format(x, '02x') for x in message.mac)}")
        if message.message:
            log_message_str += f", Message: {message.message}"

        print(log_message_str)
