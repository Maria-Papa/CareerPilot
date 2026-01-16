from __future__ import annotations

from typing import TYPE_CHECKING

from app.db.base import BaseModel
from app.models.mixins import TimestampMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models import Location


class Currency(BaseModel, TimestampMixin):
    __tablename__ = "currencies"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(3), unique=True)
    symbol: Mapped[str | None] = mapped_column(String(5))

    locations: Mapped[list["Location"]] = relationship(back_populates="currency")

    def __repr__(self) -> str:
        return f"Currency(id={self.id!r}, code={self.code!r})"
