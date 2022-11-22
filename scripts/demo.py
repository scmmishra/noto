import logging
from sqlmodel import Session
from pydantic import EmailStr, HttpUrl
from settings import Config

from models.user import User
from models.team import Team
from models.post import ChangelogPost
from models.team_membership import RoleEnum

from errors.debug import OnlyDebugError

logger = logging.getLogger(Config.APP_NAME)

# load faker only if we are in debug mode
if Config.DEBUG:
    from faker import Faker
    from mdgen import MarkdownPostProvider

    fake = Faker()
    fake.add_provider(MarkdownPostProvider)


def make_demo_user(first_name=None, last_name=None):
    if not Config.DEBUG:
        raise OnlyDebugError("This action is only available in debug mode.")

    first_name = first_name if first_name else fake.first_name()

    return User(
        first_name=first_name,
        last_name=last_name if last_name else fake.last_name(),
        email=EmailStr(first_name.lower() + "@example.com"),
        avatar=fake.file_path(depth=2, category="image"),
    )


def make_demo_team(owner: User, name=None, tagline=None, website_url=None):
    if not Config.DEBUG:
        raise OnlyDebugError("This action is only available in debug mode.")

    url = website_url if website_url else fake.url()

    return Team(
        name=name if name else fake.company(),
        tagline=tagline if tagline else fake.catch_phrase(),
        website_url=HttpUrl(url=url, scheme="https"),
        subdomain=name.lower() if name else fake.slug(),
        owner_id=owner.id or 0,
        owner=owner,
    )


def make_demo_post(team: Team):
    if not Config.DEBUG:
        raise OnlyDebugError("This action is only available in debug mode.")

    post = ChangelogPost(
        title=fake.sentence(),
        short_description=fake.paragraph(nb_sentences=3),
        content=fake.markdown_post(),
        for_team_id=team.id,
        published_on=fake.date_time_between(start_date="-1y", end_date="now"),
        author_id=team.owner_id,
        slug=fake.slug(),
    )


def build():
    if not Config.DEBUG:
        raise OnlyDebugError("This action is only available in debug mode.")

    faris = make_demo_user("Faris", "Ansari")
    shivam = make_demo_user("Shivam", "Mishra")

    users = [faris, shivam]

    for _ in range(10):
        user = make_demo_user()
        users.append(user)

    with Session(Config.engine) as session:
        session.add_all(users)
        session.commit()

        gameplan = make_demo_team(
            faris,
            "Gameplan",
            "Gameplan is a better way to communicate with your team.",
            "gameplan.so",
        )

        session.add(gameplan)
        session.commit()
        gameplan.add_member(faris, RoleEnum.admin)
        gameplan.add_member(shivam, RoleEnum.admin)

        for user in users:
            gameplan.add_member(user)

        for _ in range(25):
            post = make_demo_post(gameplan)
            session.add(post)
