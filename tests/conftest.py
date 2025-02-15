import pytest
import sqlalchemy.orm.session
from pytest_mock import session_mocker
from sqlalchemy.orm import Session

from microservice_template.config.db_config import Base, engine


@pytest.fixture(scope="function")
def db_engine():
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    session: Session = Session(db_engine)
    Base.metadata.create_all(bind=engine)
    yield session
    session.close()

