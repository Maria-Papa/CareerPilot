# MVP Progress

This section reflects **actual implementation progress**, not future intent.

## Documentation & ADRs

- [x] Architecture overview documented [`docs/architecture.md`](../architecture.md)
- [x] Architectural Decision Records (ADRs) framework established [`docs/adr/`](../adr/)
- [x] Initial ADRs created and committed:
  - ADR-001: Overall architecture
  - ADR-002: Enum strategy
  - ADR-003: Timeline-based domain modeling
- [x] Public API contract defined [`docs/public_api_contract.md`](../public_api_contract.md)
- [x] OpenAPI v1 specification generated [`docs/openapi.v1.yml`](../openapi.v1.yml)
- [x] API evolution & deprecation rules documented [`docs/api_evolution.md`](../api_evolution.md)
- [x] Project README updated to reference ADRs, API contracts, and progress

## Core Foundations

- [x] Repository structure and layering
- [x] Architecture documentation
- [x] ADR process and initial decisions
- [x] API-first design approach
- [x] Docker-based development environment

## Backend (FastAPI)

- [x] Project bootstrap and configuration
- [x] Domain-driven folder structure
- [x] Public API contract definition
- [x] OpenAPI specification (v1)
- [~] Core domain models (some models already implemented)
- [ ] Application services
- [ ] Persistence layer
- [ ] Authentication (planned)

## Frontend (Next.js)

- [x] Next.js 14 project setup
- [x] Tailwind + shadcn/ui integration
- [ ] Application shell and layout
- [ ] Job tracking views
- [ ] Dashboard and charts

## Job Tracking (MVP Scope)

- [ ] Manual job application entry
- [ ] Application status lifecycle
- [ ] Timeline/history per application
- [ ] CV and cover letter storage
- [ ] Basic metadata (salary, location)

## Automation & AI

- [ ] Background task infrastructure
- [ ] Job scraping (config-driven)
- [ ] AI-assisted CV and cover letter generation
- [ ] Email parsing for application updates

This checklist will evolve as features are implemented and refined.
