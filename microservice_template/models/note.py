from datetime import datetime

from sqlalchemy import DateTime, func, CheckConstraint, String, UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from microservice_template.config.db_config import Base


class Note(Base):
    __tablename__ = "note"
    id: Mapped[int] = mapped_column(primary_key=True)
    note_title: Mapped[str] = mapped_column(String(50), unique=True)
    note_body: Mapped[str] = mapped_column()
    published: Mapped[bool] = mapped_column(default=False)
    date_created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    date_modified: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
    )
    __table_args__ = (UniqueConstraint(note_title, name="note_title_unique_constraint"),)




