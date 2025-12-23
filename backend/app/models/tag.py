from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models import JobTag


class Tag(Base, TimestampMixin):
    __tablename__ = "tags"
    __table_args__ = (Index("idx_tags_name", "name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    jobs: Mapped[list["JobTag"]] = relationship(back_populates="tag")
