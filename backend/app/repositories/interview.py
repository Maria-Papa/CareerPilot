from app.models import Interview
from app.repositories import BaseRepository


class InterviewRepository(BaseRepository[Interview]):
    def __init__(self):
        super().__init__(Interview)
