from pydantic import BaseModel
from app.enums import EmploymentType, FlexibilityType, JobStatus
from app.schemas import TimestampRead, SoftDeleteRead


class JobBase(BaseModel):
    user_id: int
    company_id: int
    location_id: int | None = None
    title: str
    employment_type: EmploymentType | None = None
    flexibility: FlexibilityType | None = None
    description_html: str | None = None
    description_text: str | None = None
    job_url: str | None = None
    salary_gross_given: int | None = None
    salary_gross_calculated: int | None = None
    salary_net: int | None = None
    current_status: JobStatus


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    user_id: int | None = None
    company_id: int | None = None
    location_id: int | None = None
    title: str | None = None
    employment_type: EmploymentType | None = None
    flexibility: FlexibilityType | None = None
    description_html: str | None = None
    description_text: str | None = None
    job_url: str | None = None
    salary_gross_given: int | None = None
    salary_gross_calculated: int | None = None
    salary_net: int | None = None
    current_status: JobStatus | None = None


class JobRead(JobBase, TimestampRead, SoftDeleteRead):
    id: int

    class Config:
        from_attributes = True
