from pydantic import BaseModel
from .base import TimestampRead, SoftDeleteRead


class JobTagBase(BaseModel):
    job_id: int
    tag_id: int


class JobTagCreate(JobTagBase):
    pass


class JobTagUpdate(BaseModel):
    job_id: int | None = None
    tag_id: int | None = None


class JobTagRead(JobTagBase, TimestampRead, SoftDeleteRead):
    id: int

    class Config:
        from_attributes = True
