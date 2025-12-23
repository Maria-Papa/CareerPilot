# CareerPilot – Architecture Overview

## 1. Architectural Goals

CareerPilot is designed as a **local-first, backend-driven application** that prioritizes:

- Clear domain boundaries
- Explicit data ownership
- Ease of reasoning and debugging
- Long-term maintainability
- Future migration to SaaS without rewrites

## 2. High-Level Architecture

CareerPilot follows an **API-first, layered architecture** implemented as a **modular monolith**.

The system is organized around **domain boundaries**, not technical shortcuts, allowing business logic to remain explicit, testable, and evolvable over time.

At a high level, the flow is:

```text
Client (Web / CLI / Future Integrations)
            |
            v
---------------------------------------
| FastAPI Application                 |
| ----------------------------------- |
| Routes (HTTP layer)                 |
| - auth                              |
| - users                             |
| - jobs                              |
| - companies                         |
| - analytics                         |
| ----------------------------------- |
| Services (Business Logic)           |
| - JobService                        |
| - CompanyService                    |
| - FileService                       |
| - AnalyticsService                  |
| ----------------------------------- |
| Repositories (Persistence)          |
| - JobRepository                     |
| - CompanyRepository                 |
| ----------------------------------- |
| Domain Models                       |
| - Job                               |
| - Company                           |
| - Interview                         |
| - JobEvent                          |
| ----------------------------------- |
| Database                            |
| SQLite → PostgreSQL                 |
---------------------------------------
```

### Architectural Characteristics

- **API-first:** The public REST API is the primary contract and drives design decisions (see: [Public API Contract (v1)](public_api_contract.md), [CareerPilot Public API](openapi.v1.yml))
- **Layered:** Each layer has a single, well-defined responsibility
- **Domain-oriented:** Business concepts (jobs, companies, timelines) shape the codebase
- **User-scoped by design:** All data access is explicitly tied to a user
- **Framework-light core:** Business logic is not coupled to FastAPI internals
- **Async-first:** Built on FastAPI and SQLAlchemy 2.0 async APIs

### Why a Modular Monolith

CareerPilot intentionally avoids microservices at this stage.

Instead, it uses:

- Internal modularization
- Explicit service boundaries
- Clean separation of concerns

This approach provides:

- Faster iteration
- Easier debugging
- Strong architectural clarity
- A clean path to future service extraction if scale justifies it

This decision is documented in [ADR-001: Modular Monolith Architecture](adr/ADR-001-architecture.md).

## 3. Request Lifecycle (Example)

1. Request enters a FastAPI route
2. Authentication and user context are resolved
3. Route validates input and delegates to a service
4. Service:
   - Enforces user ownership
   - Applies business rules
   - Coordinates repositories
5. Repository performs database operations
6. Domain models are returned
7. Service prepares the response
8. Route returns a schema-defined response

This flow ensures strict separation between HTTP, business logic, and persistence.

## 4. Backend Structure

```text
app/
├── routes/        # HTTP layer only
├── services/      # Business rules
├── repositories/  # Database access only
├── models/        # SQLAlchemy ORM models
├── schemas/       # Pydantic input/output models
├── enums/         # Domain enums
```

### Key Rules

- Routes never access the database directly
- Services enforce user scoping and domain rules
- Repositories contain no bussiness logic
- Models represent persistence only

## 5. Data Modeling Principles

- Integer primary keys (SQLite-first, PostgreSQL-ready)
- Explicit foreign keys with indexes
- Soft deletes via `deleted_at`
- Timeline-based job history (append-only records)
- Versioned file attachments
- Enum-backed state machines for status transitions

Key modeling decisions are documented in:

- [ADR-002: Enum Strategy and Database Representation](adr/ADR-002-enum-strategy.md)
- [ADR-003: Timeline-Based Modeling vs Mutable State](adr/ADR-003-timeline-modeling.md)

## 6. Authentication & Security

- OAuth2 Password Flow with JWT
- Short-lived access tokens
- Refresh tokens stored in httpOnly secure cookies
- Password hashing with bcrypt
- User flags enforced (`is_active`, `is_verified`)

## 7. API Design

- REST-based, pragmatic
- Explicit versioning (`/api/v1`)
- User-scoped by default
- Explicit resource ownership
- Stable enums and backward-compatible contracts

API evolution rules are defined in [API Evolution & Deprecation Rules](api_evolution.md)

## 8. Migration Strategy

- SQLite for MVP and local-first usage
- PostgreSQL-compatible schema
- Alembic-ready models
- Enum strategy compatible with PostgreSQL ENUMs if needed

## 9. Non-Goals (By Design)

- No GraphQL (unnecessary complexity for the domain)
- No CQRS or event sourcing
- No premature microservices
- No multi-tenant SaaS logic in MVP

## 10. Architectural Highlights

This architecture emphasizes:

- Clean separation of concerns
- Explicit domain modeling
- Predictable request and data flow
- Thoughtful evolution strategy
- Clear documentation of trade-offs via ADRs

## 11. Portfolio Value

This architecture demonstrates:

- Maintainable, scalable backend design
- Well-defined domain boundaries
- Clear reasoning supported by documentation
- Explicit principles guiding future refactoring and growth
