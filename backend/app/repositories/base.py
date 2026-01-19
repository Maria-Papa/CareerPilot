from typing import Generic, Sequence, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.sql import Select
from sqlalchemy.sql.elements import BinaryExpression

from app.db.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def _base_query(self) -> Select:
        return select(self.model)  # type: ignore[arg-type]

    def get(self, session: Session, id: int) -> ModelType | None:
        try:
            stmt = self._base_query().where(self.model.id == id)
            return session.execute(stmt).scalar_one_or_none()
        except SQLAlchemyError:
            session.rollback()
            raise

    def get_all(self, session: Session, *, offset: int = 0, limit: int = 100) -> Sequence[ModelType]:
        try:
            stmt = self._base_query().offset(offset).limit(limit)
            return session.execute(stmt).scalars().all()
        except SQLAlchemyError:
            session.rollback()
            raise

    def find(self, session: Session, **filters) -> Sequence[ModelType]:
        try:
            conditions: list[BinaryExpression] = []
            for key, value in filters.items():
                conditions.append(getattr(self.model, key) == value)
            stmt = self._base_query().where(*conditions) if conditions else self._base_query()
            return session.execute(stmt).scalars().all()
        except SQLAlchemyError:
            session.rollback()
            raise

    def find_one(self, session: Session, **filters) -> ModelType | None:
        try:
            conditions: list[BinaryExpression] = []
            for key, value in filters.items():
                conditions.append(getattr(self.model, key) == value)
            stmt = self._base_query().where(*conditions) if conditions else self._base_query()
            return session.execute(stmt).scalar_one_or_none()
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
            for key, value in values.items():
                setattr(instance, key, value)
            session.commit()
            session.refresh(instance)
            return instance
        except SQLAlchemyError:
            session.rollback()
            raise

    def delete(self, session: Session, instance: ModelType) -> None:
        try:
            session.delete(instance)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
