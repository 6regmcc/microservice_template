from datetime import datetime

from sqlalchemy import DateTime

from microservice_template.db.db_sqlalchemy.db_sqlalchemy import create
from microservice_template.models.note import Note




def test_create_note_success(db_session):
    new_note = Note(note_title="Note_Title",note_body="Note_Body")
    created_note: Note = create(new_note, db=db_session)
    assert created_note.id
    assert created_note.note_title == "Note_Title"
    assert created_note.note_body == "Note_Body"
    assert created_note.published == False
    print(type(created_note.date_created))
    assert isinstance(created_note.date_created, datetime)
    assert isinstance(created_note.date_modified, datetime)
    assert isinstance(created_note, Note)


def test_create_note_failure(db_session):
    new_note = Note(note_title="Note_Title", note_body="Note_Body")
    created_note: Note = create(new_note, db=db_session)
    second_note = Note(note_title="Note_Title", note_body="Note_Body")
    created_note: Note = create(new_note, db=db_session)