from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy import Column

from typing import Optional
from pydantic import FileUrl
from sqlmodel import Field, SQLModel, Relationship
from api.mixins.timestamp import TimeStampMixin
from sqlmodel import Field, DateTime
from datetime import datetime

from api.public.team.model import Team
from api.public.user.model import User


class ChangelogPost(TimeStampMixin, SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(max_length=120, nullable=False)
    slug: str = Field(max_length=120, nullable=False, unique=True)
    short_description: str = Field(max_length=250, nullable=False)
    content: str = Field(sa_column=Column(TEXT))
    hero_image: Optional[FileUrl] = Field(default=None)
    for_team_id: int = Field(default=None, foreign_key="team.id")
    for_team: Team = Relationship(back_populates="changelog_posts")
    tags: Optional[str] = Field(default=None, nullable=True)

    published_on: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            default=None,
            nullable=True,
        )
    )
    author_id: Optional[int] = Field(default=None, foreign_key="user.id")
    author: "User" = Relationship(back_populates="changelog_posts")
