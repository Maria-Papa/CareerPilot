# 💼 CareerPilot – Personal ATS & Job Application Automation

![Status](https://img.shields.io/badge/status-in%20development-yellow)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/fastapi-latest-009688?logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/next.js-14-black?logo=next.js&logoColor=white)
![Architecture](https://img.shields.io/badge/architecture-ADR--driven-purple)

## Overview

CareerPilot is a modern, AI-powered, **personal Applicant Tracking System (ATS)** built to organize, automate, and analyze the job-search process.

The project was originally designed for **my own use during job interviews** and is now **open-sourced** for visibility and learning. It also acts as a **portfolio project**, showcasing backend architecture, API design, and documentation-first engineering.

This repository is intentionally public **before an MVP exists** to demonstrate how I reason about systems, structure codebases, and document decisions from day one.

## Project Status

This project is in **early development**.

- There is no MVP yet
- Features and APIs are incomplete
- Documentation may describe *planned* behavior

The current value of the repository is architectural clarity and design intent, not runnable completeness.

## Project Progress

Detailed mvp implementation progress is tracked in [`docs/progress/mvp_progress.md`](docs/progress/mvp_progress.md).

## Why This Project Exists

Job searching produces fragmented data:

- applications
- CV and cover letter versions
- emails and interviews
- salaries and locations

CareerPilot treats job hunting as **structured data**, focusing on:

- clean separation of concerns
- explicit design decisions
- production-grade practices applied in a personal project

## How to Read This Repository

If you are reviewing this as an interviewer or engineer:

1. Start with the high-level README (this file)
2. Read the architecture overview in [`docs/architecture.md`](docs/architecture.md)
3. Browse the ADRs in [`docs/adr/`](docs/adr/) to understand trade-offs
4. Skim the public API contract to see how the system is intended to be consumed

Code will evolve; **architecture and intent are already stable**.

## Planned Capabilities

### Job Tracking

- Track job applications and status changes
- Timeline-based history (applied → interview → offer → rejection)
- Store CVs and cover letters per application
- Salary and cost-of-living metadata

### Automation & AI (Planned)

- Config-driven job scraping
- AI-assisted CV and cover letter generation
- Background workers for scoring and notifications
- Email parsing for application updates

### Insights (Planned)

- Application funnel and timelines
- Salary comparisons
- Cost-of-living impact per city

## Architecture Snapshot

CareerPilot follows an **API-first, layered modular monolith**.

```text
Routes → Services → Repositories → Domain Models
```

Key characteristics:

- strict separation of concerns
- business logic isolated from frameworks
- decisions documented via Architectural Decision Records (ADRs)

## Technology Stack

### Backend

- Python 3.11
- FastAPI
- SQLAlchemy (synchronous)
- SQLite for development, PostgreSQL planned

### Frontend

- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- shadcn/ui

### Environment

- Docker and Docker Compose

## Documentation

Documentation is treated as a first-class artifact.

- [`docs/architecture.md`](docs/architecture.md) – system overview and layering
- [`docs/adr/`](docs/adr/) – architectural decision records
- [`docs/public_api_contract.md`](docs/public_api_contract.md) – API guarantees and stability rules
- [`docs/openapi.v1.yml`](docs/openapi.v1.yml) – machine-readable API specification
- [`docs/api_evolution.md`](docs/api_evolution.md) – versioning and deprecation strategy

## Development Setup (Early)

Requirements:

- Docker & Docker Compose
- Python 3.11
- Node.js 20+

```bash
git clone https://github.com/Maria-Papa/CareerPilot.git
cd careerpilot
docker-compose up --build
```

Local ports:

- Frontend: <http://localhost:3000>
- Backend: <http://localhost:8000>

## Roadmap (High Level)

### Version 1.0 – MVP

- Core job tracking
- Manual job entry
- Dashboard with basic charts
- CV and cover letter storage

### Version 2.0

- Scraping engine
- Email parsing
- AI-assisted scoring

### Version 3.0

- Multi-user support
- SaaS exploration

## Philosophy

- Built for personal use, shared openly
- Learn by applying real-world best practices
- Architecture decisions are explicit and documented
- Documentation evolves alongside the code

## License

MIT License
