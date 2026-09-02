# Starting Plan — AI-Based Online Exam Integrity System

> **10-minute orientation.** Canonical execution spec is `docs/milestones/M0_IMPLEMENTATION_PLAN.md`
> (Definition of Done `M0:21-96`, Phases `M0:99-186`, Exit Check `M0:349-360`; see also `docs/milestones/README.md`).
> This file gives the **why and order** for 8 people; `M0` gives the **verifiable
> how, estimates, owners, and gates**. **If they conflict, `M0` wins.**
> Branch naming / Ruleset detail source of truth is `CONTRIBUTING.md` (branch) and `M0:57-60 / M0-10` (Ruleset enforcement).

> Purpose: the exact first steps to take the GitHub repo from empty to a
> working, cloneable skeleton that all 8 team members can build on without
> blocking each other. Follow this in order — later steps depend on earlier
> ones.

---

## Step 0 — Before touching Git

Agree as a team on:
- **Repo name:** `exam-integrity-system` (or your chosen alternative)
- **Branching convention:** `<type>/<member-name>/<short-description>` — **see
  `CONTRIBUTING.md:1` for the full spec** (types: `feat`, `fix`, `docs`,
  `refactor`, `test`, `chore`). Examples:
  - `feat/seif/agent-tool-calling`
  - `feat/ahmed/frontend`
  - `fix/sara/api-error-handling`
  - `docs/mohamed/project-documentation`
- **Who owns `main`:** repo admin (team leader) sets the **Ruleset targeting `main`**
  (Step 2 → `M0-10` `M0:116`) before anyone else pushes. Only the leader is `Admin`;
  all other members are `Write` (no bypass). See `CONTRIBUTING.md:2-3` and durable
  decision log `docs/PROJECT_CONTEXT.md:289-291`.

---

## Steps 1–6 — Execution pointers (see M0 for acceptance criteria)

Detailed acceptance, owners, estimates, dependencies, and verifiable gates live
in `M0`. Do not duplicate normative values here — follow the pointer.

| Step | What (narrative) | Canonical tasks & DoD in M0 | Why it matters |
|---|---|---|---|
| **Step 1 — Push the skeleton first** (`M0:33-36` structure only) | Create folder tree (Section 7), `README`, `.gitignore` + tool pins, `docs/` stubs, initial `git push -u origin main`. Git doesn't track empty folders — add `.gitkeep`/`README.md` in `apps/mobile-proctor`, `services/cv-identity`, etc. Do not scaffold full service code day one — only `services/api` + `apps/web` later (MVP focus). | `M0-1` skeleton `M0:107`, `M0-2` README `M0:108`, `M0-3` `.gitignore`/`.dockerignore`/`.editorconfig`/`.nvmrc`/`.python-version` `M0:109`, `M0-4` `docs/` (`ARCHITECTURE.md` v0 + `API_CONTRACT.md` + `ONBOARDING.md` + `supervisor-log`) `M0:110`, `M0-8` `infra/.env.example` **Day 1 contract** `M0:114` (10 vars: `POSTGRES_*`, `DATABASE_URL=postgresql+asyncpg://`, `JWT_SECRET`, `CORS_ORIGINS`, `NEXT_PUBLIC_API_URL`), `M0-9` initial push `M0:115` (sole direct-to-main exception). Tree is defined in `docs/PROJECT_CONTEXT.md:153-184`; health path is `GET /api/v1/health` + `/health` redirect per `M0-16` `M0:133` (not just `/health`). | Gives every teammate the same base to clone before any code diverges. `M0-8` early prevents `Step 3`/`Step 4` picking conflicting env names (former `M0-10→M0-12` inversion). |
| **Step 2 — Ruleset + workflow** | **Already configured.** `Settings → Rules → Rulesets → Active targeting `main``. Enable: restrict direct pushes/updates, restrict deletions, block force pushes, require PR, require **1 leader approval** (dismiss stale on push), require conversation resolution, plus status checks/branches up-to-date after `M0-29`. Bypass: only `Admin` (leader) can bypass, **For pull requests only**; members `Write` cannot bypass/modify. Workflow: `git checkout -b <type>/<member-name>/<desc>` → `push` → PR → resolve conversations → **leader approves** → squash-merge; **never push directly to `main` after Ruleset**. | `M0-10` `M0:116` (exact toggles), DoD `M0:59`, `M0-5` workflow in `CONTRIBUTING.md` `M0:111`, CODEOWNERS `M0-6` `M0:112` (`@<leader>` required), `M0-32` `M0:180` validates (non-admin push/deletion/conversation gates), Exit `M0:357`. Source of truth for branch spec: `CONTRIBUTING.md:1`. | With 8 people, one accidental force-push wipes work. Leader-only bypass prevents drift. |
| **Step 3 — Backend first** | Must come **before** CV/audio/frontend feature work — they depend on schema/auth. Scaffold FastAPI (`main.py`, `routers/`, `models/`, `schemas/`), **canonical** `GET /api/v1/health → {"status":"ok"}` (+ `/health` redirect), Postgres via `DATABASE_URL` from `infra/.env.example`, core tables **migrated via `alembic`** (not near-empty). Push before CV starts. | Phase 2 `docs/milestones/M0:125-140`: `M0-14` FastAPI+toolpins `M0:131` (2hr), `M0-15` `pydantic-settings` `M0:132`, `M0-16` health+CORS `M0:133`, `M0-17` `asyncpg` connection `M0:134`, `M0-18` `students/sessions/violations` with enums/CHECK/meta + `alembic init/upgrade/psql \dt` `M0:135` (2.5hr, CV advisory), `M0-19` freeze `docs/API_CONTRACT.md` + `packages/shared` `M0:136`, `M0-20` PR (48h timebox, 24h SLA, leader approves) `M0:137`. | Schema is the API contract; CV/frontend block without it. |
| **Step 4 — Frontend in parallel** | Can start parallel to Step 3 — needs only `NEXT_PUBLIC_API_URL`, not full schema. Scaffold Next.js (App Router), layout shell, placeholder page **client-side fetching** `NEXT_PUBLIC_API_URL/api/v1/health` with fallback UI. Proves `web → api` end-to-end before webcam/dashboard. | Phase 3 `docs/milestones/M0:142-156`: `M0-21` Next.js init `M0:149`, `M0-22` layout+tokens+mock `M0:150`, `M0-23` placeholder `M0:151` (works with mock Day 2, real API Day 4), `M0-24` **browser** CORS verify `M0:152` (not Route Handler proxy), `M0-25` PR `M0:153`. Parallel `Day 2-4` `M0:125`. | Catches CORS/env/networking on Day 2, not Week 6. Mock per `M0-22` avoids idling on `M0-16`. |
| **Step 5 — CV/audio/risk** | Only after API contract (`M0-19` frozen). Each specialist builds against stub/mock, improves accuracy after wiring. | Deferred to **M1-M4**; in M0 only `.gitkeep` placeholders `M0:107` + `M0-18` advisory review `M0:135` + optional spike `services/cv-identity/README fake {"face_found":true}` `M0:186`. Priority: `cv-identity` → `risk-engine` → `cv-objects`/`audio` (MVP order). Heavy deps (YOLO/MediaPipe) not containerized in M0 per `M0:186` & `M0:159`. See `docs/milestones/README.md` for M1–M4 index. | Keeps MVP focus; CV doesn't block M0. |
| **Step 6 — Compose** | Once `services/api` + `apps/web` + Postgres each run **standalone** — not before. One-command `docker compose -f infra/docker-compose.yml up --build` (root `docker compose up` fails — file lives in `infra/`). Includes `healthcheck: pg_isready`, `depends_on: service_healthy`, `pgdata` volume, `app_net` network; **defer** Redis/MinIO + heavy CV images to M4. | Phase 4 `docs/milestones/M0:159-168`: `M0-26` Dockerfiles `M0:165`, `M0-27` `infra/docker-compose.yml` wiring `M0:166` (2.5hr, commented `redis` stub), `M0-28` verify on **Windows + Mac** + `scripts/verify-setup.sh`/`OS matrix` `M0:167`, `M0-29` `ruff/black/eslint/prettier/pre-commit` + `ci.yml` + enable status checks `M0:168`. | Avoids manual per-machine installs; early containerizing of unstable CV deps slows iteration. |

---

## Quick Checklist → Canonical gates

This quick list is **non-normative**. M0 is done only when **all**
`docs/milestones/M0_IMPLEMENTATION_PLAN.md:21-96` (DoD) and `docs/milestones/M0_IMPLEMENTATION_PLAN.md:349-360`
(Exit Check) are green **on a fresh clone on 2 OSes**. See also
`CONTRIBUTING.md:1-4` for branch/workflow gates and `docs/milestones/README.md` for the milestone index.

- [ ] Folder skeleton + tool pins (`M0-1..M0-4`) → DoD `M0:28-31,52-56`
- [ ] Ruleset active targeting `main` with bypass/permissions (`M0-10` `M0:116`) → DoD `M0:59`
- [ ] Branch naming `<type>/<member-name>/<desc>` in `CONTRIBUTING.md` (`feat/fix/docs/refactor/test/chore`)
- [ ] `services/api` `GET /api/v1/health` + migrated schema (`M0-14..M0-19`) → DoD `M0:32,44-50`
- [ ] `apps/web` calling `/api/v1/health` via `NEXT_PUBLIC_API_URL` (`M0-21..M0-25`) → DoD `M0:35`
- [ ] `docs/API_CONTRACT.md` frozen + `packages/shared` (`M0-19`) → DoD `M0:67-71`
- [ ] `infra/docker-compose.yml` + Dockerfiles (`M0-26..M0-28`) → DoD `M0:38-43`
- [ ] CI gate `ruff/black/eslint/prettier/ci.yml` (`M0-29`) → DoD `M0:84-85`
- [ ] Onboarding + 8 clones + test PRs + retro (`M0-30..M0-34` `M0:172-183`) → DoD `M0:86-92`

If this list and `M0` disagree, **`M0` wins** — update this pointer, not `M0`.
