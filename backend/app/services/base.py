# backend/app/services/base.py
from typing import Generic, Sequence, TypeVar

from app.db.base import BaseModel
from app.repositories.base import BaseRepository
from app.repositories.soft_delete_base import SoftDeleteBaseRepository
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseService(Generic[ModelType]):
    def __init__(self, repository: BaseRepository[ModelType]):
        self.repository = repository

    def get(self, session: Session, id: int) -> ModelType | None:
        return self.repository.get(session, id)

    def get_all(
        self, session: Session, *, offset: int = 0, limit: int = 100
    ) -> Sequence[ModelType]:
        return self.repository.get_all(session, offset=offset, limit=limit)

    def find(self, session: Session, **filters) -> Sequence[ModelType]:
        return self.repository.find(session, **filters)

    def find_one(self, session: Session, **filters) -> ModelType | None:
        return self.repository.find_one(session, **filters)

    def create(self, session: Session, instance: ModelType) -> ModelType:
        return self.repository.add(session, instance)

    def update(self, session: Session, instance: ModelType, values: dict) -> ModelType:
        return self.repository.update(session, instance, values)

    def delete(self, session: Session, instance: ModelType) -> None:
        if isinstance(self.repository, SoftDeleteBaseRepository):
            self.repository.soft_delete(session, instance)
        else:
            self.repository.delete(session, instance)

    def restore(self, session: Session, instance: ModelType) -> None:
        if isinstance(self.repository, SoftDeleteBaseRepository):
            self.repository.restore(session, instance)
        else:
            raise AttributeError(
                f"Restore is not supported for {type(instance).__name__}"
            )
