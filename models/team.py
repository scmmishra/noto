from typing import Optional
from pydantic import FileUrl, HttpUrl
from sqlmodel import Field, SQLModel, Relationship

from models.user import User


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    website_url: Optional[HttpUrl] = Field(default=None)
    tagline: Optional[str] = Field(nullable=True)
    team_logo: Optional[FileUrl] = Field(default=None, nullable=True)
    owner_id: int = Field(default=None, foreign_key="user.id")
    # owner: User = Relationship(back_populates="users")
