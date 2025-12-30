from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Index, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models import Base, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models import Location


class CostOfLiving(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "cost_of_living"
    __table_args__ = (
        Index("idx_col_location_id", "location_id"),
        Index("idx_col_yearly_cost", "yearly_cost"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"), index=True)
    yearly_cost: Mapped[int] = mapped_column(Integer)  # stored in cents
    title: Mapped[str | None] = mapped_column(String(100))

    location: Mapped["Location"] = relationship(back_populates="cost_of_living_entries")

    def __repr__(self) -> str:
        return f"CostOfLiving(id={self.id!r}, location_id={self.location_id!r}, yearly_cost={self.yearly_cost!r})"
