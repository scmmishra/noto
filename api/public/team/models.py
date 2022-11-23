from typing import Optional, List, TYPE_CHECKING
from pydantic import FileUrl, HttpUrl
from sqlmodel import Field, SQLModel, Relationship
from sqlmodel import Session
from settings import Config

from api.public.user.models import User

if TYPE_CHECKING:
    from api.public.post.models import ChangelogPost

from api.mixins.timestamp import TimeStampMixin
from api.public.team_membership.models import TeamMembershipLink, RoleEnum


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
