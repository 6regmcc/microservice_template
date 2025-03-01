from importlib.metadata import Lookup


async def process_received_messages(message:dict, topic: str):
    if topic == "note.created":
        pass