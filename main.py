import logging
from fastapi import FastAPI
from sqlmodel import SQLModel, Session
from pydantic import EmailStr
from settings import Config

from models.user import User
from models.team import Team


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
    if not Config.DEBUG:
        return {"error": "This endpoint is only available in debug mode."}

    from faker import Faker

    fake = Faker()

    user = User(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        avatar=fake.file_path(depth=2, category="image"),
        email=EmailStr(fake.email()),
    )
    print(fake.file_path(depth=2, category="image"))

    with Session(Config.engine) as session:
        session.add(user)
        session.commit()

        team = Team(
            name=fake.company(),
            tagline=fake.catch_phrase(),
            website_url=fake.domain_name(),
            owner_id=user.id or 0,
        )

        session.add(team)
        session.commit()
