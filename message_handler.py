import asyncio
import struct
import logging
import uuid
from collections import deque
from asyncio.streams import StreamReader, StreamWriter
from google.protobuf.message import DecodeError

from message_processor import MessageProcessor


class MessageHandler:
    """
    This class manages all connections and provides methods to:
    - Manage the maximum concurrent connections
    - Receive messages from connections continuously
    - Replace new connections with long paused connections
    - Update the freshness of connections
    """
    _connections = {}
    _con_queue = deque()

    def __init__(self, max_connections: int, processor: MessageProcessor):
        self.max_connections = max_connections
        self.message_processor = processor

    async def add_new_connection(self, writer: StreamWriter) -> str:
        """
        Assigns a random string id to a new connection and add that to the connection queue.
        If the maximum number of concurrent connections has been reached, the long paused connection is removed and
        closed in order to open a room for new connection.
        :param writer: writer object
        :return: random string as the connection id
        """
        connection_id = uuid.uuid4().hex
        if len(self._con_queue) == self.max_connections:
            # removing the long paused connection from the connection queue
            long_paused_connection = self._con_queue.popleft()
            self._connections.pop(long_paused_connection).close()

        # adding new connection to the connection queue
        self._con_queue.append(connection_id)
        self._connections[connection_id] = writer

        return connection_id

    async def receive_messages(self, reader: StreamReader, writer: StreamWriter) -> None:
        """
        Starts to receiving messages from connections.
        Handles errors and logging for further analysis.
        :param reader: reader object
        :param writer: writer object
        :return: None
        """
        connection_id = await self.add_new_connection(writer)
        try:
            await self.reading_sequence_of_messages(reader, connection_id)
        except asyncio.IncompleteReadError:
            logging.error(f"Connection closed!")
        except Exception as e:
            logging.error(f"Error: {str(e)}")
        finally:
            try:
                self._con_queue.remove(connection_id)
                self._connections.pop(connection_id).close()
            except (ValueError, KeyError):
                writer.close()

    async def reading_sequence_of_messages(self, reader: StreamReader, connection_id: str) -> None:
        """
        Receiving messages from a connection constantly, delegate the messages to the message processor
         and update the freshness of the connections in the connections queue
        :param reader: reader object
        :param connection_id: write object
        :return: None
        """
        while True:
            # Read the message length
            length_data = await reader.readexactly(4)
            message_length = struct.unpack('>L', length_data)[0]
            # Read the protobuf message
            message_data = await reader.readexactly(message_length)

            try:
                await self.message_processor.process(message_data)
                # By receiving a new message from a connection, the connection is moved to the end of the queue
                # so that the connection is considered as a fresh connection
                self._con_queue.remove(connection_id)
                self._con_queue.append(connection_id)
            except DecodeError:
                logging.error("The message is not consistent!")
            except Exception as e:
                logging.error(f"Error: {str(e)}")
