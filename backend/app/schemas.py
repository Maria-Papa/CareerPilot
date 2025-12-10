from pydantic import BaseModel
from typing import Optional
from datetime import date


class JobBase(BaseModel):
    company: Optional[str] = None
    position_title: Optional[str] = None
    position_generalized: Optional[str] = None
    url: Optional[str] = None
    location: Optional[str] = None
    expected_salary: Optional[float] = None
    given_salary: Optional[float] = None
    flexibility: Optional[str] = None
    status: Optional[str] = None
    application_date: Optional[date] = None
    rejection_date: Optional[date] = None
    saved_date: Optional[date] = None
    declined_date: Optional[date] = None
    rejected_reason: Optional[str] = None
    cv_path: Optional[str] = None
    cover_letter_path: Optional[str] = None
    notes: Optional[str] = None


class JobCreate(JobBase):
    pass


class JobUpdate(JobBase):
    pass


class Job(JobBase):
    id: int

    class Config:
        orm_mode = True
