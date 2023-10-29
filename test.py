import unittest
import asyncio
import io
from unittest.mock import MagicMock, patch
from server import MessageHandler
from message_processor import MessagePrinter


class TestMessageHandler(unittest.TestCase):
    # TODO only two basic unit tests is added. We need more tests to cover all edge cases
    def setUp(self):
        self.message_processor = MessagePrinter()

    def test_add_new_connection(self):
        handler = MessageHandler(max_connections=2, processor=self.message_processor)
        writer_1 = MagicMock()
        writer_2 = MagicMock()

        # Add two connections
        connection_id_1 = asyncio.run(handler.add_new_connection(writer_1))
        connection_id_2 = asyncio.run(handler.add_new_connection(writer_2))

        self.assertEqual(len(handler._connections), 2)

        # The maximum connections are reached, so the first connection should be closed
        writer_3 = MagicMock()
        connection_id_3 = asyncio.run(handler.add_new_connection(writer_3))

        # Ensure that the first connection is removed from the queue
        self.assertEqual(len(handler._connections), 2)

        # Check that the closed connection is no longer in the connection queue
        self.assertNotIn(connection_id_1, handler._con_queue)

    @patch('message_handler.MessageHandler.reading_sequence_of_messages')
    def test_receive_messages(self, mock):
        handler = MessageHandler(max_connections=2, processor=self.message_processor)
        writer = MagicMock()
        reader = io.BytesIO(b'\x00\x00\x00\x0bHello, test')

        async def simulate_client(reader, writer):
            await handler.receive_messages(reader, writer)

        # Simulate a client connection
        asyncio.run(simulate_client(reader, writer))

        # Ensure that the message processor is called with the message data
        self.assertTrue(mock.called)

    def test_reading_sequence_of_messages(self):
        # TODO this test should be completed
        pass

    def test_reading_sequence_of_messages_invalid_message(self):
        # TODO this test should be completed
        pass

    def test_reading_sequence_of_messages_exception(self):
        # TODO this test should be completed
        pass


if __name__ == "__main__":
    unittest.main()
