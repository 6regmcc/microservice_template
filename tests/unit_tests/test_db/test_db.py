import datetime
import os
from sqlite3 import sqlite_version
from unittest import mock

import pytest
from pytest_mock import MockerFixture
from sqlalchemy.orm import Session

import microservice_template
from microservice_template.db import db_sqlalchemy
from microservice_template.db.db import db_create_note
from microservice_template.models.note import Note
from microservice_template.schemas.note import CreateNote, ReturnNote





@pytest.fixture(scope="function")
def create_note_data():
    note_data: CreateNote = CreateNote(note_title="test_note_title",note_body="test_note_body")
    return note_data


@pytest.fixture(scope="function")
def create_note_model(create_note_data: CreateNote):
    note_model: Note = Note(**create_note_data.model_dump())
    return note_model

@pytest.fixture(scope="function")
def return_note_model(create_note_data: CreateNote):
    return_note_model: Note = Note(**create_note_data.model_dump(),date_created=datetime.datetime.now(),date_modified=datetime.datetime.now(),published=False)
    return return_note_model


#@mock.patch("microservice_template.db.db.create", return_value=return_note_model)
def test_create_note(create_note_data: CreateNote, return_note_model: Note, mocker: MockerFixture, db_session: Session):
    mocker.patch("microservice_template.db.db.create", return_value=return_note_model)
    new_note = db_create_note(create_note_data, db_session)
    assert isinstance(new_note, ReturnNote)
    microservice_template.db.db.create.assert_called_once()
