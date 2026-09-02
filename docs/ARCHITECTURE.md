# Architecture — AI-Based Online Exam Integrity System (v0)

> M0 stub — service diagram, repo tree, DB tables v0, auth stub, compose topology.
> Created in `M0-4` `M0:110`, reviewed per DoD `M0:64` (1 CV + 1 Full-Stack).
> Canonical data contract lives in `docs/API_CONTRACT.md` (see `M0-19` `M0:136`).

## 1. Service Diagram (v0)

```
Browser (Next.js apps/web)
   │ getUserMedia (WebRTC video/audio) + screen/tab events
   │ fetch NEXT_PUBLIC_API_URL/api/v1/* (client-side, CORS)
   ▼
services/api (FastAPI)  ──► PostgreSQL (students/sessions/violations)
   │  ▲  │                     ▲
   │  │  └── JWT (future M1)  │
   │  │                       │
   │  └── WebSockets (future M2+) ──► Proctor Dashboard (apps/web)
   │
   ├──► services/cv-identity (future: face detection/recognition, liveness)
   ├──► services/cv-objects  (future: YOLO phone/person)
   ├──► services/audio       (future: VAD, noise)
   └──► services/risk-engine (future: risk fusion, Gemini, reports)

packages/shared — single source of truth types (M0-19 M0:136)
infra — docker-compose.yml wiring api + web + postgres (M0-27 M0:166) + .env.example (M0-8 M0:114)
```

**Boundaries v0 (M0):**
- `services/api` owns DB + migrations (`alembic`), auth stub, `/api/v1/health` (public).
- `apps/web` owns UI shell + client fetch of health with fallback `API unreachable`.
- CV/audio/risk-engine are **placeholders** (`.gitkeep`) — no code, no containers in M0. Their real work starts M1 after `API_CONTRACT.md` frozen.
- `packages/shared` types imported by both `services/api/schemas` and `apps/web/lib/api.ts` (DoD `M0:49`).

## 2. Repo Tree (v0)

```
exam-integrity-system/
├── apps/
│   ├── web/                 # Next.js (M0-21..M0-25)
│   └── mobile-proctor/      # Flutter — future empty (M0-1 .gitkeep)
├── services/
│   ├── api/                 # FastAPI (M0-14..M0-20) — main.py, routers/, models/, schemas/, core/config.py
│   ├── cv-identity/         # .gitkeep (M0-1)
│   ├── cv-objects/          # .gitkeep
│   ├── audio/               # .gitkeep
│   └── risk-engine/         # .gitkeep
├── packages/
│   └── shared/              # types/violation.ts, types/session.ts (M0-19)
├── infra/
│   ├── docker-compose.yml   # M0-27 wiring api+web+postgres, healthcheck, pgdata, app_net
│   └── .env.example         # M0-8 canonical 10 vars
├── scripts/
│   ├── verify-setup.sh      # M0-28 OS checks
│   └── verify-setup.ps1
├── docs/
│   ├── PROJECT_CONTEXT.md
│   ├── STARTING_PLAN.md     # 10-min pointer → milestones/M0
│   ├── milestones/
│   │   ├── M0_IMPLEMENTATION_PLAN.md  # M0 canonical (M0:21-96 DoD)
│   │   └── README.md                  # index of M0–M6
│   ├── ARCHITECTURE.md      # this file
│   ├── API_CONTRACT.md      # M0-19 freeze
│   ├── ONBOARDING.md        # M0-28 OS matrix
│   ├── PROGRESS_LOG.md
│   └── supervisor-log.md
├── .github/
│   ├── workflows/ci.yml     # M0-29 lint on PR
│   └── ISSUE_TEMPLATE.md
├── CONTRIBUTING.md          # M0-5 branch + workflow + Ruleset
├── CODEOWNERS               # M0-6 sayfeldinn required
├── .gitignore / .dockerignore / .editorconfig
├── .nvmrc (20) / .python-version (3.11.8)
└── LICENSE (MIT)
```

## 3. DB Tables v0 (M0-18)

Migrated via `alembic` — `alembic current == head`, `psql \dt` shows 3 tables. Full DDL in `M0-18` `M0:135` and `docs/API_CONTRACT.md`.

**`students`** — `id PK`, `name`, `university_id UNIQUE`, `registered_photo_ref`, `hashed_password`, `role enum (student/proctor/admin)`, `created_at`, indexes on `university_id`.

**`sessions`** — `id PK`, `student_id FK→students`, `exam_id`, `start_time`, `status enum (pending/active/ended)`, `created_at`, indexes on `student_id`, `status`.

**`violations`** — `id PK`, `session_id FK→sessions`, `type enum (phone/person/face_loss/head_turn/voice/noise/screen_leave)`, `timestamp`, `risk_contribution float CHECK 0-1`, `confidence float`, `meta jsonb`, indexes on `session_id`, `timestamp`, `type`.

Extensions in M1+ (not M0): `students.embedding`, `sessions.liveness_score`, `violations` additional types.

## 4. Auth Flow Stub (v0 → M1)

- **M0:** `GET /api/v1/health` is **public** (no auth) `M0:32`. `JWT_SECRET` exists in `infra/.env.example` but not enforced. Roles stubbed in `students.role`.
- **M1+:** `POST /api/v1/auth/login` → JWT issuance (`python-jose`, `passlib[bcrypt]` per `M0-14` pins), `dependencies.get_current_user` guards `/api/v1/*` (except health). Role-based access (student/proctor/admin) per `PROJECT_CONTEXT.md:114-115`.

## 5. API Contract Pointer

Canonical JSON fields, enums, and `GET /api/v1/health` OpenAPI snippet are frozen in `docs/API_CONTRACT.md` (`M0-19` `M0:136`) and `packages/shared` types. See also `CONTRIBUTING.md:4` workflow.

## 6. Compose Topology (v0)

```
services:
  postgres:
    image: postgres:16-alpine
    healthcheck: pg_isready -U $POSTGRES_USER
    volumes: [pgdata:/var/lib/postgresql/data]
  api:
    build: services/api/Dockerfile (python:3.11-slim, HEALTHCHECK curl /api/v1/health)
    depends_on: postgres: {condition: service_healthy}
    env_file: infra/.env
    ports: ["8000:8000"]
  web:
    build: apps/web/Dockerfile (node:20-alpine multi-stage)
    env: NEXT_PUBLIC_API_URL
    ports: ["3000:3000"]
    depends_on: [api]
volumes: pgdata
networks: app_net
# redis: image: redis:7-alpine # post-MVP M4 — one uncomment (M0-27 stub)
```

Validation: `docker compose -f infra/docker-compose.yml config` after `cp infra/.env.example infra/.env` (`M0-8`).

---

*Update this file per milestone — keep v0 as snapshot, append v1 decisions.*
