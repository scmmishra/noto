from typing import List, Optional, TYPE_CHECKING
from pydantic import FileUrl, EmailStr
from sqlmodel import Field, SQLModel, Relationship
from api.mixins.timestamp import TimeStampMixin

if TYPE_CHECKING:
    from api.public.team.models import Team
    from api.public.post.models import ChangelogPost


class UserBase(TimeStampMixin, SQLModel):
    first_name: str = Field()
    email: EmailStr = Field(default=None, unique=True, index=True, nullable=False)
    last_name: str = Field()
    avatar: Optional[FileUrl] = Field(default=None, nullable=True)


class User(TimeStampMixin, SQLModel, table=True):
    """User model"""

    id: Optional[int] = Field(default=None, primary_key=True)
    ownerships: List["Team"] = Relationship(back_populates="owner")
    is_active: bool = Field(default=True, nullable=False, index=True)
    changelog_posts: List["ChangelogPost"] = Relationship(back_populates="author")


class UserCreate(UserBase):
    """User create model"""


class UserUpdate(UserBase):
    """User update model"""
