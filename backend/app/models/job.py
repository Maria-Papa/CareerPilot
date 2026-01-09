from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import (
    Enum,
    Index,
    String,
    Integer,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from app.enums import EmploymentType, FlexibilityType, JobStatus
from app.models import TimestampMixin, SoftDeleteMixin
from app.db import BaseModel

if TYPE_CHECKING:
    from app.models import (
        Company,
        Location,
        User,
        Interview,
        JobEvent,
        JobFileAttachment,
        JobTag,
        JobStatusHistory,
    )


class Job(BaseModel, TimestampMixin, SoftDeleteMixin):
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
    employment_type: Mapped[EmploymentType | None] = mapped_column(
        Enum(
            EmploymentType,
            name="employment_type_enum",
            native_enum=False,
            validate_strings=True,
        ),
        nullable=True,
    )
    flexibility: Mapped[FlexibilityType | None] = mapped_column(
        Enum(
            FlexibilityType,
            name="flexibility_type_enum",
            native_enum=False,
            validate_strings=True,
        ),
        nullable=True,
    )

    description_html: Mapped[str | None] = mapped_column(Text)
    description_text: Mapped[str | None] = mapped_column(Text)
    job_url: Mapped[str | None] = mapped_column(String(1024))

    salary_gross_given: Mapped[int | None] = mapped_column(Integer)
    salary_gross_calculated: Mapped[int | None] = mapped_column(Integer)
    salary_net: Mapped[int | None] = mapped_column(Integer)

    current_status: Mapped[JobStatus] = mapped_column(
        Enum(
            JobStatus, name="job_status_enum", native_enum=False, validate_strings=True
        ),
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="jobs")
    company: Mapped["Company"] = relationship(back_populates="jobs")
    location: Mapped["Location | None"] = relationship(back_populates="jobs")

    status_history: Mapped[list["JobStatusHistory"]] = relationship(
        back_populates="job",
        cascade="all, delete-orphan",
    )

    events: Mapped[list["JobEvent"]] = relationship(
        back_populates="job",
        cascade="all, delete-orphan",
    )

    interviews: Mapped[list["Interview"]] = relationship(
        back_populates="job",
        cascade="all, delete-orphan",
    )

    attachments: Mapped[list["JobFileAttachment"]] = relationship(
        back_populates="job",
        cascade="all, delete-orphan",
    )

    job_tag_links: Mapped[list["JobTag"]] = relationship(
        back_populates="job",
        cascade="all, delete-orphan",
    )
    tags = association_proxy("job_tag_links", "tag")

    def __repr__(self) -> str:
        return (
            f"Job(id={self.id!r}, user_id={self.user_id!r}, company_id={self.company_id!r}, "
            f"title={self.title!r}, current_status={self.current_status!r})"
        )
