from app.models import JobStatusHistory
from app.repositories import BaseRepository


class JobStatusHistoryRepository(BaseRepository[JobStatusHistory]):
    def __init__(self):
        super().__init__(JobStatusHistory)
