from typing import Optional
import logging
from fastapi import FastAPI
from sqlmodel import SQLModel
from settings import Config


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
        "support_email": Config.SUPPORT_EMAIL,
    }
