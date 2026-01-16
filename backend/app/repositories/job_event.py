from app.models.job_event import JobEvent
from app.repositories.base import BaseRepository


class JobEventRepository(BaseRepository[JobEvent]):
    def __init__(self):
        super().__init__(JobEvent)
