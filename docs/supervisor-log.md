# Supervisor Log — exam-integrity-system

> Updated per sprint retro (see `docs/PROGRESS_LOG.md` + `docs/PROJECT_CONTEXT.md:8` cadence).
> This file is the paste-ready summary for instructor updates.

---

## M0 — Repo & Scaffolding (2026-09-02 – ongoing) — Phase 1 COMPLETE, Phase 2 COMPLETE

**Status:** Phase 1 (`M0-1..M0-13`) **complete**. Phase 2 (`M0-14..M0-20`) **complete** — merged to `main` via PRs `#24` `#27` `#28` `#31` `#36` `#38`. Research spikes validated and review-fixed. `v0.0.2` tag at `3d5c2cf`.

**Done — Phase 1 (2026-09-02):**
- Folder skeleton `M0-1` + `README.md` `M0-2` + `.gitignore`/`.dockerignore`/`.editorconfig`/`.nvmrc`/`python-version` `M0-3` + `docs/` stubs `M0-4` — `dcad3a0` `v0.0.0`
- `CONTRIBUTING.md` `M0-5` + `LICENSE`/`CODEOWNERS` `M0-6` + `.github/ISSUE_TEMPLATE.md` `M0-7` + `infra/.env.example` `M0-8` — `dcad3a0`
- Ruleset active targeting `main` `M0-10` — restrict pushes/deletions, block force pushes, require PR + 1 sayfeldinn approval + dismiss stale + conversation resolution + status checks, bypass only Admin `For pull requests only`, members `Write`
- Board infra via API `M0-11..13`: milestones `M0–M6` (7), labels `area:*` (19 total), issues `M0-14..M0-34` (21) — `2026-09-03`; board UI + tag protection `v*` documented `BOARD_SETUP.md` + snapshot `BOARD.md`
- Tags: `v0.0.0` (`dcad3a0` skeleton), `v0.0.1` (`892a103` Phase 1 complete)

**Done — Phase 2 (2026-09-03–2026-09-09):**
- `M0-14` FastAPI scaffold + toolpins — `feat/hana/api-scaffold` `PR#24` merged
- `M0-15` `core/config.py` pydantic-settings — `feat/hana/api-scaffold` `PR#24`
- `M0-16` `GET /api/v1/health` + `CORSMiddleware` — `PR#24`
- `M0-17` Postgres `asyncpg` — `feat/sayfeldinn/asyncpg-setup` `PR#31` merged; `fix/sayfeldinn/m0-17-review` fixes applied
- `M0-18` core tables + Alembic — `feat/moatasem/m0-18-db-tables` `PR#27` merged; `fix/sayfeldinn/m0-18-review` removes hardcoded creds, reads `DATABASE_URL` from settings
- `M0-19` freeze `docs/API_CONTRACT.md` + `packages/shared` — `feat/sayfeldinn/m0-19-freeze-contract` `PR#37` merged to develop, `PR#38` to main
- `M0-20` PR Phase 2 leader review gate — closed, issues `#5` `#6` `#7` closed
- Research spikes validated: `face_recognition` review-fixed (8 files, `fix/sayfeldinn/face-recognition-review` `PR#43` merged), `face_monitor` superseded

**In progress / next:**
- `M0-21` `feat/adel/web-scaffold` `M0:149-153` Next.js `App Router` + `NEXT_PUBLIC_API_URL` browser fetch — `This Sprint`
- `M0-22..M0-25` frontend continuation — `Backlog`
- `M0-26/27` Dockerfiles + `infra/docker-compose.yml` `M0:165-166` after `M0-25` PR merges
- Research → services graduation: `face_recognition` to `services/cv-identity` when production-ready

**Decisions:**
- `M0` canonical over `STARTING_PLAN` pointer model — `M0` wins if conflict
- Compose path `infra/docker-compose.yml` via `docker compose -f`
- Milestones subfolder `docs/milestones/`
- Empty scaffold dirs kept via `.gitkeep` until service starts
- Tagging `v{MAJOR}.{MINOR}.{PATCH}` — `Admin`-only via tag protection pattern `v*`
- Research convention: features start in `research/`, graduate to `services/` when production-ready

---

<!-- Add new entries above this line, newest on top -->
