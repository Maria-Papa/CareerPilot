from typing import Sequence

from app.core.errors import EntityNotFoundError
from app.models import File
from app.repositories.file import FileRepository
from app.repositories.user import UserRepository
from app.schemas import FileCreate, FileUpdate
from app.services.soft_delete_base import SoftDeleteService
from sqlalchemy.orm import Session


class FileService(SoftDeleteService[File]):
    def __init__(
        self,
        repository: FileRepository | None = None,
        user_repo: UserRepository | None = None,
    ) -> None:
        super().__init__(repository or FileRepository())
        self.user_repo = user_repo or UserRepository()

    def _validate_user(self, session: Session, user_id: int) -> None:
        if self.user_repo.get(session, user_id) is None:
            raise EntityNotFoundError("User not found")

    def list_user_files(
        self, session: Session, user_id: int, *, offset: int = 0, limit: int = 100
    ) -> Sequence[File]:
        self._validate_user(session, user_id)
        files = self.find(session, user_id=user_id)
        return files[offset : offset + limit]

    def create_file(self, session: Session, data: FileCreate) -> File:
        self._validate_user(session, data.user_id)
        file = File(**data.model_dump())
        return self.create(session, file)

    def update_file(self, session: Session, file: File, data: FileUpdate) -> File:
        values = data.model_dump(exclude_unset=True)
        if "user_id" in values:
            self._validate_user(session, values["user_id"])
        return self.update(session, file, values)

    def get_including_deleted(self, session: Session, id: int) -> File:
        file = self.soft_repo.get_including_deleted(session, id)
        if file is None:
            raise EntityNotFoundError("File not found")
        return file
