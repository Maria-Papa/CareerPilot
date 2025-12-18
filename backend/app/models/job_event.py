from __future__ import annotations
from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, JSON, Index, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.enums import JobEventType
from app.models import Base, Job


class JobEvent(Base):
    __tablename__ = "job_events"
    __table_args__ = (
        Index("idx_job_events_job_id_created_at", "job_id", "created_at"),
        Index("idx_job_events_event_type", "event_type"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id", ondelete="CASCADE"), index=True
    )
    event_type: Mapped[JobEventType] = mapped_column(SmallInteger)
    payload: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    job: Mapped[Job] = relationship(back_populates="events")
