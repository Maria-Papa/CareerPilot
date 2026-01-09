from app.models.job_status_history import JobStatusHistory
from .base import BaseRepository


class JobStatusHistoryRepository(BaseRepository[JobStatusHistory]):
    def __init__(self):
        super().__init__(JobStatusHistory)
