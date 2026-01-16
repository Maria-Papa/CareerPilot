from datetime import datetime

from app.schemas import ORMBase, SoftDeleteRead, TimestampRead


class JobFileAttachmentBase(ORMBase):
    file_id: int
    version: int


class JobFileAttachmentCreate(JobFileAttachmentBase):
    attached_at: datetime


class JobFileAttachmentUpdate(ORMBase):
    file_id: int | None = None
    version: int | None = None


class JobFileAttachmentDetach(ORMBase):
    detached_at: datetime


class JobFileAttachmentRead(JobFileAttachmentBase, TimestampRead, SoftDeleteRead):
    id: int
    job_id: int
    is_active: bool
    attached_at: datetime
    detached_at: datetime | None
