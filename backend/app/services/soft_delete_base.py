from typing import Generic, TypeVar

from app.db.base import BaseModel
from app.repositories.soft_delete_base import SoftDeleteBaseRepository
from app.services.base import BaseService
from sqlalchemy.orm import Session

T = TypeVar("T", bound=BaseModel)


class SoftDeleteService(BaseService[T], Generic[T]):
    repository: SoftDeleteBaseRepository[T]

    def __init__(self, repository: SoftDeleteBaseRepository[T]):
        super().__init__(repository)
        self.repository = repository

    def restore(self, session: Session, instance: T) -> None:
        self.repository.restore(session, instance)

    def get_including_deleted(self, session: Session, id: int) -> T | None:
        return self.repository.get_including_deleted(session, id)
