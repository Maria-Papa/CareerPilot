from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Root declarative base."""

    pass


class BaseModel(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
