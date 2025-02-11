from sqlalchemy.orm import Session

from microservice_template.config.db_config import Base
from microservice_template.models.note import Note
from microservice_template.schemas.note import CreateNote, ReturnNote
from microservice_template.db.db_sqlalchemy.db_sqlalchemy import create

def db_create_note(create_note_data: CreateNote, db:Session) -> ReturnNote:
    new_note: Note = Note(**create_note_data.model_dump())
    created_node: Base = create(new_note, db)
    return_note: ReturnNote = ReturnNote(**created_node.to_dict())
    return return_note

