from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base


class Task(Base):
    id: Mapped[str] = mapped_column(String, primary_key=True)
    params: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    text: Mapped[str]
    period: Mapped[str] = mapped_column(String, nullable=True)

    user: Mapped["User"] = relationship(back_populates="tasks")


class User(Base):

    id: Mapped[int]
    username: Mapped[str] = mapped_column(String, nullable=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)

    delay_times: Mapped[str]
    auto_delay_time: Mapped[str]

    tasks: Mapped[list[Task]] = relationship(back_populates="user")

