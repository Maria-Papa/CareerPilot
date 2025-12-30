# ADR-004: Synchronous Persistence with SQLAlchemy

## Status

Accepted

## Context

CareerPilot uses FastAPI as its web framework and SQLAlchemy as its ORM.

FastAPI supports both synchronous and asynchronous request handling, and SQLAlchemy provides both sync and async APIs.

An explicit decision is required to avoid architectural drift and mixed patterns.

## Decision

CareerPilot uses **synchronous SQLAlchemy sessions** for all database access.

Async database drivers and async ORM APIs are intentionally deferred.

## Rationale

Synchronous persistence is chosen to:

- Maintain SQLite compatibility for local-first usage
- Reduce architectural and cognitive complexity
- Avoid premature optimization
- Simplify testing and debugging
- Keep business logic independent of async constraints

Given current scale expectations, async persistence would not provide meaningful performance benefits.

## Alternatives Considered

### Async SQLAlchemy + asyncpg

Rejected due to:

- Increased complexity
- Reduced SQLite support
- Higher migration and testing overhead
- No current throughput justification

## Consequences

### Positive

- Simpler code and mental model
- Easier onboarding and maintenance
- Clear migration path if async is needed later

### Trade-offs

- Lower theoretical concurrency ceiling
- Requires future refactor if async persistence becomes necessary

## Notes

This decision can be revisited if CareerPilot transitions to:

- PostgreSQL-only deployments
- High-concurrency SaaS workloads
- Background worker-heavy architectures

## Related Documents

- [`architecture.md`](../architecture.md)
- [`ADR-001-architecture.md`](ADR-001-architecture.md)

This decision establishes the baseline persistence strategy for CareerPilot, ensuring synchronous, consistent data access that supports repositories, services, and domain rules.
