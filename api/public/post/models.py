from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy import Column

from typing import Optional
from pydantic import FileUrl
from sqlmodel import Field, SQLModel, Relationship, DateTime
from api.mixins.timestamp import TimeStampMixin
from datetime import datetime

from api.public.team.models import Team
from api.public.user.models import User


class ChangelogPostBase(TimeStampMixin, SQLModel):
    title: str = Field(max_length=120, nullable=False)
    slug: str = Field(max_length=120, nullable=False, unique=True)
    short_description: str = Field(max_length=250, nullable=False)
    content: str = Field(sa_column=Column(TEXT))
    hero_image: Optional[FileUrl] = Field(default=None)
    for_team_id: int = Field(default=None, foreign_key="team.id")
    tags: Optional[str] = Field(default=None, nullable=True)

    published_on: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            default=None,
            nullable=True,
        )
    )


class ChangelogPost(ChangelogPostBase, table=True):
    """ChangelogPost model"""

    id: int = Field(default=None, primary_key=True)
    author_id: Optional[int] = Field(default=None, foreign_key="user.id")
    for_team: Team = Relationship(back_populates="changelog_posts")
    author: "User" = Relationship(back_populates="changelog_posts")


class ChangelogPostCreate(ChangelogPostBase):
    pass


class CHangelogPostRead(ChangelogPostBase):
    id: int
    author_id: int


class CHangelogPostUpdate(ChangelogPostBase):
    pass
