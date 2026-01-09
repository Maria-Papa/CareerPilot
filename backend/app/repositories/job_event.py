from app.models import JobEvent
from app.repositories import BaseRepository


class JobEventRepository(BaseRepository[JobEvent]):
    def __init__(self):
        super().__init__(JobEvent)
