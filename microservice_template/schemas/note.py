from datetime import datetime

from pydantic import BaseModel


class CreateNote(BaseModel):
    note_title: str
    note_body: str


class ReturnNote(CreateNote):
    id: int
    published: bool
    date_created: datetime
    date_modified: datetime


