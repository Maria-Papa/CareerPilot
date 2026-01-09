from app.models import JobTag
from app.repositories import BaseRepository


class JobTagRepository(BaseRepository[JobTag]):
    def __init__(self):
        super().__init__(JobTag)
