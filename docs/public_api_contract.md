# CareerPilot – Public API Contract (v1)

This document defines the **public API contract** for CareerPilot.
It serves as the authoritative reference for frontend integration, future API consumers, and interview discussions.

The contract is **versioned, user-scoped, REST-based**, and designed to remain stable as the application evolves from a local-first tool to a potential SaaS.

ADR references:

- Timeline-based modeling: [ADR-003](adr/ADR-003-timeline-modeling.md)
- Enum strategy: [ADR-002](adr/ADR-002-enum-strategy.md)
- Repository pattern: [ADR-005](adr/ADR-005-repository-pattern.md)
- Domain error mapping: [ADR-006](adr/ADR-006-domain-errors.md)

## 1. General Principles

- Base URL: `/api/v1`
- API style: REST (resource-oriented, pragmatic)
- Authentication: OAuth2 Password Flow with JWT
- All endpoints are **user-scoped** unless explicitly stated
- Soft deletes are respected across all queries (see: [ADR-005](adr/ADR-005-repository-pattern.md))
- Breaking changes require a new API version (see: [Api Evolution](api_evolution.md))

## 2. Authentication

### POST `/auth/register`

Create a new user account.

**Request:**

```json
{
  "email": "user@example.com",
  "password": "string"
}
```

**Response:**

```json
{
  "id": 1,
  "email": "user@example.com",
  "is_verified": false
}
```

### POST `/auth/login`

Authenticate a user and issue tokens.

**Response:**

```json
{
  "access_token": "jwt",
  "token_type": "bearer"
}
```

- Access token: sent in `Authorization: Bearer <token>`
- Refresh token: stored in httpOnly secure cookie

### GET `/auth/me`

Return the authenticated user.

## 3. Users

### GET `/users/me`

Returns the current user's profile.

## 4. Companies

### GET `/companies`

List companies associated with the user.

**Query Parameters:**

- `q` (optional): name search
- `limit`, `offset`

### POST `/companies`

Create a new company.

**Request:**

```json
{
  "name": "OpenAI",
  "website": "https://openai.com",
  "industry": "AI"
}
```

### GET `/companies/{company_id}`

Retrieve company details.

## 5. Locations & Cost of Living

### GET `/locations`

List available locations.

### POST `/locations`

Create a location.

**Request:**

```json
{
  "name": "Dublin",
  "country_code": "IE",
  "currency_id": 1
}
```

### GET `/cost-of-living`

List cost-of-living entries.

**Query Parameters:**

- `location_id`

### POST `/cost-of-living`

Create a cost-of-living record.

**Request:**

```json
{
  "location_id": 1,
  "title": "Family of 4",
  "yearly_cost_cents": 5200000
}
```

## 6. Jobs

### GET `/jobs`

List jobs for the authenticated user.

**Query Parameters:**

- `status` (see: [ADR-002](adr/ADR-002-enum-strategy.md))
- `company_id`
- `tag`
- `limit`, `offset`

### POST `/jobs`

Create a job application.

**Request:**

```json
{
  "company_id": 1,
  "location_id": 2,
  "title": "Senior Backend Engineer",
  "employment_type": "FULL_TIME",
  "flexibility": "REMOTE",
  "job_url": "https://example.com/job",
  "salary_gross_given": 8500000
}
```

> Applies timeline-based modeling (see: [ADR-003](adr/ADR-003-timeline-modeling.md)) for auditability.

### GET `/jobs/{job_id}`

Retrieve full job details.

**Includes:**

- Company
- Location
- Tags
- Interviews
- Active file attachments
- Current status

### PATCH `/jobs/{job_id}`

Update mutable job fields.

### DELETE `/jobs/{job_id}`

Soft-delete a job.

## 7. Job Status History

### POST `/jobs/{job_id}/status`

Change job status.

**Request:**

```json
{
  "status": "INTERVIEW"
}
```

**Side Effects:**

- Inserts a `JobStatusHistory` record (see: [ADR-003](adr/ADR-003-timeline-modeling.md))
- Inserts a `JobEvent`
- Soft-delete rules handled by repository (see: [ADR-005](adr/ADR-005-repository-pattern.md))

### GET `/jobs/{job_id}/status-history`

Retrieve job status timeline (see: [ADR-003](adr/ADR-003-timeline-modeling.md)).

## 8. Tags

### GET `/tags`

List tags.

### POST `/tags`

Create a tag.

**Request:**

```json
{
  "name": "Backend"
}
```

### POST `/jobs/{job_id}/tags`

Attach tags to a job.

**Request:**

```json
{
  "tag_ids": [1, 3]
}
```

## 9. Files

### POST `/files`

Upload a file.

**Request:**

```json
{
  "file_type": "CV",
  "file_url": "s3://bucket/file.pdf"
}
```

### GET `/files`

List user files.

## 10. Job File Attachments (Versioned)

### POST `/jobs/{job_id}/files`

Attach a file to a job.

**Request:**

```json
{
  "file_id": 12
}
```

**Behavior:**

- Automatically increments version (see: [ADR-003](adr/ADR-003-timeline-modeling.md))
- Deactivates previous attachment (see: [ADR-005](adr/ADR-005-repository-pattern.md))
- Creates a JobEvent

### GET `/jobs/{job_id}/files`

Retrieve attachment history (see: [ADR-003](adr/ADR-003-timeline-modeling.md)).

### DELETE `/jobs/{job_id}/files/{attachment_id}`

Detach a file (soft delete) (see: [ADR-005](adr/ADR-005-repository-pattern.md)).

## 11. Interviews

### GET `/jobs/{job_id}/interviews`

List interviews for a job.

### POST `/jobs/{job_id}/interviews`

Schedule an interview.

**Request:**

```json
{
  "interview_type": "TECHNICAL",
  "scheduled_at": "2025-01-15T14:00:00Z",
  "notes": "Pair programming"
}
```

### PATCH `/interviews/{interview_id}`

Update interview outcome.

**Request:**

```json
{
  "outcome": "PASSED"
}
```

> Follows timeline-based modeling (see: [ADR-003](adr/ADR-003-timeline-modeling.md)).

## 12. Job Timeline (Unified Feed)

### GET `/jobs/{job_id}/timeline`

Returns a chronological feed combining:

- JobEvents
- Status changes
- Interviews
- File attachments

**Response:**

```json
[
  {
    "type": "STATUS_CHANGED",
    "timestamp": "...",
    "payload": {
      "from": "APPLIED",
      "to": "INTERVIEW"
    }
  }
]
```

> Timeline feed fully implements append-only modeling (see: [ADR-003](adr/ADR-003-timeline-modeling.md)).

## 13. Analytics

### GET `/analytics/job-pipeline`

Aggregate job counts by status (see: [ADR-003](adr/ADR-003-timeline-modeling.md)).

### GET `/analytics/salary-vs-col`

Compare salaries against cost of living per location (see: [ADR-002](adr/ADR-002-enum-strategy.md), [ADR-003](adr/ADR-003-timeline-modeling.md)).

## 14. Error Handling

All errors follow FastAPI's standard format and domain error mapping (see: [ADR-006](adr/ADR-006-domain-errors.md)):

**Response:**

```json
{
  "detail": "Not authorized"
}
```

Validation errors return structured field-level messages.

## 15. Versioning Rules

- API versions are explicit in the URL
- Breaking changes require a new version
- Enum values are stable and never reordered (see: [ADR-002](adr/ADR-002-enum-strategy.md))
- Fields are deprecated before removal
- Long-term maintainability

> It prioritizes clarity, stability, and explicit workflows over incidental complexity.

## 16. Audience & Intent

This contract is designed for:

- Frontend developers
- Future API consumers
- Interviewers reviewing architecture decisions
- Long-term maintainability

It prioritizes clarity, stability, and explicit workflows over incidental complexity.
