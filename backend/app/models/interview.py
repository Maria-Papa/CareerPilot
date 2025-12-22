from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, Index, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.enums import InterviewOutcome, InterviewType
from app.models import Base

if TYPE_CHECKING:
    from app.models import Job


class Interview(Base):
    __tablename__ = "interviews"
    __table_args__ = (
        Index("idx_interviews_job_id_scheduled_at", "job_id", "scheduled_at"),
        Index("idx_interviews_interview_type", "interview_type"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id", ondelete="CASCADE"), index=True
    )
    interview_type: Mapped[InterviewType] = mapped_column(SmallInteger)
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    outcome: Mapped[InterviewOutcome | None] = mapped_column(SmallInteger)
    notes: Mapped[str | None] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    job: Mapped["Job"] = relationship(back_populates="interviews")
