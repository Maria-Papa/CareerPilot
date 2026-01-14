from app.core.errors import (
    AccessDeniedError,
    ConflictError,
    DomainError,
    EntityNotFoundError,
    ValidationError,
)
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)


def _error_detail(exc: Exception) -> str:
    """
    Helper to produce a human-readable message for the response.
    Falls back to the class name if no message is provided.
    """
    msg = str(exc)
    return msg or exc.__class__.__name__


def register_error_handlers(app: FastAPI) -> None:
    """
    Register all domain -> HTTP exception mappings on the given FastAPI app.
    """

    @app.exception_handler(EntityNotFoundError)
    async def entity_not_found_handler(request: Request, exc: EntityNotFoundError):
        # Map domain "not found" to HTTP 404
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content={"detail": _error_detail(exc)},
        )

    @app.exception_handler(ConflictError)
    async def conflict_error_handler(request: Request, exc: ConflictError):
        # E.g. duplicate name, unique constraint, etc.
        return JSONResponse(
            status_code=HTTP_409_CONFLICT,
            content={"detail": _error_detail(exc)},
        )

    @app.exception_handler(AccessDeniedError)
    async def access_denied_handler(request: Request, exc: AccessDeniedError):
        # Use 403 when user is authenticated but not allowed
        return JSONResponse(
            status_code=HTTP_403_FORBIDDEN,
            content={"detail": _error_detail(exc)},
        )

    @app.exception_handler(ValidationError)
    async def domain_validation_handler(request: Request, exc: ValidationError):
        # IMPORTANT: This is for *domain* validation, not Pydantic/422.
        # E.g. invalid state transition, business rules, etc.
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={"detail": _error_detail(exc)},
        )

    # Optional: base DomainError fallback (anything not caught above)
    @app.exception_handler(DomainError)
    async def domain_error_handler(request: Request, exc: DomainError):
        # If a DomainError slips through without a specific mapping,
        # treat it as a 400 by default.
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={"detail": _error_detail(exc)},
        )

    # NOTE: we intentionally do NOT add a global Exception handler here.
    # Unhandled exceptions should surface as 500s and fail loudly in tests.
