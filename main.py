import logging
from fastapi import FastAPI, HTTPException, status
from settings import Config
from errors import DebugModeOnlyError
from scripts.demo import build

from database import create_db_and_tables

logger = logging.getLogger(Config.APP_NAME)

app = FastAPI()


@app.on_event("startup")
def on_startup():
    logger.info("Creating database and tables")
    create_db_and_tables()


@app.get("/build-demo")
async def build_demo():
    try:
        build()
        return {"message": "Demo data built"}
    except DebugModeOnlyError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
