from datetime import datetime, timezone
from typing import Any, Sequence, Type, TypeVar, cast

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.sql import Select

from app.db.base import BaseModel
from app.repositories.base import BaseRepository

SoftDeleteModelType = TypeVar("SoftDeleteModelType", bound=BaseModel)


class SoftDeleteBaseRepository(BaseRepository[SoftDeleteModelType]):
    def __init__(self, model: Type[SoftDeleteModelType]):
        if not issubclass(model, BaseModel):
            raise TypeError(f"{model.__name__} must inherit from BaseModel")

        if not hasattr(model, "deleted_at"):
            raise TypeError(f"{model.__name__} must have a 'deleted_at' attribute")

        super().__init__(model)

    def _base_query(self) -> Select:
        model_any = cast(Any, self.model)
        return cast(Select, select(self.model)).where(model_any.deleted_at.is_(None))

    def get_including_deleted(self, session: Session, id: int) -> SoftDeleteModelType | None:
        try:
            model_any = cast(Any, self.model)
            stmt = cast(Select, select(self.model)).where(model_any.id == id)
            return session.execute(stmt).scalars().first()
        except SQLAlchemyError:
            session.rollback()
            raise

    def get(self, session: Session, id: int) -> SoftDeleteModelType | None:
        try:
            model_any = cast(Any, self.model)
            stmt = self._base_query().where(model_any.id == id)
            return session.execute(stmt).scalar_one_or_none()
        except SQLAlchemyError:
            session.rollback()
            raise

    def get_all(self, session: Session, *, offset: int = 0, limit: int = 100) -> Sequence[SoftDeleteModelType]:
        try:
            stmt = self._base_query().offset(offset).limit(limit)
            return session.execute(stmt).scalars().all()
        except SQLAlchemyError:
            session.rollback()
            raise

    def soft_delete(self, session: Session, instance: SoftDeleteModelType) -> None:
        try:
            inst_any = cast(Any, instance)
            inst_any.deleted_at = datetime.now(timezone.utc)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise

    def restore(self, session: Session, instance: SoftDeleteModelType) -> None:
        try:
            inst_any = cast(Any, instance)
            inst_any.deleted_at = None
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
