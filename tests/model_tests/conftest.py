import pytest
from sqlalchemy import inspect

from microservice_template.config.db_config import engine


@pytest.fixture(scope="function")
def db_inspector(db_session):
    return inspect(engine)