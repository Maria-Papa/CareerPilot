from app.core import (
    AccessDeniedError,
    ConflictError,
    EntityNotFoundError,
    InvalidStateTransitionError,
)
from fastapi import HTTPException, status


def raise_http_error(exc: Exception) -> None:
    if isinstance(exc, EntityNotFoundError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

    if isinstance(exc, AccessDeniedError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))

    if isinstance(exc, ConflictError):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))

    if isinstance(exc, InvalidStateTransitionError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    # Fallback for unexpected domain errors
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error"
    )
