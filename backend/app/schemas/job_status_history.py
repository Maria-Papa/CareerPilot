from pydantic import BaseModel
from app.enums import JobStatus
from .base import TimestampRead, SoftDeleteRead


class JobStatusHistoryBase(BaseModel):
    job_id: int
    status: JobStatus


class JobStatusHistoryCreate(JobStatusHistoryBase):
    pass


class JobStatusHistoryUpdate(BaseModel):
    job_id: int | None = None
    status: JobStatus | None = None


class JobStatusHistoryRead(JobStatusHistoryBase, TimestampRead, SoftDeleteRead):
    id: int

    class Config:
        from_attributes = True
