import datetime

import pytest
import sqlalchemy
from sqlalchemy.orm import Session

from microservice_template.config.db_config import Base
from microservice_template.db.db_sqlalchemy.db_sqlalchemy import create
from microservice_template.models.note import Note
from microservice_template.schemas.note import CreateNote


@pytest.fixture(scope="function")
def note_model_data():
    note_data: Note = Note(note_title="test_note_title", note_body="test_node_body")
    return note_data


def test_mock_db(mocker, db_session: Session, note_model_data:Note, ):
    mocker.patch("sqlalchemy.orm.session.Session.add")
    mocker.patch("sqlalchemy.orm.session.Session.commit")
    mocker.patch("sqlalchemy.orm.session.Session.refresh", return_value=note_model_data)

    created_note: Base = create(data=note_model_data, db=db_session)
    assert isinstance(created_note, Note)
    sqlalchemy.orm.session.Session.add.assert_called_once_with(note_model_data)
    sqlalchemy.orm.session.Session.commit.assert_called_once()
    sqlalchemy.orm.session.Session.refresh.assert_called_once()

