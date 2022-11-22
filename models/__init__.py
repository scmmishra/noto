# https://github.com/tiangolo/sqlmodel/issues/254
from sqlalchemy import Column

from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel
from sqlmodel import Field, DateTime
from datetime import datetime

if TYPE_CHECKING:
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
