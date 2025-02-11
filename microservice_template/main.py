import os
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from microservice_template.config.db_config import db_create_all, get_db
from microservice_template.db.db import db_create_note
from microservice_template.schemas.note import ReturnNote, CreateNote


load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"current environment is {os.environ.get("ENVIRONMENT")}")
    db_create_all()
    yield

app = FastAPI(lifespan=lifespan,
              root_path=os.environ.get("ROOT_PATH"),
              openapi_url=os.environ.get("OPENAPI_URL")
              )


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/create_note", response_model=ReturnNote)
async def create_note(note_data: CreateNote, db: Annotated[Session, Depends(get_db)]):
    new_note = db_create_note(note_data, db)
    return new_note