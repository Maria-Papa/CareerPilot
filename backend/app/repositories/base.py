from typing import Generic, Sequence, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def _base_query(self):
        return select(self.model)

    def get(self, session: Session, id: int) -> ModelType | None:
        try:
            stmt = self._base_query().where(self.model.id == id)
            return session.execute(stmt).scalar_one_or_none()
        except SQLAlchemyError:
            session.rollback()
            raise

    def get_all(
        self,
        session: Session,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> Sequence[ModelType]:
        try:
            stmt = self._base_query().offset(offset).limit(limit)
            return session.execute(stmt).scalars().all()
        except SQLAlchemyError:
            session.rollback()
            raise

    def find(self, session: Session, **filters) -> Sequence[ModelType]:
        try:
            stmt = self._base_query().filter_by(**filters)
            return session.execute(stmt).scalars().all()
        except SQLAlchemyError:
            session.rollback()
            raise

    def find_one(self, session: Session, **filters) -> ModelType | None:
        try:
            stmt = self._base_query().filter_by(**filters)
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
