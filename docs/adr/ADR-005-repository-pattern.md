# ADR-005: Repository Pattern and Data Access Boundaries

## Status

Accepted

## Context

CareerPilot requires clear separation between:

- HTTP concerns
- Business logic
- Persistence implementation details

As the system grows, direct database access from services or routes would:

- Increase coupling
- Complicate testing
- Blur responsibility boundaries
- Make future refactors riskier

A consistent data access abstraction is required.

## Scope

This decision defines how database access is structured and constrained within the CareerPilot backend.

It applies to:

- All SQLAlchemy ORM interactions
- All service-to-database communication
- All future persistence-related extensions

## Decision

Adopt a **Repository Pattern** as the sole interface to persistence.

### Rules

- Routes **never** access the database directly
- Services **never** issue SQLAlchemy queries
- Repositories:
  - Perform CRUD operations
  - Apply soft-delete filters
  - Enforce user-scoped access constraints
  - Return ORM models, not schemas
- Services:
  - Orchestrate repositories
  - Apply business rules
  - Control transactions when needed

### Repository Responsibilities

Repositories may:

- Filter by ownership (`user_id`)
- Apply default ordering
- Implement pagination
- Hide SQLAlchemy-specific details

Repositories must **not**:

- Contain business rules
- Raise HTTP exceptions
- Perform cross-aggregate orchestration

## Consequences

### Positive

- Clear ownership of responsibilities
- Easier unit testing (repository mocking)
- Consistent data access patterns
- Reduced architectural entropy

### Trade-offs

- Slight increase in boilerplate
- Requires discipline to avoid shortcuts

## Related Documents

- [`architecture.md`](../architecture.md)
- [`ADR-001-architecture.md`](ADR-001-architecture.md)
- [`ADR-004-sync-vs-async-persistence.md`](ADR-004-sync-vs-async-persistence.md)

This decision ensures that persistence concerns remain isolated, explicit, and evolvable as the system grows.
