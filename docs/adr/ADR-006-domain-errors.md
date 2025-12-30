# ADR-006: Domain Errors and Exception Mapping

## Status

Accepted

## Context

CareerPilot requires consistent error handling across:

- Routes
- Services
- Repositories

Allowing HTTP exceptions or framework-specific errors to leak into business logic would:

- Couple services to FastAPI
- Reduce testability
- Obscure domain intent
- Complicate future transport layers (CLI, background jobs)

A clear error boundary is required.

## Scope

This decision defines how errors are represented, propagated, and translated across architectural layers.

It applies to:

- Services
- Repositories
- API route handlers

## Decision

Adopt a **Domain Error pattern** with explicit exception mapping.

### Rules

- Repositories:
  - Raise domain-level exceptions (e.g. `NotFoundError`)
  - Never raise HTTP exceptions
- Services:
  - Raise domain errors
  - Do not translate errors to HTTP responses
- Routes:
  - Catch domain errors
  - Translate them into HTTP responses

### Example Domain Errors

- `EntityNotFoundError`
- `AccessDeniedError`
- `InvalidStateTransitionError`
- `ConflictError`

### HTTP Mapping Responsibility

Only the HTTP layer (routes):

- Maps domain errors to HTTP status codes
- Defines error response schemas
- Controls error messages exposed to clients

## Consequences

### Positive

- Framework-agnostic business logic
- Consistent error handling
- Easier testing
- Clear separation of concerns

### Trade-offs

- Requires explicit exception classes
- Slightly more code upfront

## Related Documents

- [`architecture.md`](../architecture.md)
- [`ADR-001-architecture.md`](ADR-001-architecture.md)
- [`ADR-005-repository-pattern.md`](ADR-005-repository-pattern.md)

This decision preserves domain purity and keeps infrastructure concerns at the system boundary.
