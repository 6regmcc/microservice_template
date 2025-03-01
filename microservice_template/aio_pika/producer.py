import asyncio
import json

from aio_pika import Message, connect

from microservice_template.schemas.note import ReturnNote
from os import environ

async def main(message: ReturnNote) -> None:
    # Perform connection
    connection = await connect(f"amqp://guest:guest@{environ.get("RABBITMQ_URL")}/")
    mes_body = {**message.model_dump()}
    json_mes_body_json: str = json.dumps(mes_body, default=str)
    encoded_json_message_body: bytes = json_mes_body_json.encode()

    async with connection:
        # Creating a channel
        channel = await connection.channel()

        # Declaring queue
        queue = await channel.declare_queue("hello")

        # Sending the message
        await channel.default_exchange.publish(

            Message(encoded_json_message_body),
            routing_key=queue.name,
        )

        print(f" [x] Sent {encoded_json_message_body.decode()}")


if __name__ == "__main__":
    asyncio.run(main())