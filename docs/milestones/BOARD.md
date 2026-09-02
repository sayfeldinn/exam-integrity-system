# Board — exam-integrity-system (M0)

> Local mirror of GitHub Projects board `M0-11` `docs/milestones/M0_IMPLEMENTATION_PLAN.md:117`. GitHub Milestones + Issues are the source of truth (`docs/PROJECT_CONTEXT.md:190-192` — auto-updates on PR merge); this file is a static snapshot for offline review and for `M0-13` verification (`M0:119`). Until the Projects V2 board is created via UI (token `INSUFFICIENT_SCOPES` `project`, see `BOARD_SETUP.md:3`), use this table + `https://github.com/sayfeldinn/exam-integrity-system/issues` filtered by `milestone:"M0 - Repo and Scaffolding"`.

**Board:** `https://github.com/sayfeldinn/exam-integrity-system/projects` → `exam-integrity-system Board` (manual, see `BOARD_SETUP.md:13-28`).

| Column | WIP | Issues (M0 milestone `1`, 21 open) |
|---|---|---|
| **Backlog** | ∞ | `#14` `M0-27` `area:infra` `M0:166` docker-compose · `#15` `M0-28` verify 2 OSes · `#13` `M0-26` Dockerfiles · `#11` `M0-24` CORS · `#10` `M0-23` /health page · `#9` `M0-22` layout shell · `#7` `M0-20` PR Phase2 · `#6` `M0-19` freeze contract · `#5` `M0-18` Alembic · `#4` `M0-17` asyncpg · `#3` `M0-16` /health+CORS · `#2` `M0-15` settings · (others per `#1-21`) |
| **This Sprint** `M0:119` ≤8 | seeded per `BOARD_SETUP.md:32-35` | `#1` `M0-14` `area:api` `Hana` `M0:131` FastAPI project · `#8` `M0-21` `area:web` `Adel` `M0:149` Next.js |
| **In Progress** | ≤4 | *(empty — move here when dev starts, 1 per person `M0:76-79`)* |
| **In Review (PR open)** | ≤4 | *(empty — PR opened `feat/<member>/...` per `CONTRIBUTING.md:1`, needs 1 leader approval `CONTRIBUTING.md:3`)* |
| **Done** | ∞ | `M0-1..M0-13` setup tasks (skeleton `M0:107`, `README` `M0:108`, `docs` `M0:110`, `CONTRIBUTING` `M0:111`, `CODEOWNERS` `M0:112`, `ISSUE_TEMPLATE` `M0:113`, `infra/.env.example` `M0:114` `M0-9` `dcad3a0` `v0.0.1`, Ruleset `M0-10` `CONTRIBUTING.md:2`, board checklist `f15a28c` `v0.0.3`, milestones `1–7` + labels `19` + issues `21` created via API `2026-09-03`) |

## Milestone `M0 - Repo and Scaffolding` (`1`, 21 open)

| # | Issue | Area | Owner `M0` | Depends |
|---|---|---|---|---|
| 1 | `M0-14` Initialize FastAPI `services/api` `M0:131` | `area:api` | Hana | `M0-9,M0-8` |
| 2 | `M0-15` `core/config.py` `pydantic-settings` `M0:132` | `area:api` | Hana | `M0-14,M0-8` |
| 3 | `M0-16` `GET /api/v1/health` + `CORSMiddleware` `M0:133` | `area:api` | Hana | `M0-14` |
| 4 | `M0-17` Postgres `asyncpg` `M0:134` | `area:api` | Rodaina | `M0-15` |
| 5 | `M0-18` tables + Alembic `M0:135` | `area:api` | Rodaina (Seif+Jana advisory, Leader approves) | `M0-17` |
| 6 | `M0-19` freeze `docs/API_CONTRACT.md` + `packages/shared` `M0:136` | `area:api` | Rodaina+Seif/Jana | `M0-18` |
| 7 | `M0-20` PR Phase 2 `M0:137` | `area:api` | Hana/Rodaina | `M0-16,18,19` |
| 8 | `M0-21` Initialize Next.js `apps/web` `M0:149` | `area:web` | Adel | `M0-9` |
| 9 | `M0-22` layout shell `M0:150` | `area:web` | Adel+Huda | `M0-21` |
| 10 | `M0-23` `/health` page `M0:151` | `area:web` | Adel | `M0-21,16` |
| 11 | `M0-24` CORS verify `M0:152` | `area:web` | Adel+Rodaina | `M0-23,16` |
| 12 | `M0-25` PR Phase 3 `M0:153` | `area:web` | Adel/Huda | `M0-23,24` |
| 13 | `M0-26` Dockerfiles `M0:165` | `area:infra` | Leader+Hana | `M0-20,25` |
| 14 | `M0-27` `infra/docker-compose.yml` `M0:166` | `area:infra` | Leader+Hana | `M0-26,8` |
| 15 | `M0-28` verify `compose up` 2 OSes `M0:167` | `area:infra` | Adel+Moatasem | `M0-27` |
| 16 | `M0-29` lint/CI `ci.yml` `M0:168` | `area:infra` | Ahmed | `M0-14,21,10` |
| 17 | `M0-30` pilot onboarding Day4 `M0:177` | `area:infra` | 2 volunteers | `M0-20` |
| 18 | `M0-31` full clones (8) `M0:178` | `area:infra` | All 8 | `M0-28` |
| 19 | `M0-32` test PRs Ruleset `M0:180` | `area:infra` | All 8 | `M0-10,29` |
| 20 | `M0-33` fix env `M0:181` | `area:infra` | Hana/Adel | `M0-31` |
| 21 | `M0-34` retro + planning `M0:182` | `area:infra` | Leader | `M0-28,31` |

All 21 are `milestone:1` `open`, labeled `milestone:M0` + `area:*` per `POST /issues` `2026-09-03` (`gh api` check: `21 total` `21 open` `f15a28c` `v0.0.3`).

## How to use

- **New joiner:** `M0-14` and `M0-21` are `This Sprint` — claim one per `M0:121` (`Hana`/`Adel` seeded, you claim next in your track, not top-down).
- **Daily:** async `#standup` per `docs/PROJECT_CONTEXT.md:244` (what moved/does/blocked); **Wed/Thu** 15-min sync `docs/PROJECT_CONTEXT.md:246`.
- **PR:** `feat/<member>/<desc>` per `CONTRIBUTING.md:1` → resolve conversations → **Leader approves** `CONTRIBUTING.md:3` (only `Admin` can bypass `For pull requests only`) → squash-merge → issue auto-closes via `Closes #N`.
- **Done:** `PROGRESS_LOG.md:11` + `supervisor-log.md` `M0-34` `M0:182` `Exit` `M0:349-360` `alembic current==head` `docker compose -f infra/docker-compose.yml down -v && up --build` 2 OSes.

## Links

- Milestones: `https://github.com/sayfeldinn/exam-integrity-system/milestones` (7)
- Issues: `https://github.com/sayfeldinn/exam-integrity-system/issues?q=milestone%3A%22M0+-+Repo+and+Scaffolding%22` (21)
- Labels: `https://github.com/sayfeldinn/exam-integrity-system/labels` (19)
- Board (when created): `https://github.com/sayfeldinn/exam-integrity-system/projects` → `exam-integrity-system Board`
- Setup runbook: `BOARD_SETUP.md:13-28` (manual Projects + `Settings → Tags` `v*`/`m*`).

---

*Source: `docs/milestones/M0_IMPLEMENTATION_PLAN.md:99-182` `M0-11..M0-34`; snapshot at `1858f1b` `v0.0.4` `2026-09-03` → now `phase1-complete` Phase 1 done; update when `M0-14`/`M0-21` PRs open (`In Progress` → `In Review`). Phase 1 `M0-1..M0-13` **COMPLETE** — see `docs/PROGRESS_LOG.md:11` Sprint 1 `2026-09-02–2026-09-03` and `docs/supervisor-log.md:8` M0 Phase 1 complete.*
