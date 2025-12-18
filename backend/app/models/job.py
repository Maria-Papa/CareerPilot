from __future__ import annotations
from datetime import datetime
from sqlalchemy import Index, String, Integer, ForeignKey, DateTime, SmallInteger, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.enums import EmploymentType, FlexibilityType, JobStatus
from app.models import (
    Base,
    Company,
    Location,
    User,
    Interview,
    JobEvent,
    JobFileAttachment,
    JobStatusHistory,
)


class Job(Base):
    __tablename__ = "jobs"
    __table_args__ = (
        Index("idx_jobs_user_status", "user_id", "current_status"),
        Index("idx_jobs_location_id", "location_id"),
        Index("idx_jobs_created_at", "created_at"),
        Index("idx_jobs_company_status", "company_id", "current_status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    location_id: Mapped[int | None] = mapped_column(ForeignKey("locations.id"))

    title: Mapped[str] = mapped_column(String(255))
    employment_type: Mapped[EmploymentType | None] = mapped_column(SmallInteger)
    flexibility: Mapped[FlexibilityType | None] = mapped_column(SmallInteger)

    description_html: Mapped[str | None] = mapped_column(Text)
    description_text: Mapped[str | None] = mapped_column(Text)
    job_url: Mapped[str | None] = mapped_column(String(1024))

    salary_gross_given: Mapped[int | None] = mapped_column(Integer)
    salary_gross_calculated: Mapped[int | None] = mapped_column(Integer)
    salary_net: Mapped[int | None] = mapped_column(Integer)

    current_status: Mapped[JobStatus] = mapped_column(SmallInteger)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    user: Mapped[User] = relationship(back_populates="jobs")
    company: Mapped[Company] = relationship(back_populates="jobs")
    location: Mapped[Location | None] = relationship()

    status_history: Mapped[list["JobStatusHistory"]] = relationship(
        back_populates="job", cascade="all, delete-orphan"
    )
    events: Mapped[list["JobEvent"]] = relationship(
        back_populates="job", cascade="all, delete-orphan"
    )
    interviews: Mapped[list["Interview"]] = relationship(
        back_populates="job", cascade="all, delete-orphan"
    )
    attachments: Mapped[list["JobFileAttachment"]] = relationship(
        back_populates="job", cascade="all, delete-orphan"
    )
