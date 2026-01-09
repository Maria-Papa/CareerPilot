from app.models.interview import Interview
from .base import BaseRepository


class InterviewRepository(BaseRepository[Interview]):
    def __init__(self):
        super().__init__(Interview)
