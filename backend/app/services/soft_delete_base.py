from typing import Generic, TypeVar, cast

from sqlalchemy.orm import Session

from app.db.base import BaseModel
from app.repositories.soft_delete_base import SoftDeleteBaseRepository
from app.services.base import BaseService

T = TypeVar("T", bound=BaseModel)


class SoftDeleteService(BaseService[T], Generic[T]):
    def __init__(self, repository: SoftDeleteBaseRepository[T]):
        super().__init__(repository)

    @property
    def soft_repo(self) -> SoftDeleteBaseRepository[T]:
        return cast(SoftDeleteBaseRepository[T], self.repository)

    def get_including_deleted(self, session: Session, id: int) -> T | None:
        return self.soft_repo.get_including_deleted(session, id)
