from app.models import File
from app.repositories import SoftDeleteBaseRepository


class FileRepository(SoftDeleteBaseRepository[File]):
    def __init__(self):
        super().__init__(File)
