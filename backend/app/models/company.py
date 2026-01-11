from __future__ import annotations

from typing import TYPE_CHECKING

from app.db.base import BaseModel
from app.models.mixins import SoftDeleteMixin, TimestampMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models import Job


class Company(BaseModel, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    logo_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    website: Mapped[str | None] = mapped_column(String(255), nullable=True)
    industry: Mapped[str | None] = mapped_column(String(100), nullable=True)

    jobs: Mapped[list["Job"]] = relationship(back_populates="company")

    def __repr__(self) -> str:
        return f"Company(id={self.id!r}, name={self.name!r})"
