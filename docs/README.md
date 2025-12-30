# CareerPilot Documentation

This folder contains all documentation for CareerPilot, including architecture, API contracts, coding style, and architectural decisions.

## Entry Points

### Architecture

- [`architecture.md`](architecture.md) – High-level system architecture, layering, and design principles.
- [`adr/`](adr/) – Architectural Decision Records documenting significant design choices:
  - [`ADR-001-architecture`](adr/ADR-001-architecture.md) – Overall architecture, layered modular monolith.
  - [`ADR-002-enum-strategy`](adr/ADR-002-enum-strategy.md) – Enum strategy (affects API enum stability and evolution).
  - [`ADR-003-timeline-modeling`](adr/ADR-003-timeline-modeling.md) – Timeline-based modeling (affects job state/history and auditability).
  - [`ADR-004-sync-vs-async-persistence`](adr/ADR-004-sync-vs-async-persistence.md) – Persistence strategy (synchronous SQLAlchemy sessions).
  - [`ADR-005-repository-pattern`](adr/ADR-005-repository-pattern.md) – Repository pattern enforcing data access boundaries.
  - [`ADR-006-domain-errors`](adr/ADR-006-domain-errors.md) – Domain errors and exception mapping (consistent error handling).

### Public API

- [`public_api_contract.md`](public_api_contract.md) – Human-readable API guarantees and stability rules.
  - Endpoints reflect **timeline-based modeling** (see: [ADR-003](adr/ADR-003-timeline-modeling.md)).
  - Enum stability and append-only rules (see: [ADR-002](adr/ADR-002-enum-strategy.md)).
  - Domain error handling and HTTP mapping (see: [ADR-006](adr/ADR-006-domain-errors.md)).
  - Repository constraints and user-scoped access (see: [ADR-005](adr/ADR-005-repository-pattern.md)).

- [`openapi.v1.yml`](openapi.v1.yml) – Machine-readable OpenAPI specification.

- [`api_evolution.md`](api_evolution.md) – Rules and philosophy for evolving the API without breaking consumers.
  - Defines breaking vs non-breaking changes.
  - Ensures enum stability (see: [ADR-002](adr/ADR-002-enum-strategy.md)).
  - Preserves timeline-based modeling (see: [ADR-003](adr/ADR-003-timeline-modeling.md)).
  - Honors domain errors and HTTP mapping (see: [ADR-006](adr/ADR-006-domain-errors.md)).

### Style & Conventions

- [`style/app_style_manifest.yml`](style/app_style_manifest.yml) – Coding, commit, and documentation conventions.
  - Commit messages referencing ADRs should include the ADR number:
    - Example: `docs(adr-005): clarify repository responsibilities`
  - Ensures consistent developer practices across features, services, and persistence layers.

## ADR ↔ API Mapping

| ADR | Name | Key Impact | Affected Endpoints / Features |
|-----|------|------------|-------------------------------|
| ADR-001 | Modular Monolith Architecture | Layered modular monolith, separation of concerns | All endpoints and services |
| ADR-002 | Enum Strategy | Stable enums, append-only, type-safe | `/jobs`, `/interviews`, `/files`, `/analytics/*` |
| ADR-003 | Timeline-Based Modeling | Append-only records, audit trail | `/jobs/{job_id}/status-history`, `/jobs/{job_id}/timeline`, `/jobs/{job_id}/interviews`, `/analytics/*` |
| ADR-004 | Synchronous Persistence | Sync SQLAlchemy sessions | All CRUD repository interactions |
| ADR-005 | Repository Pattern | Enforces DB boundaries, soft-deletes, user-scoped | `/jobs`, `/companies`, `/locations`, `/tags`, `/files` |
| ADR-006 | Domain Errors & Exception Mapping | Domain errors propagate through services, HTTP mapping at route | All endpoints; consistent error handling |

## Documentation Philosophy

- Architecture is **text-first and explicit**.
- ADRs are the **single source of truth** for all architectural decisions.
- API, style guide, and evolution rules reference ADRs wherever applicable.
- Documentation evolves **alongside the codebase**.
- No diagrams without **stable, enforceable boundaries**.

This documentation supports:

- Long-term maintainability.
- Clear onboarding for developers and reviewers.
- Portfolio-ready presentation of architectural clarity.
- Smooth future evolution to SaaS.

## Cross-Linking Principles

- **ADRs** → definitive source for design decisions.
- **API Contract** → references ADRs for enums, timelines, repositories, and domain error handling.
- **API Evolution** → respects ADR constraints to avoid breaking changes.
- **Style Guide** → enforces commit discipline and code consistency in alignment with ADRs.
- **Consistency** → ensured by linking all documentation items where decisions apply.
