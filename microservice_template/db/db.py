from pydantic.v1.utils import get_model
from sqlalchemy import Sequence
from sqlalchemy.orm import Session

from microservice_template.config.db_config import Base
from microservice_template.models.note import Note
from microservice_template.schemas.note import CreateNote, ReturnNote
from microservice_template.db.db_sqlalchemy.db_sqlalchemy import create, get_all
from microservice_template.aio_pika.producer import main as publish


async def db_create_note(create_note_data: CreateNote, db:Session) -> ReturnNote:
    new_note: Note = Note(**create_note_data.model_dump())
    created_node: Base = create(new_note, db)
    return_note: ReturnNote = ReturnNote(**created_node.to_dict())
    await publish(return_note)
    return return_note


def db_get_all_notes(db:Session) -> list[ReturnNote]:
    found_notes = get_all(Note, db)
    return_notes = [ReturnNote(**note.to_dict()) for note in found_notes]
    return return_notes


