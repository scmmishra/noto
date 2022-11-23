# https://github.com/tiangolo/sqlmodel/issues/254
from sqlalchemy import Column

from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field, DateTime
from datetime import datetime


class TimeStampMixin(BaseModel):
    """TimeStampMixin to add created_on and updated_on dates"""

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
