from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models import TimestampMixin
from app.db import BaseModel

if TYPE_CHECKING:
    from app.models import Currency, Job, CostOfLiving


class Location(BaseModel, TimestampMixin):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    country_code: Mapped[str] = mapped_column(String(2), index=True)
    currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id"))

    currency: Mapped["Currency"] = relationship(back_populates="locations")
    jobs: Mapped[list["Job"]] = relationship(back_populates="location")
    cost_of_living_entries: Mapped[list["CostOfLiving"]] = relationship(
        back_populates="location",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"Location(id={self.id!r}, name={self.name!r}, country_code={self.country_code!r})"
