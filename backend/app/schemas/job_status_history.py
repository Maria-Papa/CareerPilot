from pydantic import BaseModel
from app.enums import JobStatus
from app.schemas import TimestampRead


class JobStatusHistoryBase(BaseModel):
    job_id: int
    status: JobStatus


class JobStatusHistoryCreate(JobStatusHistoryBase):
    pass


class JobStatusHistoryUpdate(BaseModel):
    job_id: int | None = None
    status: JobStatus | None = None


class JobStatusHistoryRead(JobStatusHistoryBase, TimestampRead):
    id: int

    class Config:
        from_attributes = True
