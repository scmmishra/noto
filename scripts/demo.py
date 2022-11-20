import logging
from sqlmodel import Session
from pydantic import EmailStr, HttpUrl
from settings import Config

from models.user import User
from models.team import Team
from models.team_membership import TeamMembershipLink, RoleEnum

logger = logging.getLogger(Config.APP_NAME)


def build():
    if not Config.DEBUG:
        return {"error": "This endpoint is only available in debug mode."}

    from faker import Faker

    fake = Faker()

    faris = User(
        first_name="Faris",
        last_name="Ansari",
        email=EmailStr("faris@example.com"),
        avatar=fake.file_path(depth=2, category="image"),
    )

    shivam = User(
        first_name="Shivam",
        last_name="Mishra",
        email=EmailStr("shivam@example.com"),
        avatar=fake.file_path(depth=2, category="image"),
    )

    users = [faris, shivam]

    for _ in range(10):
        user = User(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            avatar=fake.file_path(depth=2, category="image"),
            email=EmailStr(fake.email()),
        )
        users.append(user)

    with Session(Config.engine) as session:
        session.add_all(users)
        session.commit()

        gameplan = Team(
            name="Gameplan",
            tagline="Gameplan is a better way to communicate with your team",
            website_url=HttpUrl(url="gameplan.so", scheme="https"),
            subdomain="gameplan",
            owner_id=faris.id or 0,
            owner=faris,
        )

        noto = Team(
            name="Noto",
            tagline="API first changelog manager for startups and product teams",
            website_url=HttpUrl(url="noto.app", scheme="https"),
            subdomain="feedback",
            owner_id=shivam.id or 0,
            owner=shivam,
        )

        teams = [gameplan, noto]
        session.add_all(teams)
        session.commit()

        memberships = []
        for user in users:
            team_membership = TeamMembershipLink(
                team_id=gameplan.id or 0,
                user_id=user.id or 0,
                role=RoleEnum.member,
            )

            memberships.append(team_membership)

        session.add_all(memberships)
        session.commit()
