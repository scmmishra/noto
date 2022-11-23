import logging
from sqlmodel import SQLModel, Session, select
from pydantic import EmailStr, HttpUrl
from settings import Config

from models.user import User
from models.team import Team
from models.post import ChangelogPost
from models.team_membership import RoleEnum

from errors.debug import DebugModeOnlyError

logger = logging.getLogger(Config.APP_NAME)

# load faker only if we are in debug mode
if Config.DEBUG:
    from faker import Faker
    from mdgen import MarkdownPostProvider

    fake = Faker()
    fake.add_provider(MarkdownPostProvider)

import contextlib
from sqlalchemy import MetaData


def reset_db():
    if not Config.DEBUG:
        raise DebugModeOnlyError("This action is only available in debug mode.")
    meta = MetaData()
    print("Dropping all tables")
    with contextlib.closing(Config.engine.connect()) as con:
        trans = con.begin()
        for table in reversed(SQLModel.metadata.sorted_tables):
            print(table)
            con.execute(table.delete())
        trans.commit()


def make_demo_user(first_name=None, last_name=None):
    if not Config.DEBUG:
        raise DebugModeOnlyError("This action is only available in debug mode.")

    first_name = first_name if first_name else fake.unique.first_name()

    return User(
        first_name=first_name,
        last_name=last_name if last_name else fake.last_name(),
        email=EmailStr(first_name.lower() + "@example.com"),
        avatar=fake.file_path(depth=2, category="image"),
    )


def make_demo_team(owner: User, name=None, tagline=None, website_url=None):
    if not Config.DEBUG:
        raise DebugModeOnlyError("This action is only available in debug mode.")

    url = website_url if website_url else fake.url()

    return Team(
        name=name if name else fake.company(),
        tagline=tagline if tagline else fake.catch_phrase(),
        website_url=HttpUrl(url=url, scheme="https"),
        team_logo=fake.file_path(depth=2, category="image"),
        subdomain=name.lower() if name else fake.slug(),
        owner_id=owner.id or 0,
        owner=owner,
    )


def make_demo_post(team: Team):
    if not Config.DEBUG:
        raise DebugModeOnlyError("This action is only available in debug mode.")

    return ChangelogPost(
        title=fake.sentence(),
        short_description=fake.paragraph(nb_sentences=3),
        content=fake.post(size="medium"),
        for_team_id=team.id,
        published_on=fake.date_time_between(start_date="-1y", end_date="now"),
        author_id=team.owner_id,
        slug=fake.slug(),
    )


def build():
    if not Config.DEBUG:
        raise DebugModeOnlyError("This action is only available in debug mode.")

    reset_db()

    with Session(Config.engine) as session:
        faris = make_demo_user("Faris", "Ansari")
        shivam = make_demo_user("Shivam", "Mishra")

        users = [faris, shivam]

        for _ in range(10):
            user = make_demo_user()
            users.append(user)

        session.add_all(users)
        session.commit()

        session.refresh(faris)
        session.refresh(shivam)

        gameplan = make_demo_team(
            faris,
            "Gameplan",
            "Gameplan is a better way to communicate with your team.",
            "gameplan.so",
        )

        session.add(gameplan)
        session.commit()
        session.refresh(gameplan)

        gameplan.add_member(faris, RoleEnum.admin)
        gameplan.add_member(shivam, RoleEnum.admin)

        for user in users:
            if user.id in [faris.id, shivam.id]:
                continue
            session.refresh(user)
            gameplan.add_member(user)

        posts = []
        for _ in range(25):
            post = make_demo_post(gameplan)
            posts.append(post)

        session.add_all(posts)
        session.commit()
