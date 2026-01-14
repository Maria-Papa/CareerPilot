# backend/app/api/deps.py
from typing import Callable, TypeVar

from app.core import EntityNotFoundError
from app.db import get_session
from fastapi import Depends
from sqlalchemy.orm import Session

T = TypeVar("T")


def get_entity_or_404(
    getter: Callable[[Session, int], T | None],
) -> Callable[[int, Session], T]:
    def dependency(company_id: int, session: Session = Depends(get_session)) -> T:
        entity = getter(session, company_id)
        if entity is None:
            raise EntityNotFoundError()
        return entity

    return dependency
