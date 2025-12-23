from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Enum, ForeignKey, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.enums import JobEventType
from app.models import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models import Job


class JobEvent(Base, TimestampMixin):
    __tablename__ = "job_events"
    __table_args__ = (
        Index("idx_job_events_job_id_created_at", "job_id", "created_at"),
        Index("idx_job_events_event_type", "event_type"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id", ondelete="CASCADE"), index=True
    )
    event_type: Mapped[JobEventType] = mapped_column(
        Enum(
            JobEventType,
            name="job_event_type_enum",
            native_enum=False,
            validate_strings=True,
        ),
        nullable=False,
    )
    payload: Mapped[dict | None] = mapped_column(JSON)

    job: Mapped["Job"] = relationship(back_populates="events")
