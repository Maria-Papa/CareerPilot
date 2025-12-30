# ADR-003: Timeline-Based Modeling vs Mutable State

## Status

Accepted

## Context

Job applications in CareerPilot evolve through multiple states (saved → applied → interview → offer → rejected). Key requirements:

- Track state changes over time
- Preserve history for analytics
- Support append-only audit trail
- Avoid accidental data loss

## Scope

This decision documents the choice to model job-related state and history using timeline-based, append-only records rather than mutable state.

It aligns with the architectural principles outlined in:

- [`docs/architecture.md`](../architecture.md#5-data-modeling-principles)

This ADR directly affects:

- Data modeling patterns
- Analytics and historical queries
- Auditability and debugging

## Decision

- Adopt **timeline-based modeling**:
  - `JobStatusHistory` records each status change.
  - `JobEvent` records relevant actions (file attachment, interview scheduled, salary update).
  - `JobFileAttachment` versioning preserves historical attachments.
- No mutable “current state” column without a history record.
- APIs always reflect the latest status but the full timeline is preserved for analytics.

## Consequences

- Full auditability of application state over time.
- Analytics and reporting are simplified.
- Avoids accidental overwrites of historical data.
- Slight increase in storage and query complexity, mitigated by indexes.

## Related Documents

- [`architecture.md`](../architecture.md)
- [`ADR-001-architecture.md`](ADR-001-architecture.md)
- [`ADR-002-enum-strategy.md`](ADR-002-enum-strategy.md)

Timeline-based modeling provides a stable foundation for future features such as analytics, insights, and historical reconstruction.
