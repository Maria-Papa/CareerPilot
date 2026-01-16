from __future__ import annotations

from typing import TYPE_CHECKING

from app.db.base import BaseModel
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models import Job, Tag


class JobTag(BaseModel):
    __tablename__ = "job_tags"
    __table_args__ = (UniqueConstraint("job_id", "tag_id", name="uq_job_tag"),)

    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id", ondelete="CASCADE"))
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id", ondelete="CASCADE"))

    job: Mapped["Job"] = relationship(back_populates="job_tag_links")
    tag: Mapped["Tag"] = relationship(back_populates="job_tag_links")
