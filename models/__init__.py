# https://github.com/tiangolo/sqlmodel/issues/254
from sqlalchemy import Column

from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, DateTime, Relationship
from datetime import datetime

from models.user import User


class TimeStampMixin(BaseModel):
    created_on: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            default=datetime.utcnow,
            nullable=False,
        )
    )

    updated_on: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            default=datetime.utcnow,
            nullable=False,
        )
    )


class PublishableMixin(BaseModel):
    published_on: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            default=None,
            nullable=True,
        )
    )
    author_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    # author: User = Relationship(back_populates="posts")
