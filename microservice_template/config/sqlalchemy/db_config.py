import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.environ.get("DATABASE_URL"))

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db() -> Generator:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Base(DeclarativeBase):
    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.c}


def db_create_all():
    # Base.metadata.clear()
    # Base.metadata.drop_all(bind=engine)

    Base.metadata.create_all(bind=engine, checkfirst=True)
