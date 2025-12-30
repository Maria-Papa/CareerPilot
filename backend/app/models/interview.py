from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Enum, ForeignKey, DateTime, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.enums import InterviewOutcome, InterviewType
from app.models import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models import Job


class Interview(Base, TimestampMixin):
    __tablename__ = "interviews"
    __table_args__ = (
        Index("idx_interviews_job_id_scheduled_at", "job_id", "scheduled_at"),
        Index("idx_interviews_interview_type", "interview_type"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id", ondelete="CASCADE"), index=True
    )
    interview_type: Mapped[InterviewType] = mapped_column(
        Enum(
            InterviewType,
            name="interview_type_enum",
            native_enum=False,
            validate_strings=True,
        ),
        nullable=False,
    )
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    outcome: Mapped[InterviewOutcome | None] = mapped_column(
        Enum(
            InterviewOutcome,
            name="interview_outcome_enum",
            native_enum=False,
            validate_strings=True,
        ),
        nullable=True,
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    job: Mapped["Job"] = relationship(back_populates="interviews")

    def __repr__(self) -> str:
        return (
            f"Interview(id={self.id!r}, job_id={self.job_id!r}, "
            f"interview_type={self.interview_type!r}, scheduled_at={self.scheduled_at!r}, "
            f"outcome={self.outcome!r})"
        )
