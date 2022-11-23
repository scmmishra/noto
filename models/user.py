from typing import List, Optional, TYPE_CHECKING
from pydantic import FileUrl, EmailStr
from sqlmodel import Field, SQLModel, Relationship
from models import TimeStampMixin

if TYPE_CHECKING:
    from models.team import Team
    from models.post import ChangelogPost


class User(TimeStampMixin, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field()
    email: EmailStr = Field(default=None, unique=True, index=True, nullable=False)
    last_name: Optional[str] = Field()
    avatar: Optional[FileUrl] = Field(default=None, nullable=True)
    is_active: bool = Field(default=True, nullable=False, index=True)
    ownerships: List["Team"] = Relationship(back_populates="owner")
    changelog_posts: List["ChangelogPost"] = Relationship(back_populates="author")
