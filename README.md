# AI-Based Online Exam Integrity System

> Real-time AI proctoring platform: webcam / mic / screen monitoring → suspicious-behavior flagging → live cheating-risk score → instructor dashboard with alerts, recordings, and post-exam PDF reports.

**Type:** Graduation Project — Faculty of Computers and Data Science, Alexandria University (8 members)
**Repo:** `https://github.com/sayfeldinn/exam-integrity-system`
**Stack:** Next.js (web) + FastAPI + PostgreSQL / Redis / S3 + YOLOv8 / MediaPipe / FaceNet + Docker Compose

---

## Documentation

### Core (durable)

| Doc | Purpose |
|---|---|
| `docs/PROJECT_CONTEXT.md` | Full project context — feature set, MVP scope, tech stack, team roles, repo structure, Scrumban process |
| `docs/STARTING_PLAN.md` | **10-min orientation** — why and order for 8 people (thin pointer; if conflict, `M0` wins) |
| `docs/ARCHITECTURE.md` | Service diagram, repo tree, DB tables v0, auth flow, compose topology (v0) |
| `docs/API_CONTRACT.md` | Freeze of `students` / `sessions` / `violations` JSON + `GET /api/v1/health` OpenAPI snippet |
| `docs/ONBOARDING.md` | OS matrix (Windows/WSL2, macOS, Linux), `scripts/verify-setup.sh`, troubleshooting runbook |
| `CONTRIBUTING.md` | Branch naming `<type>/<member-name>/<desc>`, workflow, Ruleset, permissions, CODEOWNERS |

### Milestone plans (per-milestone execution — verifiable DoD)

| Doc | Purpose |
|---|---|
| [`docs/milestones/M0_IMPLEMENTATION_PLAN.md`](docs/milestones/M0_IMPLEMENTATION_PLAN.md) | **Canonical M0 execution spec** — Definition of Done `M0:21-96`, Phases `M0:99-186`, Exit Check `M0:349-360` |
| [`docs/milestones/README.md`](docs/milestones/README.md) | Index of `M0–M6` plans, status, and conventions |
| `docs/PROGRESS_LOG.md` | Sprint-by-sprint status (updated every Sunday retro) |
| `docs/supervisor-log.md` | Supervisor summary template |

Team roles formal doc: `Team_Roles.docx` (see `docs/PROJECT_CONTEXT.md:6`).

---

## Quick Start

Once `infra/docker-compose.yml` is scaffolded (`M0-26..M0-28`):

```bash
# 1. Copy env template (never commit .env)
cp infra/.env.example infra/.env

# 2. Validate compose config (no secrets needed)
docker compose -f infra/docker-compose.yml config

# 3. Build and start api + web + postgres
docker compose -f infra/docker-compose.yml up --build

# 4. Verify
curl http://localhost:8000/api/v1/health        # → {"status":"ok"}
curl http://localhost:3000                       # web renders health
# or: make up  (wrapper for the docker command above)
```

Standalone dev (without Docker, after `M0-14..M0-25`):

```bash
# api
cd services/api && uv sync && uvicorn main:app --reload --port 8000

# web (in another terminal)
cd apps/web && npm ci && npm run dev   # http://localhost:3000
```

Verify setup script (after `M0-28`):

```bash
./scripts/verify-setup.sh        # Linux / macOS / WSL
powershell -ExecutionPolicy Bypass -File scripts\verify-setup.ps1   # Windows
```

See `docs/ONBOARDING.md` for Windows/WSL2, macOS, and Linux prerequisites.

---

## Branch Workflow

**Branch naming (required):** `<type>/<member-name>/<short-description>` — see `CONTRIBUTING.md:1`

```
feat/seif/agent-tool-calling
fix/sara/api-error-handling
docs/mohamed/project-documentation
```

Allowed types: `feat/ fix/ docs/ refactor/ test/ chore/` — all with `<member-name>/`.

**Workflow:** `git checkout -b <type>/<member-name>/<desc>` → `push` → open PR to `main` → resolve conversations → **1 approval from leader** (only `Admin` can bypass, `For pull requests only`) → squash-merge. **Never push directly to `main`** (initial `git push -u origin main` before Ruleset is the sole exception). Full Ruleset: `CONTRIBUTING.md:2-4`, execution gate: `docs/milestones/M0_IMPLEMENTATION_PLAN.md:57-60`.

---

## Repo Structure

```
exam-integrity-system/
├── apps/
│   ├── web/                 # Next.js — student + proctor frontend
│   └── mobile-proctor/      # Flutter proctor app (future — empty for now)
├── services/
│   ├── api/                 # FastAPI — auth, sessions, DB, WebSockets
│   ├── cv-identity/         # Face detection/recognition, eye tracking, head pose
│   ├── cv-objects/          # YOLO phone/person detection
│   ├── audio/               # Voice detection, background noise
│   └── risk-engine/         # Risk scoring fusion, Gemini assistant, reports
├── packages/
│   └── shared/              # Shared types/schemas (web + api)
├── infra/
│   ├── docker-compose.yml   # api + web + postgres (see M0-27)
│   └── .env.example         # required env vars (see M0-8)
├── scripts/
│   └── verify-setup.sh|.ps1 # OS checks (see M0-28)
├── docs/
│   ├── PROJECT_CONTEXT.md
│   ├── STARTING_PLAN.md
│   ├── milestones/
│   │   ├── M0_IMPLEMENTATION_PLAN.md
│   │   ├── M1_IMPLEMENTATION_PLAN.md  # from M1
│   │   └── README.md                  # index of M0–M6
│   ├── ARCHITECTURE.md
│   ├── API_CONTRACT.md
│   ├── ONBOARDING.md
│   ├── PROGRESS_LOG.md
│   └── supervisor-log.md
├── .github/
│   ├── workflows/           # CI (lint on PR) — added in M0-29
│   └── ISSUE_TEMPLATE.md
├── CONTRIBUTING.md
├── CODEOWNERS
├── .gitignore / .dockerignore / .editorconfig
├── .nvmrc / .python-version
└── LICENSE
```

---

## Team

| Name | Specialization |
|---|---|
| Seif Eldeen Nasser | AI / ML / Computer Vision |
| Jana Mostafa | AI / ML / Computer Vision |
| Adel Serag | ML / Frontend |
| Hana Marwan Negm | Full Stack |
| Rodaina Gomaa | Full Stack |
| Moatasem Mohamed | AI / Flutter |
| Ahmed Refaat | AI / Flutter |
| Huda Mohamed Hasson | UI/UX / ML |

Leader owns `main` Ruleset and `services/api` contract. See `docs/PROJECT_CONTEXT.md:6` + `CONTRIBUTING.md:3`.

---

## Milestones

| Milestone | Target | Scope |
|---|---|---|
| M0 — Repo & Scaffolding | Week 1–2 | Skeleton, `services/api` + `apps/web` scaffolded, Ruleset, `docker compose up` on 2 OSes |
| M1 — Enrollment | Week 3–4 | Student registration, ID/photo, DB schema |
| M2 — Liveness Detection | Week 5–6 | Live face verification end-to-end |
| M3 — Continuous Re-verification | Week 7–8 | Periodic identity re-checks |
| M4 — Suspicious Activity Detection | Week 9–10 | Risk fusion → risk score |
| M5 — Instructor Dashboard | Week 11–12 | Live sessions, alerts, risk scores |
| M6 — Integration & Defense Prep | Week 13+ | E2E testing, demo, slides |

Detailed M0 plan: `docs/milestones/M0_IMPLEMENTATION_PLAN.md`. Progress: `docs/PROGRESS_LOG.md`.

---

## Contributing

See `CONTRIBUTING.md` for branch naming, commit style, PR SLA (<24h, leader final approver), and `Write` vs `Admin` permissions. Issues use `.github/ISSUE_TEMPLATE.md` (Area / Milestone / Acceptance / Dependencies).

---

## License

MIT — confirm supervisor requirement. See `LICENSE`.
