class DomainError(Exception):
    """Base class for all domain-level errors."""

    pass


class EntityNotFoundError(DomainError):
    """Raised when a requested entity does not exist."""

    pass


class InvalidStateTransitionError(DomainError):
    """Raised when a domain entity cannot transition to a requested state."""

    pass


class ConflictError(DomainError):
    """Raised when a domain conflict occurs (e.g. duplicates)."""

    pass


class AccessDeniedError(DomainError):
    """Raised when a user is not allowed to perform an action."""

    pass


class ValidationError(DomainError):
    """Domain-level validation error (distinct from Pydantic/HTTP 422)."""

    pass
