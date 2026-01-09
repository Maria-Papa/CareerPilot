from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models import File
from app.repositories import FileRepository
from app.services import BaseService
from app.schemas import FileCreate, FileUpdate


class FileService(BaseService[File]):
    repository: FileRepository

    def __init__(self):
        super().__init__(FileRepository())

    def create_file(self, session: Session, data: FileCreate) -> File:
        file = File(**data.model_dump())
        return self.create(session, file)

    def update_file(self, session: Session, file: File, data: FileUpdate) -> File:
        values = data.model_dump(exclude_unset=True)
        return self.update(session, file, values)
