from microservice_template.db.db_sqlalchemy.db_sqlalchemy import create
from microservice_template.models.note import Note
from microservice_template.config.db_config import get_db



def test_create_success(db_session):
    new_note = Note(note_title="Note_title",note_body="Note_body")
    created_note: Note = create(new_note, db=db_session)
    assert created_note.id
    assert created_note.note_title
    assert created_note.note_body
    assert created_note.published == False
    assert created_note.date_created
    assert created_note.date_modified
    assert isinstance(created_note, Note)

