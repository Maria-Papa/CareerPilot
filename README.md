# 🚀 CareerPilot – Personal ATS & Job Application Automation

CareerPilot is a modern, AI-powered, fully personal Applicant Tracking System (ATS) designed for software engineers who want to organize, automate, and optimize their job-search process.

This project acts both as a **product** and a **portfolio piece**, highlighting backend architecture, frontend engineering, automation, scraping, and AI integration.

## 🌟 Features

### 🔍 Job Discovery & Tracking

- Dynamic job scraping engine (config-driven, no code changes needed)
- Job saving, tagging, and scoring
- Timeline of all application events (applied → interviews → offer → rejection)
- Store salary expectations, offered salary, COL, flexibility, job URL
- Track status: `applied`, `saved`, `declined`, `rejected`, `no response`
- Store customized CV & cover letter per application

### 🤖 Automation & AI

- AI-powered resume generation from LaTeX template
- AI-powered cover letter writer tailored for each job
- Predict interview questions based on role + past data
- Background workers for scraping, scoring, notifications
- Email parsing: auto-detect application updates, interview invites, assessments

### 📈 Insights & Visualization

- Pie chart for application status
- Salary comparison vs market averages & medians
- Cost-of-living savings estimation per city
- Job funnel & timeline graphs
- Company salary history for positions

### 💼 Career Data Management

- Master JSON of full career history
- Store all emails per job (application, interviews, assessments)
- Track interview questions asked
- Track take-home assignments
- Salary intelligence per company & city

## 🧱 Architecture Overview

CareerPilot is built using a modern, service-oriented stack optimized for scraping, automation, and AI agents.

**Frontend:** Next.js (React), TypeScript, TailwindCSS, Shadcn/UI, Recharts </br>
**Backend:** Python (FastAPI) </br>
**DB:** PostgreSQL </br>
**Queue:** Redis + RQ or Celery </br>
**Scraping:** Playwright (browser) + Dynamic JSON config system </br>
**AI:** OpenAI API (agents), LaTeX PDF rendering </br>
**Environment:** WSL2 (Ubuntu), Docker, Docker Compose

## 🛠 Installed VS Code Plugins (Verified Publishers Only)

### Python / Backend

- **Python** – Microsoft
- **Pylance** – Microsoft
- **Black Formatter** – Microsoft

### Frontend / React / Next.js

- **Tailwind CSS IntelliSense** – Tailwind Labs
- **Prettier - Code formatter** – Prettier
- **TypeScript and JavaScript Language Features (built-in)** – Microsoft

### Productivity / Tooling

- **GitLens — Git supercharged** – GitKraken
- **Docker** – Microsoft
- **YAML** – Red Hat

### Documentation / Data

- **Markdown All in One** – Yu Zhang
- **JSON Language Features (built-in)** – Microsoft

## 🗂 Project Structure (Planned)

```txt
careerpilot/
backend/
app/
api/
models/
services/
scraping/
configs/
plugins/
tests/
Dockerfile
frontend/
src/
components/
pages/
hooks/
services/
public/
Dockerfile
data/
latex_templates/
resumes/
cover_letters/
infra/
docker-compose.yml
nginx/
docs/
architecture.md
manifest.md
.vscode/
extensions.json
settings.json
README.md
```

## 🧪 MVP Scope

### Backend (FastAPI)

- User auth (token-based)
- CRUD for job applications
- File upload for CV vs CL
- Store salary + COL data
- Basic scraping (1–2 sites)
- Timeline events API
- Pie chart data endpoint

### Frontend (Next.js)

- Dashboard + pie chart
- Job list & details
- Add/update job form
- Upload CV/cover letter per job
- Salary & COL input screens

### Background Tasks

- Scheduled scraping (small)
- Simple job scoring

## 🛠 Development Setup

### Prerequisites

- Windows 11 with **WSL2 (Ubuntu)**
- Docker + Docker Compose
- Python 3.11
- Node.js 20+
- LaTeX distribution (TexLive or MiKTeX)

### Install (WSL2)

```bash
git clone https://github.com/yourname/careerpilot.git
cd careerpilot
docker-compose up --build
```

Frontend will run at: <http://localhost:3000>

Backend will run at: <http://localhost:8000>

## 🚧 Roadmap

### Version 1.0 (MVP)

- Basic scraper
- Dashboard + job tracking
- Store CV/CL per application
- Salary/COL inputs & graphs
- Timeline + events

### Version 2.0

- Email parsing (Gmail API)
- Job scoring AI agent
- Interview question predictor
- Browser extension for auto-fill

### Version 3.0

- Multi-user capability
- SaaS version
- Automated city salary scraping
- Marketplace of scraping configs

## 📄 License

MIT License.
