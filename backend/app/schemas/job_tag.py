from pydantic import BaseModel
from app.schemas import TimestampRead


class JobTagBase(BaseModel):
    job_id: int
    tag_id: int


class JobTagCreate(JobTagBase):
    pass


class JobTagUpdate(BaseModel):
    job_id: int | None = None
    tag_id: int | None = None


class JobTagRead(JobTagBase, TimestampRead):
    id: int

    class Config:
        from_attributes = True
