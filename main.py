import logging
from fastapi import FastAPI, HTTPException, status
from settings import Config
from errors import DebugModeOnlyError
from scripts.demo import build
from api.public import api as public_api
from database import create_db_and_tables

logger = logging.getLogger(Config.APP_NAME)

app = FastAPI()
app.include_router(public_api)


@app.on_event("startup")
def on_startup():
    logger.info("Creating database and tables")
    create_db_and_tables()


if Config.DEBUG:

    @app.get("/build-demo")
    async def build_demo():
        """Build demo data"""
        try:
            build()
            return {"message": "Demo data built"}
        except DebugModeOnlyError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed"
            )
