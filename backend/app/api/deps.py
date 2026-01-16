from typing import Callable, TypeVar

from app.core.error_handlers import EntityNotFoundError
from app.db.session import get_session
from app.models.user import User
from app.repositories.user import UserRepository
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    try:
        payload = decode_jwt(token)
        user_id_raw = payload.get("sub")

        if user_id_raw is None:
            raise ValueError("Missing sub claim")

        if not isinstance(user_id_raw, (int, str)):
            raise ValueError("Invalid sub claim")

        user_id = int(user_id_raw)

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )

    user = UserRepository().get(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


def decode_jwt(token: str) -> dict:
    raise NotImplementedError("JWT decoding not implemented yet")
