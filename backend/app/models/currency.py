from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models import Base

if TYPE_CHECKING:
    from app.models import Location


class Currency(Base):
    __tablename__ = "currencies"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(3), unique=True)
    symbol: Mapped[str | None] = mapped_column(String(5))

    locations: Mapped[list["Location"]] = relationship(back_populates="currency")
