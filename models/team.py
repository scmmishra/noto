from typing import Optional, List, TYPE_CHECKING
from pydantic import FileUrl, HttpUrl
from sqlmodel import Field, SQLModel, Relationship
from sqlmodel import Session
from settings import Config

from models.user import User

if TYPE_CHECKING:
    from models.post import ChangelogPost

from models import TimeStampMixin
from models.team_membership import TeamMembershipLink, RoleEnum


class Team(TimeStampMixin, SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    subdomain: str = Field(index=True, unique=True, max_length=50, nullable=False)
    owner_id: int = Field(default=None, foreign_key="user.id")

    website_url: Optional[HttpUrl] = Field(default=None)
    logo: Optional[FileUrl] = Field(default=None)
    tagline: Optional[str] = Field(nullable=True)
    team_logo: Optional[FileUrl] = Field(default=None, nullable=True)
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
