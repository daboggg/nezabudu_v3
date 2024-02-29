from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from models import Base


class Task(Base):

    params: Mapped[str]
    chat_id: Mapped[int]
    text: Mapped[str]
    period: Mapped[str] = mapped_column(String, nullable=True)
