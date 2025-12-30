from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import (
    Boolean,
    Index,
    Integer,
    ForeignKey,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.models import Base

if TYPE_CHECKING:
    from app.models import Job, File


class JobFileAttachment(Base):
    __tablename__ = "job_file_attachments"
    __table_args__ = (
        UniqueConstraint("job_id", "file_id", "version", name="uq_job_file_version"),
        Index("idx_job_file_active", "job_id", "is_active"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id", ondelete="CASCADE"), index=True
    )
    file_id: Mapped[int] = mapped_column(ForeignKey("files.id"))
    version: Mapped[int] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    attached_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    detached_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    job: Mapped["Job"] = relationship(back_populates="attachments")
    file: Mapped["File"] = relationship(back_populates="attachments")

    def __repr__(self) -> str:
        return (
            f"JobFileAttachment(id={self.id!r}, job_id={self.job_id!r}, "
            f"file_id={self.file_id!r}, version={self.version!r}, "
            f"is_active={self.is_active!r})"
        )
