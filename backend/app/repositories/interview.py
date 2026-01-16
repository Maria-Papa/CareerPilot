from app.models.interview import Interview
from app.repositories.base import BaseRepository


class InterviewRepository(BaseRepository[Interview]):
    def __init__(self) -> None:
        super().__init__(Interview)
