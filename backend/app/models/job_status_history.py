from __future__ import annotations
from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, Index, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.enums import JobStatus
from app.models import Base, Job


class JobStatusHistory(Base):
    __tablename__ = "job_status_history"
    __table_args__ = (
        Index("idx_job_status_history_job_id_created_at", "job_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id", ondelete="CASCADE"), index=True
    )
    status: Mapped[JobStatus] = mapped_column(SmallInteger)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    job: Mapped[Job] = relationship(back_populates="status_history")
