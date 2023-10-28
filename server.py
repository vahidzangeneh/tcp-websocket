import asyncio
import config

from message_handler import MessageHandler
from message_processor import MessagePrinter


async def app(message_handler: MessageHandler):

    server = await asyncio.start_server(
        lambda r, w: message_handler.receive_messages(r, w),
        config.SERVER_ADDRESS, config.SERVER_PORT
    )

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    log_message_handler = MessageHandler(config.MAX_CONCURRENT_CONNECTIONS, MessagePrinter())
    asyncio.run(app(log_message_handler))
