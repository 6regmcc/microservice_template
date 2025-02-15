import pytest

from microservice_template.db.db import db_get_all_notes
from microservice_template.db.db_sqlalchemy.db_sqlalchemy import create
from microservice_template.models.note import Note
from microservice_template.schemas.note import ReturnNote
from tests.conftest import db_session


@pytest.fixture(scope="function")
def create_note(db_session):
    new_note = Note(note_title="note_title1", note_body="note_title2")
    created_note: Note = create(new_note, db=db_session)
    return created_note

@pytest.fixture()
def create_note_2(db_session):
    new_note = Note(note_title="note_title2", note_body="note_title2")
    created_note: Note = create(new_note, db=db_session)
    return created_note


def test_get_all_notes(create_note, create_note_2, db_session):
    found_notes = db_get_all_notes(db=db_session)
    assert len(found_notes) == 2
    for note in found_notes:
        assert isinstance(note, ReturnNote)
        assert note.note_title
        assert note.note_body
        assert note.published == False
        assert note.date_created
        assert note.date_modified
