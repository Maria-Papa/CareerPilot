from pydantic import BaseModel
from app.enums import JobEventType
from .base import TimestampRead, SoftDeleteRead


class JobEventBase(BaseModel):
    job_id: int
    event_type: JobEventType
    payload: dict | None = None


class JobEventCreate(JobEventBase):
    pass


class JobEventUpdate(BaseModel):
    job_id: int | None = None
    event_type: JobEventType | None = None
    payload: dict | None = None


class JobEventRead(JobEventBase, TimestampRead, SoftDeleteRead):
    id: int

    class Config:
        from_attributes = True
