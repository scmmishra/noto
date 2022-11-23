import logging
from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel
from settings import Config
from errors.debug import DebugModeOnlyError
from scripts.demo import build


def create_db_and_tables():
    # create the database and tables
    logger.info("Creating database and tables")
    SQLModel.metadata.create_all(Config.engine)


logger = logging.getLogger(Config.APP_NAME)

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/info")
async def info():
    return {
        "app_name": Config.APP_NAME,
        "app_version": Config.APP_VERSION,
        "support_email": Config.SUPPORT_EMAIL,
    }


@app.get("/ping")
async def pong():
    # ping pong
    return {"ping": "pong!"}


@app.get("/build-demo")
async def build_demo():
    try:
        build()
        return {"message": "Demo data built"}
    except DebugModeOnlyError:
        raise HTTPException(status_code=403, detail="Not allowed")
