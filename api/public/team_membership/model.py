from typing import Optional
from enum import Enum
from sqlmodel import Field, SQLModel


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
