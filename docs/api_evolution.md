# CareerPilot – API Evolution & Deprecation Rules

This document defines how the CareerPilot API evolves without breaking consumers.

> ADR references:
>
> - Enum stability: [ADR-002](adr/ADR-002-enum-strategy.md)
> - Timeline-based modeling: [ADR-003](adr/ADR-003-timeline-modeling.md)
> - Domain error mapping: [ADR-006](adr/ADR-006-domain-errors.md)

## 1. Versioning Strategy

- API versions are **explicit in the URL**
  - `/api/v1`
  - `/api/v2`
- Breaking changes require a new version
- Old versions remain supported for a defined period

## 2. What Is a Breaking Change

Breaking changes include:

- Removing fields
- Changing field meaning
- Changing enum values (see: [ADR-002](adr/ADR-002-enum-strategy.md))
- Changing authentication behavior
- Changing response structure
- Removing endpoints that violate timeline rules (see: [ADR-003](adr/ADR-003-timeline-modeling.md))
- Modifying error codes without mapping (see: [ADR-006](adr/ADR-006-domain-errors.md))

## 3. Non-Breaking Changes

Allowed without version bump:

- Adding optional fields
- Adding new endpoints
- Adding enum values (append-only) (see: [ADR-002](adr/ADR-002-enum-strategy.md))
- Performance improvements
- Timeline events (see: [ADR-003](adr/ADR-003-timeline-modeling.md))
- Error details updates without breaking contracts (see: [ADR-006](adr/ADR-006-domain-errors.md))

## 4. Enum Stability Rules

- Enum values are **never reordered** (see: [ADR-002](adr/ADR-002-enum-strategy.md))
- Numeric enum values are immutable
- New enum values are appended only
- Deprecated enum values remain accepted

## 5. Field Deprecation

When a field is deprecated:

1. Marked in documentation
2. Kept in responses
3. Ignored on input (optional)
4. Removed only in next major version

## 6. Endpoint Deprecation

- Deprecated endpoints return headers:
  - `Deprecation: true`
  - `Sunset: <date>`
- Deprecation period is documented
- Removal only happens in next major version
- Ensure timeline modeling and history (see: [ADR-003](adr/ADR-003-timeline-modeling.md)) remains intact

## 7. Client Responsibilities

Clients should:

- Treat unknown fields as optional
- Avoid strict enum matching
- Rely on documented contracts
- Pin API version explicitly

## 8. Philosophy

API evolution prioritizes:

- Stability over novelty
- Explicit changes over silent breaks
- Long-term maintainability
- Trust with consumers
