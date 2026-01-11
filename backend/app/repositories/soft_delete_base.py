from datetime import datetime, timezone
from typing import Sequence, Type, TypeVar

from app.db.base import BaseModel
from app.models.mixins import SoftDeleteMixin
from app.repositories.base import BaseRepository
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

SoftDeleteModelType = TypeVar("SoftDeleteModelType", bound=BaseModel)


class SoftDeleteBaseRepository(BaseRepository[SoftDeleteModelType]):
    def __init__(self, model: Type[SoftDeleteModelType]):
        if not issubclass(model, SoftDeleteMixin):
            raise TypeError(f"{model.__name__} must inherit from SoftDeleteMixin")
        super().__init__(model)

    def _base_query(self):
        return select(self.model).where(self.model.deleted_at.is_(None))  # type: ignore[attr-defined]

    def get_including_deleted(
        self, session: Session, id: int
    ) -> SoftDeleteModelType | None:
        try:
            stmt = select(self.model).where(self.model.id == id)
            return session.execute(stmt).scalars().first()
        except SQLAlchemyError:
            session.rollback()
            raise

    def get(self, session: Session, id: int) -> SoftDeleteModelType | None:
        try:
            stmt = self._base_query().where(self.model.id == id)
            return session.execute(stmt).scalar_one_or_none()
        except SQLAlchemyError:
            session.rollback()
            raise

    def get_all(
        self, session: Session, *, offset: int = 0, limit: int = 100
    ) -> Sequence[SoftDeleteModelType]:
        try:
            stmt = self._base_query().offset(offset).limit(limit)
            return session.execute(stmt).scalars().all()
        except SQLAlchemyError:
            session.rollback()
            raise

    def soft_delete(self, session: Session, instance: SoftDeleteModelType) -> None:
        try:
            instance.deleted_at = datetime.now(timezone.utc)  # type: ignore[attr-defined]
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise

    def restore(self, session: Session, instance: SoftDeleteModelType) -> None:
        try:
            instance.deleted_at = None  # type: ignore[attr-defined]
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
