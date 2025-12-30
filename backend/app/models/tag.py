from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from app.models import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models import JobTag


class Tag(Base, TimestampMixin):
    __tablename__ = "tags"
    __table_args__ = (Index("idx_tags_name", "name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    job_tag_links: Mapped[list["JobTag"]] = relationship(
        back_populates="tag",
        cascade="all, delete-orphan",
    )
    jobs = association_proxy("job_tag_links", "job")

    def __repr__(self) -> str:
        return f"Tag(id={self.id!r}, name={self.name!r})"
