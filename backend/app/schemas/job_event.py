from app.enums.job_event_type import JobEventType
from app.schemas.base import ORMBase, TimestampRead


class JobEventBase(ORMBase):
    event_type: JobEventType
    payload: dict | None = None


class JobEventCreate(JobEventBase):
    pass


class JobEventUpdate(ORMBase):
    event_type: JobEventType | None = None
    payload: dict | None = None


class JobEventRead(JobEventBase, TimestampRead):
    id: int
    job_id: int
