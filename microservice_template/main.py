import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"current environment is {os.environ.get("ENVIRONMENT")}")
    yield

app = FastAPI(lifespan=lifespan,
              root_path=os.environ.get("ROOT_PATH"),
              openapi_url=f"/{os.environ.get("ROOT_PATH")}/openapi.json",
              )


@app.get("/")
async def root():
    return {"message": "Hello World"}