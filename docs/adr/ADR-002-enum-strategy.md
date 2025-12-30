# ADR-002: Enum Strategy and Database Representation

## Status

Accepted

## Context

CareerPilot uses multiple domain enums (e.g., JobStatus, InterviewType, FileType) to represent finite sets of values in the system. Enums must:

- Be stable over time
- Allow storage in both SQLite and PostgreSQL
- Support type-safe access in Python code
- Enable versioned migrations without breaking API contracts

## Scope

This decision defines how domain enums are represented, persisted, and exposed across the CareerPilot system.

It supports the architectural goals described in:

- [`docs/architecture.md`](../architecture.md#1-architectural-goals)

Specifically, this ADR impacts:

- Data modeling principles
- API contract stability
- Database migration strategy (SQLite → PostgreSQL)

## Decision

- Use Python `IntEnum` for all domain enums.
- Store enums as `SmallInteger` in the database (SQLite first, PostgreSQL-ready).
- Never reorder enum values once released.
- Optional: In the future, migrate to PostgreSQL ENUM types when SaaS scale justifies.

### Coding Rules

- `Mapped[MyEnum]` in SQLAlchemy models.
- Only quote enums for `Mapped[...]` if needed for forward references.
- Enum names are singular (JobStatus, InterviewType) and members are SCREAMING_SNAKE_CASE.
- Reserve `99` for `OTHER` when appropriate.

## Consequences

- Strong consistency between code and database.
- Future PostgreSQL migration is straightforward.
- Breaking changes require new enum values, never reordering existing ones.

## Related Documents

- [`architecture.md`](../architecture.md)
- [`ADR-001-architecture.md`](ADR-001-architecture.md)
- [`public_api_contract.md`](../public_api_contract.md)

This enum strategy is intended to minimize coupling between the database, application logic, and public API while enabling safe evolution over time.
