import asyncio
import os
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from microservice_template.config.db_config import db_create_all, get_db
from microservice_template.db.db import db_create_note, db_get_all_notes
from microservice_template.schemas.note import ReturnNote, CreateNote
from microservice_template.aio_pika.consumer import main as start_consumer

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"current environment is {os.environ.get("ENVIRONMENT")}")
    db_create_all()
    loop = asyncio.get_event_loop()
    task = loop.create_task(start_consumer())
    yield
    task.cancel()

app = FastAPI(lifespan=lifespan,
              root_path=os.environ.get("ROOT_PATH"),
              openapi_url=os.environ.get("OPENAPI_URL")
              )

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/create_note", response_model=ReturnNote)
async def create_note(note_data: CreateNote, db: Annotated[Session, Depends(get_db)]):
    new_note = await db_create_note(note_data, db)
    return new_note


@app.get("/notes")
async def get_all_notes(db: Annotated[Session, Depends(get_db)]):
    found_notes = db_get_all_notes(db=db)
    return found_notes