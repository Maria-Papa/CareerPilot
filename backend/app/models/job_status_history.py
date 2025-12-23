from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Enum, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.enums import JobStatus
from app.models import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models import Job


class JobStatusHistory(Base, TimestampMixin):
    __tablename__ = "job_status_history"
    __table_args__ = (
        Index("idx_job_status_history_job_id_created_at", "job_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id", ondelete="CASCADE"), index=True
    )
    status: Mapped[JobStatus] = mapped_column(
        Enum(
            JobStatus,
            name="job_status_enum",
            native_enum=False,
            validate_strings=True,
        ),
        nullable=False,
    )

    job: Mapped["Job"] = relationship(back_populates="status_history")
