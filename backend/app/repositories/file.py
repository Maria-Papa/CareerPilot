from app.models import File
from app.repositories import BaseRepository


class FileRepository(BaseRepository[File]):
    def __init__(self):
        super().__init__(File)
