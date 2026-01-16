from app.enums.job_status import JobStatus
from app.schemas import ORMBase, TimestampRead


class JobStatusHistoryBase(ORMBase):
    status: JobStatus


class JobStatusHistoryCreate(JobStatusHistoryBase):
    pass


class JobStatusHistoryUpdate(ORMBase):
    status: JobStatus | None = None


class JobStatusHistoryRead(JobStatusHistoryBase, TimestampRead):
    id: int
    job_id: int
