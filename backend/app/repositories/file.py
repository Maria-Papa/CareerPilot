from app.models.file import File
from .base import BaseRepository


class FileRepository(BaseRepository[File]):
    def __init__(self):
        super().__init__(File)
