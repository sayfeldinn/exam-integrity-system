# Supervisor Log — exam-integrity-system

> Updated per sprint retro (see `docs/PROGRESS_LOG.md` + `docs/PROJECT_CONTEXT.md:8` cadence).
> This file is the paste-ready summary for instructor updates.

---

## M0 — Repo & Scaffolding (2026-09-03 – [end date])

**Status:** in progress (Phase 1 Day 1)

**Done:**
- Branch Ruleset active targeting `main` — restrict pushes/deletions, block force pushes, require PR + 1 leader approval + dismiss stale + conversation resolution, bypass only leader `For pull requests only` (`M0-10` `M0:116`)
- Folder skeleton with `.gitkeep` placeholders (`M0-1` `M0:107`)
- `README.md` + `.gitignore`/`.dockerignore`/`.editorconfig` + `.nvmrc`/`.python-version` (`M0-2..M0-3`)
- `docs/ARCHITECTURE.md` v0 stub + `docs/API_CONTRACT.md` freeze + `docs/ONBOARDING.md` + this log (`M0-4`)

**In progress / next:**
- `CONTRIBUTING.md` + `CODEOWNERS`/`LICENSE` (`M0-5..M0-6`)
- `infra/.env.example` canonical 10 vars (`M0-8`)

**Decisions:**
- `M0` canonical over `STARTING_PLAN` pointer model (`docs/STARTING_PLAN.md:3`)
- Compose path `infra/docker-compose.yml` via `docker compose -f` (not root)

---

<!-- Add new entries above this line, newest on top -->
