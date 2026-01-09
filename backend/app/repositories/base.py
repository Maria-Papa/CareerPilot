from datetime import datetime
from typing import Generic, Sequence, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.base import BaseModel
from app.models.mixins import SoftDeleteMixin

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """
    Generic synchronous repository.
    Provides basic CRUD with optional soft-delete support.
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, session: Session, id: int) -> ModelType | None:
        try:
            stmt = select(self.model).where(self.model.id == id)
            # Only apply soft-delete filter if model has deleted_at
            if issubclass(self.model, SoftDeleteMixin):
                stmt = stmt.where(self.model.deleted_at.is_(None))
            return session.execute(stmt).scalar_one_or_none()
        except SQLAlchemyError:
            session.rollback()
            raise

    def list(
        self, session: Session, skip: int = 0, limit: int = 100
    ) -> Sequence[ModelType]:
        try:
            stmt = select(self.model).offset(skip).limit(limit)
            if issubclass(self.model, SoftDeleteMixin):
                stmt = stmt.where(self.model.deleted_at.is_(None))
            return session.execute(stmt).scalars().all()
        except SQLAlchemyError:
            session.rollback()
            raise

    def add(self, session: Session, instance: ModelType) -> ModelType:
        try:
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance
        except SQLAlchemyError:
            session.rollback()
            raise

    def update(self, session: Session, instance: ModelType, values: dict) -> ModelType:
        try:
            for k, v in values.items():
                setattr(instance, k, v)
            session.commit()
            session.refresh(instance)
            return instance
        except SQLAlchemyError:
            session.rollback()
            raise

    def soft_delete(self, session: Session, instance: ModelType) -> None:
        """
        Performs soft-delete if model has deleted_at; otherwise raises.
        """
        if not isinstance(instance, SoftDeleteMixin):
            raise TypeError(f"{self.model.__name__} does not support soft-delete")
        try:
            instance.deleted_at = datetime.utcnow()
            session.add(instance)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
