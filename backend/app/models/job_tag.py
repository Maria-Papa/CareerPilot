from __future__ import annotations
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models import Base, Job, Tag


class JobTag(Base):
    __tablename__ = "job_tags"

    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id", ondelete="CASCADE"), primary_key=True
    )
    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    )

    job: Mapped["Job"] = relationship(back_populates="tags")
    tag: Mapped["Tag"] = relationship(back_populates="jobs")
