# Board — exam-integrity-system (M0)

> Local mirror of GitHub Projects board. GitHub Milestones + Issues are the source of truth; this file is a static snapshot for offline review. Use `https://github.com/sayfeldinn/exam-integrity-system/issues` filtered by `milestone:"M0 - Repo and Scaffolding"`.

**Board:** `https://github.com/sayfeldinn/exam-integrity-system/projects`

| Column | WIP | Issues (M0 milestone `1`, 14 open) |
|---|---|---|
| **Backlog** | ∞ | `#9` `M0-22` `area:web` layout shell · `#10` `M0-23` `area:web` /health page · `#11` `M0-24` `area:web` CORS verify · `#12` `M0-25` `area:web` PR Phase 3 · `#13` `M0-26` `area:infra` Dockerfiles · `#14` `M0-27` `area:infra` docker-compose · `#15` `M0-28` `area:infra` verify 2 OSes · `#16` `M0-29` `area:infra` lint/CI · `#17` `M0-30` `area:infra` pilot onboarding · `#18` `M0-31` `area:infra` full clones · `#19` `M0-32` `area:infra` test PRs · `#20` `M0-33` `area:infra` fix env · `#21` `M0-34` `area:infra` retro |
| **This Sprint** `M0:119` ≤8 | seeded per `BOARD_SETUP.md:32-35` | `#8` `M0-21` `area:web` `Adel` Next.js |
| **In Progress** | ≤4 | *(empty — move here when dev starts, 1 per person `M0:76-79`)* |
| **In Review (PR open)** | ≤4 | *(empty — PR opened `feat/<member>/...` per `CONTRIBUTING.md:1`, needs 1 sayfeldinn approval `CONTRIBUTING.md:3`)* |
| **Done** | ∞ | `M0-1..M0-13` setup tasks · `M0-14` FastAPI scaffold · `M0-15` settings · `M0-16` health+CORS · `M0-17` asyncpg · `M0-18` core tables + Alembic · `M0-19` freeze contract + `packages/shared` · `M0-20` PR Phase 2 leader review — all merged to `main` |

## Milestone `M0 - Repo and Scaffolding` (`1`, 14 open)

| # | Issue | Area | Status | Depends |
|---|---|---|---|---|
| 1 | `M0-14` Initialize FastAPI `services/api` | `area:api` | Done | `M0-9,M0-8` |
| 2 | `M0-15` `core/config.py` `pydantic-settings` | `area:api` | Done | `M0-14,M0-8` |
| 3 | `M0-16` `GET /api/v1/health` + `CORSMiddleware` | `area:api` | Done | `M0-14` |
| 4 | `M0-17` Postgres `asyncpg` | `area:api` | Done | `M0-15` |
| 5 | `M0-18` tables + Alembic | `area:api` | Done | `M0-17` |
| 6 | `M0-19` freeze `docs/API_CONTRACT.md` + `packages/shared` | `area:api` | Done | `M0-18` |
| 7 | `M0-20` PR Phase 2 | `area:api` | Done | `M0-16,18,19` |
| 8 | `M0-21` Initialize Next.js `apps/web` | `area:web` | This Sprint | `M0-9` |
| 9 | `M0-22` layout shell | `area:web` | Backlog | `M0-21` |
| 10 | `M0-23` `/health` page | `area:web` | Backlog | `M0-21,16` |
| 11 | `M0-24` CORS verify | `area:web` | Backlog | `M0-23,16` |
| 12 | `M0-25` PR Phase 3 | `area:web` | Backlog | `M0-23,24` |
| 13 | `M0-26` Dockerfiles | `area:infra` | Backlog | `M0-20,25` |
| 14 | `M0-27` `infra/docker-compose.yml` | `area:infra` | Backlog | `M0-26,8` |
| 15 | `M0-28` verify `compose up` 2 OSes | `area:infra` | Backlog | `M0-27` |
| 16 | `M0-29` lint/CI `ci.yml` | `area:infra` | Backlog | `M0-14,21,10` |
| 17 | `M0-30` pilot onboarding Day4 | `area:infra` | Backlog | `M0-20` |
| 18 | `M0-31` full clones (8) | `area:infra` | Backlog | `M0-28` |
| 19 | `M0-32` test PRs Ruleset | `area:infra` | Backlog | `M0-10,29` |
| 20 | `M0-33` fix env | `area:infra` | Backlog | `M0-31` |
| 21 | `M0-34` retro + planning | `area:infra` | Backlog | `M0-28,31` |

`M0-14` through `M0-20` are `closed` — merged to `main` via PRs `#24` `#27` `#28` `#31` `#36` `#38`. Remaining 14 are `open`, labeled `milestone:M0` + `area:*`.

## How to use

- **New joiner:** `M0-21` is `This Sprint` — pick it up or grab from `Backlog`.
- **Daily:** async `#standup` per `docs/PROJECT_CONTEXT.md:244` (what moved/does/blocked); **Wed/Thu** 15-min sync `docs/PROJECT_CONTEXT.md:246`.
- **PR:** `feat/<member>/<desc>` per `CONTRIBUTING.md:1` → resolve conversations → **sayfeldinn approves** `CONTRIBUTING.md:3` (only `Admin` can bypass `For pull requests only`) → squash-merge → issue auto-closes via `Closes #N`.
- **Done:** `PROGRESS_LOG.md:11` + `supervisor-log.md` `M0-34` `M0:182` `Exit` `M0:349-360` `alembic current==head` `docker compose -f infra/docker-compose.yml down -v && up --build` 2 OSes.

## Links

- Milestones: `https://github.com/sayfeldinn/exam-integrity-system/milestones` (7)
- Issues: `https://github.com/sayfeldinn/exam-integrity-system/issues?q=milestone%3A%22M0+-+Repo+and+Scaffolding%22` (21)
- Labels: `https://github.com/sayfeldinn/exam-integrity-system/labels` (19)
- Board: `https://github.com/sayfeldinn/exam-integrity-system/projects`
- Setup runbook: `BOARD_SETUP.md:13-28` (manual Projects + `Settings → Tags` `v*`).

---

*Source: `docs/milestones/M0_IMPLEMENTATION_PLAN.md:99-182` `M0-14..M0-34`. Phase 1 `M0-1..M0-13` **COMPLETE** — see `docs/PROGRESS_LOG.md` Sprint 1. Phase 2 `M0-14..M0-20` **COMPLETE** — merged to `main` via PRs `#24` `#27` `#28` `#31` `#36` `#38`. Research spikes in `research/` (face_recognition, face_monitor) validated and review-fixed. Snapshot at `v0.0.2`.*
