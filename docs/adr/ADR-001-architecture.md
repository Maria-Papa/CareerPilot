# ADR-001: Modular Monolith Architecture

## Status

Accepted

## Context

CareerPilot is a personal, local-first job application tracking system with the potential to evolve into a SaaS product.

The system requires:

- Clear domain modeling
- Strong consistency guarantees
- Explicit user-scoped data ownership
- Ease of reasoning and debugging
- Interview-grade architectural clarity
- A low operational burden during early development

The expected scale and complexity do not justify distributed systems, asynchronous persistence layers, or operational overhead at this stage.

## Scope

This Architectural Decision Record documents the rationale behind the overall system architecture of CareerPilot.

It should be read in conjunction with the high-level architecture overview:

- [`docs/architecture.md`](../architecture.md#2-high-level-architecture)

This ADR establishes the foundational architectural direction that all subsequent decisions (data modeling, API design, enum strategy, timelines, repository patterns) build upon.

## Decision

Adopt an **API-first, layered modular monolith architecture** implemented with FastAPI and SQLAlchemy.

The system is structured around a clear separation of responsibilities:

- **Routes** handle HTTP concerns and request/response validation
- **Services** encapsulate business logic, orchestration, and domain rules
- **Repositories** provide a strict boundary for persistence and query logic
- **Domain Models** represent the core data structures via SQLAlchemy ORM

Persistence is implemented using **synchronous SQLAlchemy sessions** within a single deployable application unit. This choice prioritizes correctness, simplicity, and SQLite compatibility during early development, and is formally documented in [ADR-004](ADR-004-sync-vs-async-persistence.md).

All database access is explicitly mediated through repositories, ensuring that query logic and persistence concerns remain isolated from business rules, as defined in [ADR-005](adr/ADR-005-repository-pattern.md).

Business logic operates independently of HTTP concerns and signals failure through domain-level errors, which are translated into API responses only at the route layer. This error-handling strategy is defined in [ADR-006](adr/ADR-006-domain-errors.md).

## Rationale

This architecture was chosen to optimize for:

- Correctness and data integrity
- Clear ownership of responsibilities
- Simple debugging and testing
- Minimal accidental complexity
- A clean, well-documented evolution path

Synchronous persistence is intentionally selected to:

- Avoid premature async complexity
- Maintain SQLite compatibility
- Reduce cognitive load during domain modeling
- Keep business logic framework-agnostic

## Alternatives Considered

### Microservices

Rejected due to:

- Premature operational complexity
- Distributed debugging overhead
- No clear scaling bottleneck requiring service separation

### Async-First Persistence (async SQLAlchemy / asyncpg)

Rejected due to:

- Increased complexity without current throughput needs
- Reduced SQLite compatibility
- Higher testing and migration overhead

### GraphQL

Rejected due to:

- Increased schema and tooling complexity
- REST being sufficient and clearer for the domain

### CQRS / Event Sourcing

Rejected due to:

- Increased conceptual overhead
- Timeline-based modeling providing sufficient auditability

## Consequences

### Positive

- Faster development and iteration
- Clear separation of concerns
- Strong domain clarity
- Easier testing and debugging
- Clean migration path to async or microservices if needed

### Trade-offs

- Single deployable unit
- Vertical-first scaling
- Requires discipline to maintain boundaries

## Notes

This decision is intentionally conservative and optimized for correctness, maintainability, and clarity over premature scalability.

## Related Documents

- [`architecture.md`](../architecture.md)
- [`ADR-002-enum-strategy.md`](ADR-002-enum-strategy.md)
- [`ADR-003-timeline-modeling.md`](ADR-003-timeline-modeling.md)
- [`ADR-004-sync-vs-async-persistence.md`](ADR-004-sync-vs-async-persistence.md)
- [`ADR-005-repository-pattern.md`](ADR-005-repository-pattern.md)
- [`ADR-006-domain-errors.md`](ADR-006-domain-errors.md)

This ADR defines the baseline against which future architectural changes and refactors should be evaluated.
