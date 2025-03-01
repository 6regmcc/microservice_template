from datetime import datetime

import psycopg
import pytest
import sqlalchemy
from sqlalchemy import DateTime
from sqlalchemy.orm import Session

from microservice_template.config.db_config import Base
from microservice_template.db.db_sqlalchemy.db_sqlalchemy import create, get_all, get_one, update
from microservice_template.models.note import Note



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


def test_create_note_failure_check_constraint(db_session):
    new_note = Note(
        note_title="Note_TitleNote_TitleNote_TitleNote_TitleNote_TitleNote_TitleNote_TitleNote_TitleNote_TitleNote_TitleNote_TitleNote_TitleNote_TitleNote_TitleNote_TitleNote_TitleNote_Title",
        note_body="Note_Body")
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        created_note: Note = create(new_note, db=db_session)




def test_create_note_failure_unique_constraint(db_session):
    new_note = Note(
        note_title="Note_Title",
        note_body="Note_Body")
    created_note: Note = create(new_note, db=db_session)
    new_note2 = Note(note_title="Note_Title",
        note_body="Note_Body")
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        created_note2: Note = create(new_note2, db=db_session)


def test_get_all(create_note, create_note_2,  db_session: Session):
    found_data: list[Base] = get_all(Note, db_session)
    for model in found_data:
        assert isinstance(model, Base)
        assert model.note_title
        assert model.note_body
        assert model.published == False
        assert model.date_created
        assert model.date_modified
    assert True



def test_get_one(db_session):
    new_note = Note(note_title="Note_Title", note_body="Note_Body")
    created_note: Note = create(new_note, db=db_session)
    found_note: Note = get_one(Note,created_note.id,db_session)
    assert found_note.id == created_note.id
    assert found_note.note_title == created_note.note_title
    assert found_note.note_body == created_note.note_body
    assert found_note.published == created_note.published
    assert found_note.date_created == created_note.date_created
    assert found_note.date_modified == found_note.date_modified


def test_update(db_session):
    new_note = Note(note_title="Note_Title", note_body="Note_Body")
    created_note: Note = create(new_note, db=db_session)
    created_note.note_title = 'This title was updated'
    updated_note: Note = update(created_note, created_note.id,type(created_note),db_session)
    assert updated_note.note_title == 'This title was updated'
    assert updated_note.note_body == created_note.note_body
    assert updated_note.id  == created_note.id