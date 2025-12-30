from datetime import datetime
from pydantic import BaseModel
from .base import TimestampRead, SoftDeleteRead


class JobFileAttachmentBase(BaseModel):
    job_id: int
    file_id: int
    version: int


class JobFileAttachmentCreate(JobFileAttachmentBase):
    attached_at: datetime


class JobFileAttachmentUpdate(BaseModel):
    job_id: int | None = None
    file_id: int | None = None
    version: int | None = None


class JobFileAttachmentDetach(BaseModel):
    detached_at: datetime


class JobFileAttachmentRead(JobFileAttachmentBase, TimestampRead, SoftDeleteRead):
    id: int
    is_active: bool
    attached_at: datetime
    detached_at: datetime | None

    class Config:
        from_attributes = True
