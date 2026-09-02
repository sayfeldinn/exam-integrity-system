# M0 Implementation Plan — Repo & Scaffolding (Revised)

> Scope: this covers **only** M0 (Section 4/8 of `PROJECT_CONTEXT.md`) — the
> milestone where the repo goes from empty to "every team member can clone,
> run `docker compose -f infra/docker-compose.yml up`, and open a PR."
> Nothing here touches actual feature logic (enrollment, liveness, etc.) —
> that starts at M1.
>
> Target duration: **Week 1–2 (10 working days + 3-day buffer = 13 calendar days)**.
> This plan breaks that into 5 phases so you can turn each task directly into
> a GitHub Issue tagged to the M0 milestone. All 8 members have real work
> from Day 1 — no one idles.
>
> Conventions fixed vs. original: compose lives at `infra/docker-compose.yml` (invoke
> via `docker compose -f infra/docker-compose.yml up` or `make up` wrapper).
> Branch naming is `<type>/<member-name>/<short-description>` per
> `CONTRIBUTING.md` (not `feature/<area>-<desc>`). Ruleset is `Settings → Rules → Rulesets` targeting `main` (not legacy `Settings → Branches` rule).

---

## Definition of Done for M0

M0 is complete when **all** of the following are true. This is the **intersection**
of `docs/STARTING_PLAN.md:219-231` (Quick Checklist) and the board/process
requirements — the original plan dropped 3 checklist items and expanded ceremony
without the technical contract. That drift is fixed here:

### Code & Infra (must pass on a fresh clone on 2 OSes: Windows + Linux/Mac)
- [ ] Repo skeleton (Section 7 folder tree) is pushed to `main` — Section 7
      tree + `apps/web`, `services/api` scaffolded, other service folders as
      `.gitkeep` placeholders
- [ ] `services/api` runs locally (`uvicorn main:app --reload` **and** via
      Docker) and returns `200 OK` on `GET /api/v1/health` and `GET /health`
      (redirect). Health is **public** — all future `/api/v1/*` will be
      JWT-protected (stub noted in `docs/ARCHITECTURE.md`).
- [ ] `apps/web` runs locally (`npm run dev` **and** via Docker) and
      successfully displays the result of calling `/api/v1/health` via
      `NEXT_PUBLIC_API_URL` (client-side `fetch`, with fallback UI
      "API unreachable — check `docker logs api`")
- [ ] `docker compose -f infra/docker-compose.yml up --build` starts
      `api + web + postgres` together with one command, with
      `healthcheck: pg_isready`, `depends_on: condition: service_healthy`,
      named volume `pgdata`, network `app_net`, and `ports` mapped.
      `web → api` reachability verified from browser (not just server fetch).
- [ ] DB migrations exist: `alembic` initialized, one migration creates
      `students` / `sessions` / `violations` in Postgres, `alembic current`
      == head, `psql \dt` shows 3 tables. `docker compose down -v && up --build`
      reproduces clean.
- [ ] `packages/shared` has single source of truth types for
      `Violation`/`Session`/`Student` (TS + Python or OpenAPI export), imported
      by both `services/api/schemas` and `apps/web/lib/api.ts`
- [ ] `infra/.env.example` lists **all** vars with comments + no secrets and
      validates via `docker compose -f infra/docker-compose.yml config` after
      `cp infra/.env.example infra/.env` (see M0-8 acceptance)
- [ ] Dockerfiles exist: `services/api/Dockerfile` + `apps/web/Dockerfile`
      (multi-stage `node:20-alpine`) + `.dockerignore` with `HEALTHCHECK`

### Docs & Process
- [ ] Ruleset is **active** targeting `main`: **restrict direct pushes/updates to `main`**, **restrict deletions**, **block force pushes**, **require PR**, **require 1 approval** (from leader — see below), **dismiss stale approvals when new commits are pushed**, **require conversation resolution before merging**, **require status checks (lint)** and **require branches up-to-date**. Bypass: only `Admin` (leader) can bypass, mode **For pull requests only**; members have `Write` not `Admin` and cannot bypass. `CODEOWNERS` requires `@<leader>` for all paths (peers as commenters). Allowed branches: `feat/*`, `fix/*`, `docs/*`, `refactor/*`, `test/*`, `chore/*` — all as `<type>/<member-name>/<short-description>` per `CONTRIBUTING.md`.
- [ ] Branch naming convention `<type>/<member-name>/<short-description>` documented in `CONTRIBUTING.md` and linked from `README.md` — types: `feat/`, `fix/`, `docs/`, `refactor/`, `test/`, `chore/`; examples: `feat/seif/agent-tool-calling`, `feat/ahmed/frontend`, `fix/sara/api-error-handling`, `docs/mohamed/project-documentation`
- [ ] `CONTRIBUTING.md` exists (branch naming `<type>/<member-name>/<desc>`, workflow `branch → push → PR → leader approval → squash-merge`, commit style, PR SLA <24h with leader as final approver, rebase + squash-merge, `Write` vs `Admin` permissions)
- [ ] `LICENSE` (MIT recommended — confirm supervisor requirement) + link to
      `Team_Roles.docx` present in `README.md`
- [ ] `docs/ARCHITECTURE.md` v0 committed (service diagram, repo tree, DB
      tables v0 with enums, auth flow stub, API contract section, compose
      topology). Reviewed by 1 CV + 1 Full-Stack member.
- [ ] `docs/API_CONTRACT.md` (or `ARCHITECTURE.md#API Contract`) freezes
      `students`/`sessions`/`violations` JSON fields, `session_status` enum,
      `violation.type` enum, `risk_contribution float 0-1`, and
      `GET /api/v1/health` OpenAPI snippet. This is the artifact that
      `STARTING_PLAN.md:229` requires before CV work.
- [ ] `docs/ONBOARDING.md` exists with OS matrix (Windows/WSL2, Mac, Linux),
      `scripts/verify-setup.sh|.ps1` checks, and troubleshooting runbook
- [ ] `.github/ISSUE_TEMPLATE.md` is in place and auto-suggests on new issues;
      board fields `Area`/`Milestone` align with template (no double bookkeeping)
- [ ] GitHub Projects board exists with columns
      `Backlog → This Sprint → In Progress → In Review (PR open) → Done`,
      WIP limits `This Sprint ≤8, In Progress ≤4, In Review ≤4`, and custom
      fields `Area`, `Milestone`
- [ ] GitHub Milestones M0–M6 are created (due dates TBD until defense date D;
      M0 due = D-14 weeks per `PROJECT_CONTEXT.md:222-236`; if D <12w away,
      compress M0 to 7 days by cutting `M0-16` polish)
- [ ] Lint/format gate: `ruff` + `black` (Python, `pyproject.toml`) +
      `eslint` + `prettier` (web) + `pre-commit` hooks + minimal
      `.github/workflows/ci.yml` (`lint` on PR) passing on `main`
- [ ] All 8 team members have cloned and successfully run the stack (screenshot
      of `web` showing `{"status":"ok"}` posted in their test PR), on at least
      2 OS families
- [ ] Sprint 1 planning session has happened using the live board
- [ ] `docs/PROGRESS_LOG.md` has a **dated** Sprint 1 entry (done / in-progress
      / blocked / decisions + onboarding friction log) and
      `docs/supervisor-log.md` has M0 summary ready to paste to instructor

Nothing here is "nice to have" — a team member who can't run the project
locally by the end of M0 will be blocked for every future milestone.

---

## Phase 1 — Repo Foundation (Day 1)

Blocks everything else for code, but board/milestone work runs **in parallel**
on Day 1 so no one idles. Skeleton push itself stays single-owner to avoid
conflicts.

| ID | Task | Depends on | Est. | Owner |
|---|---|---|---|---|
| M0-1 | Create folder skeleton (Section 7 tree) with `README.md`/`.gitkeep` placeholders in every empty folder (`apps/mobile-proctor`, `services/cv-identity`, `services/cv-objects`, `services/audio`, `services/risk-engine`, `packages/shared`) | — | 30 min | Leader |
| M0-2 | Write root `README.md`: project name + one-line description + link to `docs/PROJECT_CONTEXT.md` + `docs/ARCHITECTURE.md` + `docs/ONBOARDING.md` + `Team_Roles.docx` + `CONTRIBUTING.md` branch convention + quick-start `cp infra/.env.example infra/.env && docker compose -f infra/docker-compose.yml up --build` + `make up` wrapper note | M0-1 | 30 min | Leader |
| M0-3 | Add `.gitignore` (Node + Python combined), `.dockerignore` (`node_modules`, `.venv`, `__pycache__`, `.next`, `*.pyc`), `.editorconfig`, pin toolchains `.nvmrc` (node 20), `.python-version` (3.11.8) | M0-1 | 15 min | Leader |
| M0-4 | Populate `docs/`: copy `PROJECT_CONTEXT.md`, `STARTING_PLAN.md` (**exact casing** — case-sensitive Linux), `PROGRESS_LOG.md` + create `docs/ARCHITECTURE.md` v0 stub (service diagram, repo tree, DB tables v0, auth stub, compose topology) + `docs/API_CONTRACT.md` placeholder + `docs/ONBOARDING.md` skeleton + `docs/supervisor-log.md` template | M0-1 | 45 min | Leader + Huda (diagram) |
| M0-5 | Add `CONTRIBUTING.md` with branch naming `<type>/<member-name>/<short-description>` (types: `feat/ fix/ docs/ refactor/ test/ chore/`), full workflow (`branch → push → PR → resolve conversations → 1 leader approval (stale dismissed) → squash-merge; never push directly to `main` after Ruleset`), commit style, PR SLA <24h with leader as final approver, rebase + squash-merge, `CODEOWNERS` requires leader + `Write` vs `Admin` permissions (see Step 2) | M0-2 | 20 min | Leader |
| M0-6 | Add `LICENSE` (MIT — confirm supervisor) + `CODEOWNERS` file: all paths require `@<leader>` (leader is final approver and only bypass holder); peers (`@hana`, `@rodaina`, `@adel`, `@huda`) may be listed as optional reviewers/commenters but not as required approvers or bypass holders — e.g. `/services/api/ @<leader>`, `/apps/web/ @<leader>`, `/infra/ @<leader>`, `/docs/ @<leader>`, `packages/shared/ @<leader>` (add peers after leader if desired for notification, but leader approval still required) | M0-1 | 15 min | Leader |
| M0-7 | Copy `ISSUE_TEMPLATE.md` into `.github/ISSUE_TEMPLATE.md` and verify frontmatter `labels: [area:*]` aligns with board custom fields (no duplication) | M0-1 | 10 min | Leader |
| M0-8 | Write `infra/.env.example` with comments, no secrets — must cover: `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_HOST=postgres`, `POSTGRES_PORT=5432`, `DATABASE_URL=postgresql+asyncpg://...`, `API_PORT=8000`, `WEB_PORT=3000`, `JWT_SECRET=change-me`, `CORS_ORIGINS=http://localhost:3000`, `NEXT_PUBLIC_API_URL=http://localhost:8000`. Compose must use `env_file`. **Acceptance:** fresh clone `cp infra/.env.example infra/.env && docker compose -f infra/docker-compose.yml config` validates. Ensure `.env` is gitignored. | M0-1 | 45 min | Leader + Hana (validator) |
| M0-9 | Initial commit + push to `main`: `git init; git add .; git commit -m "chore: initial repo skeleton"; git branch -M main; git remote add origin <url>; git push -u origin main` | M0-1 to M0-8 | 10 min | Leader |
| M0-10 | Activate Ruleset targeting `main` (Settings → Rules → Rulesets): restrict direct pushes/updates to `main`, restrict deletions, block force pushes, require PR, require 1 approval from leader (dismiss stale approvals, require conversation resolution, require status checks (lint — enabled after M0-29) + require branches up-to-date). Bypass: only `Admin` (leader) can bypass, mode **For pull requests only**; members `Write` cannot bypass/modify Ruleset. | M0-9 | 10 min | Leader (only Admin; team members `Write` — no deputy Admin; bus-factor via Org team containing only leader if needed) |
| M0-11 | Set up GitHub Projects board: columns `Backlog → This Sprint → In Progress → In Review → Done`, WIP limits `This Sprint≤8, In Progress≤4, In Review≤4`, custom fields `Area` (`cv-identity/cv-objects/audio/api/web/risk-engine/ux/infra`) + `Milestone` (M0-M6), labels per area | — (parallel Day 1) | 45 min | Huda (board UX) — uses Figma/board design skill |
| M0-12 | Create GitHub Milestones M0–M6 with target dates (TBD until D). M0 due = D-14w; document compression rule if D<12w | — (parallel Day 1) | 20 min | Ahmed |
| M0-13 | Create all 27 M0 issues on the board in `Backlog` with correct `Area` label + `M0` milestone from creation (no retroactive tagging). Seed `This Sprint` with M0-14/M0-21 | M0-11, M0-12 | 30 min | Moatasem + Ahmed |

**Coordination Day 1:** Leader pushes skeleton; Huda/Ahmed/Moatasem build board so Day 2 parallel work is visible. No one with `—` independence is actually delayed to Phase 4.

---

## Phase 2 — Backend Scaffolding (Day 2–4, parallel with Phase 3)

Highest-priority track after Phase 1 — everything M1 onward depends on the schema/contract here being **migrated**, not just sketched.

| ID | Task | Depends on | Est. | Owner |
|---|---|---|---|---|
| M0-14 | Initialize FastAPI project `services/api`: `main.py`, `routers/`, `models/`, `schemas/`, `core/config.py`; `pyproject.toml` pins `fastapi`, `uvicorn[standard]`, `sqlalchemy[asyncio]`, `asyncpg`, `alembic`, `pydantic-settings`, `python-jose[cryptography]`, `passlib[bcrypt]`; `.python-version` 3.11.8; `ruff`+`black` config. Acceptance: `uv sync`/`pip install -e .` reproducible. | M0-9, M0-8 | 2 hr | Hana (FastAPI + /health) |
| M0-15 | Centralize settings `services/api/core/config.py` via `pydantic-settings`: load `DATABASE_URL`, `JWT_SECRET`, `CORS_ORIGINS`, `API_PORT` from env; fail fast if missing. Acceptance: `python -c "from core.config import settings; print(settings.DATABASE_URL)"` works with `infra/.env`. | M0-14, M0-8 | 45 min | Hana |
| M0-16 | Add `/health` — `GET /api/v1/health → {"status":"ok"}` + `GET /health` redirect, public (no auth), plus `CORSMiddleware` `allow_origins=[http://localhost:3000]`, `allow_credentials`, `allow_methods=["*"]`. Include router in `main.py`. Acceptance: `curl localhost:8000/api/v1/health` → 200. | M0-14 | 30 min | Hana |
| M0-17 | Postgres connection: `asyncpg` engine via `DATABASE_URL`, `healthcheck: pg_isready -U $POSTGRES_USER` in compose (defined in M0-27 but tested standalone here). Acceptance: `python -c "import asyncio; ... test connection"` succeeds as `M0-15` settings. | M0-15 | 45 min | Rodaina |
| M0-18 | Define core tables + Alembic: `students(id PK, name, university_id unique, registered_photo_ref, hashed_password, role enum student/proctor/admin, created_at)`, `sessions(id PK, student_id FK→students, exam_id, start_time, status enum pending/active/ended, created_at)`, `violations(id PK, session_id FK→sessions, type enum phone/person/face_loss/head_turn/voice/noise/screen_leave, timestamp, risk_contribution float CHECK 0-1, confidence float, meta jsonb)`, indexes on `student_id/session_id/timestamp`; `alembic init`, first revision, `alembic upgrade head` verified via `psql \dt`. **Not near-empty** — must be migrated. | M0-17 | 2.5 hr | Rodaina (schema) — **advisory reviewers: Seif + Jana (CV)** must comment before leader approves; **required approver: Leader** (contract owner, only bypass holder) |
| M0-19 | Freeze contract: write `docs/API_CONTRACT.md` with JSON examples for `Violation`/`Session` + OpenAPI snippet for `GET /api/v1/health`; scaffold `packages/shared`: `types/violation.ts`, `types/session.ts`, `violation.py`/OpenAPI export script + README "single source of truth". Acceptance: both `services/api/schemas` and `apps/web/lib/api.ts` import shared types. | M0-18 | 1 hr | Rodaina + Seif/Jana (CV input) — **Leader approval required** to freeze contract |
| M0-20 | Open PR from `<type>/<member-name>/<desc>` branch, get reviewed by Seif + Jana (advisory) and **approved by Leader (required, only Admin/bypass holder)**, then squash-merge to `main`. **Timeboxed:** 48h for schema debate; unresolved items → `PENDING_REVIEW` and extended in M1 — no bikeshedding past deadline. Review SLA 24h; if no leader review, author pings `#standup` and leader reassigns. Dismiss stale approvals on new pushes; conversations must be resolved. | M0-16, M0-18, M0-19 | 1 day (incl. review latency) | Hana/Rodaina |

**Why split Hana/Rodaina not paired:** parallelizes FastAPI vs DB; CV reviewers de-risk M1 contract drift.

---

## Phase 3 — Frontend Scaffolding (Day 2–4, parallel with Phase 2)

Proves `web → api` end-to-end before any real feature. Must not block on full schema — use mock.

| ID | Task | Depends on | Est. | Owner |
|---|---|---|---|---|
| M0-21 | Initialize Next.js `apps/web`: `create-next-app` with TypeScript + App Router + ESLint + Prettier + Tailwind decision documented in `apps/web/README.md`; `.nvmrc` 20; `NEXT_PUBLIC_API_URL` via `.env.local.example`. Acceptance: `npm ci` reproducible, `npm run lint` passes, `npm run dev` serves. | M0-9 | 1 hr | Adel |
| M0-22 | Build layout shell (header, page container) + design tokens. Define mock `GET /api/v1/health → {"status":"ok"}` via `msw` or local stub so `M0-23` doesn't idle. | M0-21 | 1 hr | Adel (scaffold) + Huda (design tokens/layout) |
| M0-23 | Placeholder page `/health` that **client-side `fetch`s** `${process.env.NEXT_PUBLIC_API_URL}/api/v1/health` (fallback to mock if API not yet merged) and renders result + error state "API unreachable — check `docker logs api`". Acceptance: works with mock on Day 2, real API on Day 4 without code change (env switch only). | M0-21, M0-16 (mock until merged) | 1 hr | Adel |
| M0-24 | Verify CORS/env from **browser fetch** (not server `fetch` — Route Handler proxy would hide CORS). Document `NEXT_PUBLIC_API_URL=http://localhost:8000` locally vs `http://api:8000` in Docker network. If CORS fails, fix is in `services/api/main.py` (M0-16), not frontend. | M0-23, M0-16 | 30 min | Adel + Rodaina (pair, 1h) |
| M0-25 | Open PR from `<type>/<member-name>/<desc>` branch, get reviewed by Hana + Huda (advisory) and **approved by Leader (required, only Admin/bypass holder)**, then squash-merge to `main`. Conversations resolved, stale dismissed. | M0-23, M0-24 | 1 day (incl. review) | Adel/Huda |

**Mock contract detail (Day 2):** Leader publishes `docs/API_CONTRACT.md` snippet for `/health` on Day 2 (M0-19 partial), frontend codes against mock and swaps URL when `M0-16` merges — no idle.

---

## Phase 4 — Infra & Tooling (Day 5–7)

Starts once Phases 2 and 3 each run **standalone** (not containerized) — per `STARTING_PLAN.md:204-215`. Don't skip ahead.

| ID | Task | Depends on | Est. | Owner |
|---|---|---|---|---|
| M0-26 | Write Dockerfiles + `.dockerignore`: `services/api/Dockerfile` (`python:3.11-slim`, `uv`/`pip` install, `HEALTHCHECK CMD curl -f http://localhost:8000/api/v1/health`), `apps/web/Dockerfile` (multi-stage `node:20-alpine` builder → runner), `.dockerignore` at root and per-service. | M0-20, M0-25 | 1 hr | Leader + Hana |
| M0-27 | Write `infra/docker-compose.yml` wiring `api` + `web` + `postgres` (NOT redis/minio — deferred post-MVP per `PROJECT_CONTEXT.md:94,108`): `healthcheck: pg_isready`, `depends_on: condition: service_healthy` for `api→postgres`, named volume `pgdata`, network `app_net`, `ports` `3000:3000`, `8000:8000`, `5432:5432` (or 5433 to avoid host conflict), `env_file: ../infra/.env`, commented stub `# redis: image: redis:7-alpine # ports: ["6379:6379"]` + `app_net` so M4 is one uncomment. | M0-26, M0-8 | 2.5 hr | Leader + Hana |
| M0-28 | Verify `docker compose -f infra/docker-compose.yml up --build` on **1 Windows + 1 Mac** (from clean `down -v`): `api:/api/v1/health` 200, `web` renders health from browser, `psql` connect, `docker compose config` validates, logs clean. Document in `docs/ONBOARDING.md` + create `scripts/verify-setup.sh|.ps1` checking `node>=20`, `python>=3.11`, `docker>=20`, `git`, ports free. Include OS matrix: Windows WSL2 + Docker Desktop (Hyper-V, clone inside WSL), Mac Rosetta, Linux `usermod -aG docker`. | M0-27 | 1 hr (plus 2hr buffer for WSL) | Adel + Moatasem |
| M0-29 | Lint/format + CI: add `ruff`/`black` via `pyproject.toml`, `eslint`+`prettier` via `apps/web`, `pre-commit` hooks; minimal `.github/workflows/ci.yml` (on PR: `ruff check`, `black --check`, `npm run lint`, `docker compose -f infra/docker-compose.yml config`); enable **Require status checks** in Ruleset (M0-10) — adds `require branches up-to-date` + `require conversation resolution` already enforced. | M0-14, M0-21, M0-10 | 1.5 hr | Ahmed (AI track — keeps engaged) |

---

## Phase 5 — Team Onboarding (Day 8–10, + 3-day buffer)

Exit gate — a scaffold only one person can run is not done. Staggered to catch drift early, not batched at end.

| ID | Task | Depends on | Est. | Owner |
|---|---|---|---|---|
| M0-30 | **Pilot onboarding Day 4** (early): 1 Windows + 1 Mac volunteer run `scripts/verify-setup.sh` then `docker compose -f infra/docker-compose.yml up --build` and screenshot `web` showing `{"status":"ok"}`. Catches WSL/port/env drift 4 days before batch. | M0-20 (backend alone) | 1 hr | 2 volunteers |
| M0-31 | Full team clones: each of 8 runs `scripts/verify-setup.sh` → `cp infra/.env.example infra/.env` → `docker compose -f infra/docker-compose.yml up --build` → verifies `web` shows health + `alembic current==head` + `psql \dt`. Post screenshot in PR. **Staggered, not batched.** | M0-28 | 45 min each (success path) + 4hr timebox before escalation | All 8 |
| M0-32 | Staggered test PRs to validate Ruleset + CI + review flow **using `ISSUE_TEMPLATE.md` and `<type>/<member-name>/<desc>` naming**: Day 3 (before critical merges) — e.g. `feat/hana/test-ruleset`, `feat/rodaina/test-ruleset`, `feat/adel/test-ruleset`; Day 8 — remaining 5 (e.g. `feat/seif/test-ruleset`) after compose works. Each needs **1 approval from leader** (only Admin/can bypass, stale dismissed, conversations resolved), 24h SLA, squash-merge. Validate: non-admin push to `main` fails, deletion blocked, unresolved conversation blocks merge, direct push rejected. No mass-close. | M0-10, M0-29 | 15 min each | All 8 (sequenced) |
| M0-33 | Fix env issues surfaced in M0-31: **timebox 2hr per issue**, triage owner **Hana (env/API)** + **Adel (web)**, fixes logged in `docs/ONBOARDING.md` (runbook) **and** `docs/PROGRESS_LOG.md` (retro). If >2 people fail same step → blocker for M0-34, extend M0 by buffer days. | M0-31 | 2hr per issue | Hana/Adel |
| M0-34 | Sprint 1 retro + planning: 30-min retro (what worked/slowed/change), board cleanup (`In Progress` >3 days → break down), write **dated Sprint 1 entry** in `docs/PROGRESS_LOG.md` (done/in-progress/blocked/decisions + onboarding friction), update `docs/supervisor-log.md` for instructor, draft M1 issues tagged to M1 milestone, freeze `docs/API_CONTRACT.md`. | M0-28, M0-31 (not blocked on M0-33 fixes — concurrent follow-up) | 30 min + 20 min writing | Leader |

> If anyone stuck >1hr on `M0-31`, that's worth fixing now (`docs/M0_IMPLEMENTATION_PLAN.md:121` preserved) — Week 1 friction repeats for every late joiner.

**AI/UX track engagement (prevents idle):** Moatasem + Ahmed (AI/Flutter) own `M0-29` CI + `M0-28` verify script; Seif/Jana own `M0-18`/`M0-19` review + `services/cv-identity/README` stub returning fake `{"face_found":true}` against mocked contract (2hr spike, no heavy deps) before M0-27 — this keeps CV track invested in contract they use in M1.

---

## Ready-to-paste example issues

Three highest-risk tasks, written in `.github/ISSUE_TEMPLATE.md` format so you can paste them directly. Note they now include frontmatter, `Notes`, correct acceptance, and OS/env specifics missing before.

<details>
<summary>M0-8 — Write infra/.env.example (the contract that all env loading depends on)</summary>

```
---
name: Task
about: M0-8 — infra/.env.example contract
title: "M0-8: Write infra/.env.example with all required vars"
labels: [area:infra]
assignees: leader
---

## Area
infra

## Milestone
M0 Scaffolding

## Description
Write `infra/.env.example` — the single source of truth for env vars. Backend
(`services/api/core/config.py` via pydantic-settings), web (`NEXT_PUBLIC_API_URL`),
and `infra/docker-compose.yml` (`env_file`) all read from this contract. Must be
done Day 1 so M0-14/M0-21 don't pick conflicting var names. No secrets in file;
add comments explaining each var. Ensure `.env` (real) is gitignored.

## Acceptance criteria
- [ ] File exists at `infra/.env.example` with comments for every var
- [ ] Contains: `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_HOST=postgres`, `POSTGRES_PORT=5432`, `DATABASE_URL=postgresql+asyncpg://user:pass@postgres:5432/db`, `API_PORT=8000`, `WEB_PORT=3000`, `JWT_SECRET=change-me`, `CORS_ORIGINS=http://localhost:3000`, `NEXT_PUBLIC_API_URL=http://localhost:8000`
- [ ] `.env` is in `.gitignore` (and `.dockerignore` not copying it)
- [ ] Fresh clone validates: `cp infra/.env.example infra/.env && docker compose -f infra/docker-compose.yml config` succeeds
- [ ] `services/api/core/config.py` + `apps/web` docs reference these exact names (no hardcoded `localhost:8000` drift)

## Dependencies
Blocked by: M0-1 (skeleton)
Blocks: M0-9, M0-14, M0-15, M0-17, M0-21, M0-27
Related: docs/API_CONTRACT.md, docs/ONBOARDING.md

## Notes
- Compose at `infra/docker-compose.yml` must use `env_file: ../infra/.env` or `env_file: .env` relative to compose file — test on Windows (CRLF) and Linux (LF).
- Leave commented `# REDIS_URL=redis://redis:6379/0  # post-MVP M4` for future uncomment.
```

</details>

<details>
<summary>M0-14 — Initialize FastAPI project structure (with tooling pins)</summary>

```
---
name: Task
about: M0-14 — FastAPI scaffold
title: "M0-14: Initialize FastAPI project structure + toolchain pins"
labels: [area:api]
assignees: hana
---

## Area
api

## Milestone
M0 Scaffolding

## Description
Set up the base FastAPI project inside `services/api`: `main.py` entrypoint,
`routers/` for endpoint modules, `models/` for DB models, `schemas/` for
Pydantic request/response schemas, `core/config.py` for settings. No business
logic yet beyond structure — this is where `/health` (M0-16) and later feature
work will live. Pin toolchains so `docker compose up` and local `uvicorn` use
same versions.

## Acceptance criteria
- [ ] Folder structure `services/api/{main.py,routers/__init__.py,models/__init__.py,schemas/__init__.py,core/config.py}` exists
- [ ] `pyproject.toml` pins `fastapi`, `uvicorn[standard]`, `sqlalchemy[asyncio]`, `asyncpg`, `alembic`, `pydantic-settings`, `python-jose[cryptography]`, `passlib[bcrypt]`, `ruff`, `black`
- [ ] `.python-version` is `3.11.8` (and `python --version` matches in `verify-setup`)
- [ ] `ruff check` + `black --check` pass on `services/api` (pre-commit hook configured in M0-29)
- [ ] `services/api/README.md` explains `uv sync && uvicorn main:app --reload --port 8000`
- [ ] `alembic` not yet initialized here — that is M0-18

## Dependencies
Blocked by: M0-9 (skeleton pushed), M0-8 (.env contract)
Blocks: M0-15, M0-16, M0-18
Related: docs/ARCHITECTURE.md#Backend, infra/.env.example

## Notes
- Use `asyncpg` not `psycopg2` — matches `DATABASE_URL=postgresql+asyncpg://`.
- `core/config.py` must use `pydantic-settings` `BaseSettings` with `env_file="../infra/.env"` fallback for local dev.
```

</details>

<details>
<summary>M0-21 — Initialize Next.js project (with mock health)</summary>

```
---
name: Task
about: M0-21 — Next.js scaffold
title: "M0-21: Initialize Next.js project"
labels: [area:web]
assignees: adel
---

## Area
web

## Milestone
M0 Scaffolding

## Description
Scaffold `apps/web` with Next.js (App Router, TypeScript). No real pages yet
beyond layout shell (M0-22) and health placeholder (M0-23) — this just needs to
run and be ready for the `/health` check page. Decide Tailwind vs CSS Modules
now and document in `apps/web/README.md`.

## Acceptance criteria
- [ ] `create-next-app` with TypeScript + App Router + ESLint + Prettier + Tailwind (decision logged in README)
- [ ] `.nvmrc` is `20`, `npm ci` reproducible (or `pnpm` — choose one, document it, don't mix)
- [ ] Folder follows App Router conventions (`app/layout.tsx`, `app/page.tsx`, `lib/api.ts`)
- [ ] `.env.local.example` documents `NEXT_PUBLIC_API_URL=http://localhost:8000`
- [ ] `npm run lint` passes; `npm run dev` serves locally without errors
- [ ] `apps/web/README.md` explains `npm ci && npm run dev` and `NEXT_PUBLIC_API_URL` env

## Dependencies
Blocked by: M0-9 (skeleton pushed)
Blocks: M0-22, M0-23
Related: M0-8 (.env contract), M0-16 (real /health), docs/ARCHITECTURE.md#Frontend

## Notes
- Client component must `fetch(${process.env.NEXT_PUBLIC_API_URL}/api/v1/health)` — not server `fetch` via Route Handler (would hide CORS). See M0-24.
- Keep `M0-23` mock in `lib/api.ts` so this task can close before `M0-16` merges.
```

</details>

---

## Risks specific to M0 — expanded with mitigations

| # | Risk | Likelihood | Impact | Mitigation (owner) |
|---|---|---|---|---|
| 1 | **Phase 1 bottleneck if >1 person pushes skeleton** | High | Blocks all | Single-owner (Leader) until M0-9 merged; `M0_IMPLEMENTATION_PLAN.md:38` preserved. |
| 2 | **Schema bikeshedding in M0-18** | High | 2-4 day slip | 48h timebox, Leader tie-break; unresolved → `PENDING_REVIEW` extended in M1 (`docs/M0_IMPLEMENTATION_PLAN.md:194-197` preserved) |
| 3 | **Docker containerizing too early** | High | Debug hell | Gate Phase 4 on standalone success (`STARTING_PLAN.md:204-215`); `M0_IMPLEMENTATION_PLAN.md:198-200` preserved |
| 4 | **Bus factor =1 on Leader** | High | M0 stalls | Leader is only `Admin`/bypass holder (M0-10); members are `Write` and cannot be deputy Admin. Mitigate via GitHub Organization team containing only leader for required approval, plus documented recovery via `CONTRIBUTING.md` — not by granting extra Admin. |
| 5 | **Review latency stalls critical path** | High | 2-4 day slip | 24h SLA (`PROJECT_CONTEXT.md:247-248`), reassign rule on `#standup`; `M0-20`/`M0-25` now estimate 1 day incl. latency |
| 6 | **Windows/WSL + low-RAM env drift** | High | Batch onboarding fails | `scripts/verify-setup.sh`, OS matrix in `docs/ONBOARDING.md`, pilot Day 4 (M0-30), `M0-28` buffer 2hr |
| 7 | **Merge conflict on `infra/.env.example`/`docker-compose.yml`** | Medium | Day 7 rework | Single infra owner (Leader) + env names published Day 2 in `#standup`; PR must touch `.env.example` first |
| 8 | **Idle → disengagement (5/8 idle in original plan)** | High | M1 cold start | Board Day 1, all 8 have Day 2 work (R1 fix): CV reviewers on schema, Huda on layout, Ahmed/Moatasem on CI/verify |
| 9 | **No CI catches lint/env pre-merge** | Medium | 400 errors by M2 | M0-29 minimal CI + `Require status checks` (M0-10) |
| 10 | **`.env`/CORS drift between tracks** | Medium | `M0-28` fails late | `M0-8` Day 1 contract + `M0-24` browser verification + `M0-19` shared types |
| 11 | **Defense date TBD compresses timeline** | Medium | M0 eats 20% runway | Backward plan: M0 due = D-14w; if D<12w compress to 7 days (cut `M0-22` polish) |
| 12 | **No `ARCHITECTURE.md` → examiner fails docs** | Medium | Graduation risk | P0 `M0-4` stub + DoD gate requiring CV+Full-Stack review |

---

## Exit checklist (copy into the M0 GitHub Milestone description)

- [ ] All Definition of Done items above are checked (including `alembic current==head`, `packages/shared` types, `infra/.env.example` validates)
- [ ] `docker compose -f infra/docker-compose.yml down -v && up --build` reproduces clean on 2 OSes (Windows + Linux/Mac)
- [ ] `docs/PROGRESS_LOG.md` has dated Sprint 1 entry (done / in-progress / blocked / decisions + onboarding friction log)
- [ ] `docs/ARCHITECTURE.md` v0 reviewed by 1 CV + 1 Full-Stack member
- [ ] `docs/supervisor-log.md` has M0 summary ready to paste to instructor
- [ ] `docs/ONBOARDING.md` troubleshooting section updated from `M0-33` fixes
- [ ] Ruleset on `main` shows green: restrict direct pushes/updates ✓, restrict deletions ✓, block force pushes ✓, require PR + 1 leader approval + dismiss stale + require conversation resolution ✓, require status checks (lint) + require branches up-to-date ✓, bypass only leader (For pull requests only) ✓, members `Write` not `Admin` ✓
- [ ] Board has `M0` closed and `M1` issues drafted, tagged to `M1` milestone, `docs/API_CONTRACT.md` frozen
- [ ] Retro held (30 min) — board cleanup: any `In Progress` >3 days broken down or re-scoped

---

## Appendix — What changed vs. original plan (for reviewers)

- **Merged feedback from 3 critics (technical, process, completeness).**
- **DoD fixed:** restored dropped `STARTING_PLAN.md:219-231` items (branch convention, API contract, CV scaffolds via `.gitkeep` + spike) and added migrated DB, shared types, env validation, CI, architecture/onboarding docs.
- **Dependencies corrected:** `M0-8` (`.env.example`) moved to Phase 1 Day 1; `M0-10→M0-12` inversion fixed; `CORS` moved to backend `M0-16`; Dockerfiles `M0-26` explicit; board `M0-11/12/13` moved to Day 1.
- **Estimates honest:** `M0-14 1hr→2hr`, `M0-18 1.5hr→2.5hr`, `M0-21 30min→1hr`, `M0-27 1.5hr→2.5hr`, `M0-31 15min→45min+4hr timebox`, `M0-20/25 —→1 day incl. review`, added 3-day buffer.
- **Utilization fixed:** No one idle — Huda (board+layout), Seif/Jana (schema reviewers + spike), Ahmed/Moatasem (milestones+CI+verify) all have Day 2 work.
- **Onboarding hardened:** `M0-30` pilot Day 4, OS matrix, `scripts/verify-setup`, staggered PRs, 2hr timebox + triage owners.
- **Filenames fixed:** `StartingPlan.md` → `STARTING_PLAN.md`; compose path `infra/docker-compose.yml` with `-f` flag and `make up` wrapper.

