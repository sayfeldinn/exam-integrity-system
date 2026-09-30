# Progress Log

> Filled in every Sunday at the sprint retro (see `PROJECT_CONTEXT.md`
> Section 8 — weekly leadership cadence). Newest entry on top. Keep entries
> short — a few bullets, not essays. This is what gets pasted into instructor
> status updates and what future-you searches when someone asks "why did we
> drop X."

---

## Sprint 2 — 2026-09-03 – 2026-09-09

**Milestone:** M0 — Repo & Scaffolding (Phase 2 Complete + Research Validation)

- Done:
  - Phase 2 (`M0-14..M0-20`) merged to `main` via PRs `#24` `#27` `#28` `#31` `#36` `#38`:
    - `M0-14` FastAPI scaffold + `M0-15` pydantic-settings + `M0-16` health+CORS (`feat/hana/api-scaffold` `PR#24`)
    - `M0-17` asyncpg (`feat/sayfeldinn/asyncpg-setup` `PR#31`) — review fixes: lifespan handler, return type, Arabic comments, pool_pre_ping
    - `M0-18` core tables + Alembic (`feat/moatasem/m0-18-db-tables` `PR#27`) — review fixes: removed hardcoded credentials from `alembic.ini`, `env.py` reads `DATABASE_URL` from settings
    - `M0-19` freeze `docs/API_CONTRACT.md` + `packages/shared` (`feat/sayfeldinn/m0-19-freeze-contract` `PR#37` `PR#38`)
    - `M0-20` PR Phase 2 leader review gate — closed
  - Issues closed: `#3` (M0-16), `#4` (M0-17), `#5` (M0-18), `#6` (M0-19), `#7` (M0-20)
  - Research folder created (`research/README.md`) with convention docs
  - `face_recognition` moved from `services/` to `research/` (`feat/jana/face-recognition` `PR#41` merged to develop)
  - `face_monitor` moved from `services/` to `research/` (`feat/jana/face-detection` `PR#42` merged to develop)
  - `face_recognition` review-fixed (8 files) — `fix/sayfeldinn/face-recognition-review` `PR#43` merged; fixes: lazy-load insightface, CPU default, shared `cosine_similarity()`, threshold unified, `enroll_live.py` deleted, `LargeBinary` for embeddings, `numpy<2`, `SQLAlchemy<3`
  - Tag cleanup: deleted stale tags (`v0.0.2-4`, `phase1-complete`, `v0.0.1`), reorganized to `v0.0.0` (skeleton), `v0.0.1` (Phase 1), `v0.0.2` (current main `3d5c2cf`)
  - Docs audit: BOARD.md reconciled, supervisor-log + PROGRESS_LOG updated, root README tree corrected, research/ added to CODEOWNERS, CONTRIBUTING.md, ARCHITECTURE.md, PROJECT_CONTEXT.md
- In progress / carried over:
  - `M0-21` Next.js init `feat/adel/web-scaffold` — `This Sprint`
  - Manual Projects board creation (`M0-11`) — `Huda` 1-min at `https://github.com/sayfeldinn/exam-integrity-system/projects`
  - Manual tag protection `v*` (`Settings → Tags`)
- Blocked:
  - Projects V2 creation via API — token lacks `project` scope; requires manual UI or token with `project` scope
- Decisions made this sprint:
  - Research convention: features start in `research/`, graduate to `services/` when production-ready. Naming: `research/<feature-name>/` (no member names)
  - All tags use `v` prefix — `v0.0.x` internal checkpoints, `v0.1.0`=M0, up to `v1.0.0`=M6
  - Owner column removed from M0_IMPLEMENTATION_PLAN.md tables
  - Never push directly to someone else's feature branch — use separate fix branches

## Sprint 1 — 2026-09-02 – 2026-09-03

**Milestone:** M0 — Repo & Scaffolding (Phase 1 — Repo Foundation)

- Done:
  - Repo skeleton pushed to `main` (`M0-1..M0-9`) — Section 7 tree + `.gitkeep`, `README.md`, `.gitignore`/`.dockerignore`/`.editorconfig`/`.nvmrc`/`python-version`, `docs/` stubs, `CONTRIBUTING.md`, `LICENSE`+`CODEOWNERS`, `.github/ISSUE_TEMPLATE.md`, `infra/.env.example` — commits `dcad3a0` `v0.0.0` + `892a103` `v0.0.1`
  - Ruleset active targeting `main` (`M0-10`) — restrict pushes/deletions, block force pushes, require PR + 1 sayfeldinn approval + dismiss stale + conversation resolution + status checks, bypass only Admin `For pull requests only`, members `Write`
  - Board infra via API (`M0-11..13`): milestones `M0–M6` (7), labels `area:*` (19 total), issues `M0-14..M0-34` (21); board UI + tag protection `v*` documented in `BOARD_SETUP.md` + snapshot `BOARD.md`
  - Branch workflow `CONTRIBUTING.md` — `<type>/<member-name>/<desc>` + workflow + permissions
  - Tagging convention `v{MAJOR}.{MINOR}.{PATCH}` — `Admin`-only via tag protection pattern `v*`
  - Docs structure refactor `docs/milestones/` + thin pointer `docs/STARTING_PLAN.md`
- In progress / carried over:
  - Manual Projects board creation (`M0-11`) — `Huda` 1-min
  - Manual tag protection `v*` — `sayfeldinn` 1-min
  - Milestone `due_on` dates for `M0–M6` — TBD until defense date `D`
  - Issue assignees — `21` issues have `Area`+`Milestone` but `assignees []`
- Blocked:
  - Projects V2 creation via API — token lacks `project` scope
  - Tag protection via API — manual UI required
- Decisions made this sprint:
  - Thin pointer model `docs/STARTING_PLAN.md:3` (`M0` canonical, `M0` wins if conflict)
  - Milestones subfolder `docs/milestones/`
  - Empty scaffold dirs kept via `.gitkeep` until service starts
  - Tagging convention `v{MAJOR}.{MINOR}.{PATCH}` — `Admin`-only via tag protection

---

<!-- Add new entries above this line, newest on top -->
