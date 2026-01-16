from app.models.job_tag import JobTag
from app.repositories.base import BaseRepository


class JobTagRepository(BaseRepository[JobTag]):
    def __init__(self):
        super().__init__(JobTag)
