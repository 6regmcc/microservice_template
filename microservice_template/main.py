import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from dotenv import load_dotenv

from microservice_template.config.sqlalchemy.db_config import db_create_all

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