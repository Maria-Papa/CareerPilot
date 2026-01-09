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

Additionally:

- Certain models (`user`, `job`, `company`, `file`, `job_file_attachment`) require **soft-delete support**, where records are logically deleted but retained in the database.
- All datetime fields stored in the database should be **timezone-aware (UTC)** to prevent bugs and ensure consistent comparisons.

## Scope

This decision defines how database access is structured and constrained within the CareerPilot backend.

It applies to:

- All SQLAlchemy ORM interactions
- All service-to-database communication
- All future persistence-related extensions
- Soft-delete handling for applicable models
- Timezone-aware datetime handling for all timestamp fields

## Decision

Adopt a **Repository Pattern** as the sole interface to persistence.

### Rules

- Routes **never** access the database directly
- Services **never** issue SQLAlchemy queries
- Repositories:
  - Perform CRUD operations
  - Apply **soft-delete filters** automatically for models with `SoftDeleteMixin`
  - Use **timezone-aware UTC datetimes** for all timestamp operations (e.g., `deleted_at`)
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
- Implement `soft_delete` and `restore` operations for models with soft-delete support
- Use `datetime.now(timezone.utc)` for all datetime modifications

Repositories must **not**:

- Contain business rules
- Raise HTTP exceptions
- Perform cross-aggregate orchestration

## Consequences

### Positive

- Clear ownership of responsibilities
- Easier unit testing (repository mocking)
- Consistent data access patterns
- Soft-deleted records are automatically excluded from queries
- Timestamps are consistent, timezone-aware, and UTC-based
- Reduced architectural entropy

### Trade-offs

- Slight increase in boilerplate
- Requires discipline to avoid shortcuts
- Developers must select the correct repository (base vs soft-delete) for models
- Minor static type checking warnings may require `# type: ignore[attr-defined]` in soft-delete repositories

## Related Documents

- [`architecture.md`](../architecture.md)
- [`ADR-001-architecture.md`](ADR-001-architecture.md)
- [`ADR-004-sync-vs-async-persistence.md`](ADR-004-sync-vs-async-persistence.md)

This decision ensures that persistence concerns remain isolated, explicit, evolvable, and safe, including soft-delete and timezone-aware handling.
