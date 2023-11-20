from typing import Annotated

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

from app import mixins
from app.permissions import Role

IntPK = Annotated[int, mapped_column(primary_key=True)]
UniqueStr = Annotated[str, mapped_column(unique=True)]
UsersFk = Annotated[int, mapped_column(ForeignKey("users.id"))]
str100 = Annotated[str, 100]


class Base(DeclarativeBase):
    """subclasses will be converted to dataclasses"""

    type_annotation_map = {
        str100: String(100),
    }


class Todo(Base):
    """Todo model

    description: Annotated[str, Field(min_length=3, max_length=100)]
    priority: Annotated[int, Field(ge=1, le=5)]
    """

    __tablename__ = "todos"

    id: Mapped[IntPK]
    title: Mapped[str]
    description: Mapped[str100]
    priority: Mapped[int]
    completed: Mapped[bool] = mapped_column(default=False)
    owner_id: Mapped[UsersFk]

    owner: Mapped["User"] = relationship("User", back_populates="todos")


class User(Base, mixins.AuthUserMixin):
    """User model"""

    __tablename__ = "users"

    id: Mapped[IntPK]
    email: Mapped[UniqueStr]
    username: Mapped[UniqueStr]
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone_number: Mapped[str | None]

    hashed_password: Mapped[str]
    role: Mapped[Role]
    is_active: Mapped[bool] = mapped_column(default=False)

    todos: Mapped[list[Todo]] = relationship(
        "Todo", back_populates="owner", cascade="all, delete"
    )
