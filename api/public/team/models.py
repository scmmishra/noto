from typing import Optional, List, TYPE_CHECKING
from pydantic import FileUrl, HttpUrl
from enum import Enum

from sqlmodel import Session, Field, SQLModel, Relationship

from settings import Config

from api.public.user.models import User
from api.mixins.timestamp import TimeStampMixin

if TYPE_CHECKING:
    from api.public.post.models import ChangelogPost


class RoleEnum(str, Enum):
    """RoleEnum enum"""

    admin = "admin"
    member = "member"


class TeamMembershipLink(SQLModel, table=True):
    """Team membership link model"""

    team_id: Optional[int] = Field(
        default=None, foreign_key="team.id", primary_key=True
    )
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    role: RoleEnum = Field(default="member", max_length=50, nullable=False)


class TeamBase(TimeStampMixin, SQLModel):
    name: str = Field(index=True)
    subdomain: str = Field(index=True, unique=True, max_length=50, nullable=False)
    owner_id: int = Field(default=None, foreign_key="user.id")
    website_url: Optional[HttpUrl] = Field(default=None)
    logo: Optional[FileUrl] = Field(default=None, nullable=True)
    tagline: Optional[str] = Field(nullable=True)


class Team(TeamBase, table=True):
    """Team model"""

    id: int = Field(default=None, primary_key=True)
    owner: User = Relationship(back_populates="ownerships")
    changelog_posts: List["ChangelogPost"] = Relationship(back_populates="for_team")

    def add_member(self, user: User, role: RoleEnum = RoleEnum.member):
        """Add a member to a team."""
        with Session(Config.engine) as session:
            team_membership = TeamMembershipLink(
                team_id=self.id,
                user_id=user.id,
                role=role,
            )

            print(self.id, self)

            session.add(team_membership)
            session.commit()

            return team_membership


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    id: int


class TeamUpdate(TeamBase):
    name: Optional[str] = None
    website_url: Optional[str] = None
    logo: Optional[FileUrl] = None
    tagline: Optional[str] = None
