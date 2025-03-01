"""import asyncio

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage
from os import environ

async def on_message(message: AbstractIncomingMessage) -> None:

    on_message doesn't necessarily have to be defined as async.
    Here it is to show that it's possible.

    print(" [x] Received message %r" % message)
    print("Message body is: %r" % message.body)

    print("Before sleep!")
    await asyncio.sleep(5)  # Represents async I/O operations
    print("After sleep!")


async def main() -> None:
    # Perform connection
    connection = await connect(f"amqp://guest:guest@{environ.get("RABBITMQ_URL")}/")
    async with connection:
        # Creating a channel
        channel = await connection.channel()

        # Declaring queue
        queue = await channel.declare_queue("hello")

        # Start listening the queue with name 'hello'
        await queue.consume(on_message, no_ack=True)

        print(" [*] Waiting for messages. To exit press CTRL+C")
        await asyncio.Future()"""



import asyncio
import sys
from os import environ

from aio_pika import ExchangeType, connect
from aio_pika.abc import AbstractIncomingMessage

async def process_received_message(message):
    print(f" ahhhhhh [x] {message.routing_key!r}:{message.body.decode()!r}")



async def main() -> None:
    # Perform connection
    connection = await connect(f"amqp://guest:guest@{environ.get("RABBITMQ_URL")}/")

    # Creating a channel
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    # Declare an exchange
    topic_logs_exchange = await channel.declare_exchange(
        "topic_logs", ExchangeType.TOPIC,
    )

    # Declaring queue
    queue = await channel.declare_queue(
        "task_queue", durable=True,
    )

    binding_keys = ["note.created"]

    if not binding_keys:
        sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
        sys.exit(1)

    for binding_key in binding_keys:
        await queue.bind(topic_logs_exchange, routing_key=binding_key)

    print(" [*] Waiting for messages. To exit press CTRL+C")

    # Start listening the queue with name 'task_queue'
    async with queue.iterator() as iterator:
        message: AbstractIncomingMessage
        async for message in iterator:
            async with message.process():
                await process_received_message(message)



