from typing import Callable, TypeVar

from app.core import EntityNotFoundError
from app.db import get_session
from fastapi import Depends, Request
from sqlalchemy.orm import Session

T = TypeVar("T")


def get_entity_or_404(getter: Callable[[Session, int], T | None]) -> Callable[..., T]:
    def dependency(request: Request, session: Session = Depends(get_session)) -> T:
        path_params = request.path_params
        if not path_params:
            raise EntityNotFoundError("Missing identifier in path")

        id_value = next(iter(path_params.values()))
        try:
            id_int = int(id_value)
        except (TypeError, ValueError):
            raise EntityNotFoundError("Invalid identifier")

        entity = getter(session, id_int)
        if entity is None:
            raise EntityNotFoundError()
        return entity

    return dependency
