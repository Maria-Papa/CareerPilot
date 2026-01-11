class DomainError(Exception):
    pass


class EntityNotFoundError(DomainError):
    pass


class InvalidStateTransitionError(DomainError):
    pass


class ConflictError(DomainError):
    pass


class AccessDeniedError(DomainError):
    pass


class ValidationError(DomainError):
    pass
