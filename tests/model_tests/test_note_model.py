import os
from sqlite3.dbapi2 import Timestamp

from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.dialects.mssql.information_schema import columns

from microservice_template.models.note import Note


def test_testing():

    print(os.getenv("ENVIRONMENT"))
    print(os.getenv("DATABASE_URL"))
    assert True


def test_model_structure_table_exists(db_inspector):
    assert db_inspector.has_table(Note.__tablename__)


def test_db_columns(db_inspector):
    columns = {columns["name"]: columns for columns in db_inspector.get_columns("note")}
    assert "id" in columns
    assert "note_title" in columns
    assert "note_body" in columns
    assert "published" in columns
    assert "date_created" in columns
    assert "date_modified" in columns
    assert len(columns) == 6


def test_column_type(db_inspector):
    columns = {columns["name"]: columns for columns in db_inspector.get_columns("note")}
    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["note_title"]["type"], String)
    assert isinstance(columns["note_body"]["type"], String)
    assert isinstance(columns["published"]["type"], Boolean)
    assert isinstance(columns["date_created"]["type"], DateTime)
    assert isinstance(columns["date_modified"]["type"], DateTime)

def test_db_nullable(db_inspector):
    table = "note"
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
        "note_title": False,
        "note_body": False,
        "published": False,
        "date_created": False,
        "date_modified": False,
    }

    for column in columns:
        column_name = column["name"]
        assert column["nullable"] == expected_nullable.get(
            column_name
        ), f"column '{column_name}' is not nullable as expected"


def test_server_default(db_inspector):
    columns = {columns["name"]: columns for columns in db_inspector.get_columns("note")}
    assert columns["date_created"]["default"] == "now()"
    assert columns["date_modified"]["default"] == "now()"
    #assert columns["published"]["default"] == False


def test_model_structure_unique_constraints(db_inspector):
    constraints = db_inspector.get_unique_constraints("note")
    assert True
