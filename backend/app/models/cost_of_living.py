from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Index, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.models import Base

if TYPE_CHECKING:
    from app.models import Location


class CostOfLiving(Base):
    __tablename__ = "cost_of_living"
    __table_args__ = (
        Index("idx_col_location_id", "location_id"),
        Index("idx_col_yearly_cost", "yearly_cost"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"), index=True)
    yearly_cost: Mapped[int] = mapped_column(Integer)  # stored in cents
    title: Mapped[str | None] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    location: Mapped["Location"] = relationship()
