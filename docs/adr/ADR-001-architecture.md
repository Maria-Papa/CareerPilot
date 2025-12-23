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

The expected scale and complexity do not justify distributed systems or operational overhead at this stage.

## Scope

This Architectural Decision Record documents the rationale behind the
overall system architecture of CareerPilot.

It should be read in conjunction with the high-level architecture overview:

- [`docs/architecture.md`](../architecture.md#2-high-level-architecture)

This ADR establishes the foundational architectural direction that all
subsequent decisions (data modeling, API design, enum strategy, timelines)
build upon.

## Decision

Adopt an **API-first, layered modular monolith architecture** implemented with FastAPI and SQLAlchemy.

The architecture consists of:

- Routes for HTTP handling and validation
- Services for business logic and orchestration
- Repositories for persistence concerns
- Domain models for data representation

## Alternatives Considered

### Microservices

Rejected due to:

- Premature operational complexity
- Distributed debugging overhead
- No clear scaling bottleneck requiring service separation

### GraphQL

Rejected due to:

- Over-fetching and under-fetching risks
- Increased schema and tooling complexity
- REST being sufficient and clearer for the domain

### CQRS / Event Sourcing

Rejected due to:

- Increased conceptual overhead
- Unnecessary complexity for current requirements
- Timeline-based modeling provides sufficient auditability

## Consequences

### Positive

- Faster development and iteration
- Clear separation of concerns
- Strong domain clarity
- Easier testing and debugging
- Clean migration path to microservices if ever needed

### Trade-offs

- Single deployable unit
- Requires discipline to maintain boundaries
- Scaling is vertical-first rather than horizontal

## Notes

This decision is intentionally conservative and optimized for correctness,
maintainability, and clarity over premature scalability.

## Related Documents

- [`architecture.md`](../architecture.md)
- [`ADR-002-enum-strategy.md`](ADR-002-enum-strategy.md)
- [`ADR-003-timeline-modeling.md`](ADR-003-timeline-modeling.md)

This ADR defines the baseline against which future architectural changes
and refactors should be evaluated.
