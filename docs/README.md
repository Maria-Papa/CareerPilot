# CareerPilot Documentation

This folder contains all documentation for CareerPilot, including architecture, API contracts, coding style, and architectural decisions.

## Entry Points

- [`architecture.md`](architecture.md)
  High-level system architecture, layering, and design principles.

- [`adr/`](adr/)
  Architectural Decision Records documenting significant design choices:
  - [`ADR-001-architecture`](adr/ADR-001-architecture.md) – Overall Architecture
  - [`ADR-002-enum-strategy`](adr/ADR-002-enum-strategy.md) – Enum Strategy
  - [`ADR-003-timeline-modeling`](adr/ADR-003-timeline-modeling.md) – Timeline-Based Modeling

- [`public_api_contract.md`](public_api_contract.md)
  Human-readable API guarantees and stability rules.

- [`openapi.v1.yml`](openapi.v1.yml)
  Machine-readable API specification.

- [`api_evolution.md`](api_evolution.md)
  Rules and philosophy for evolving the API without breaking consumers.

- [`style/app_style_manifest.yml`](style/app_style_manifest.yml)
  Non-code conventions (naming, structure, style rules).

## Documentation Philosophy

- Architecture is text-first and explicit
- Decisions are recorded once and referenced everywhere
- Documentation evolves alongside the codebase
- No diagrams without stable boundaries

This documentation is intended to support:

- Long-term maintainability
- Clear onboarding
- Portfolio presentation
- Future SaaS evolution
