# Progress Log

> Filled in every Sunday at the sprint retro (see `PROJECT_CONTEXT.md`
> Section 8 — weekly leadership cadence). Newest entry on top. Keep entries
> short — a few bullets, not essays. This is what gets pasted into instructor
> status updates and what future-you searches when someone asks "why did we
> drop X."

---

## Sprint 1 — 2026-09-02 – 2026-09-03

**Milestone:** M0 — Repo & Scaffolding (Phase 1 Day 1 — Repo Foundation)

- Done:
  - Repo skeleton pushed to `main` (`M0-1..M0-9`) — Section 7 tree + `apps/web`/`services/api` `.gitkeep` until scaffold, other services `services/cv-*`/`audio`/`risk-engine`/`packages/shared` `.gitkeep`, `README.md`, `.gitignore`/`.dockerignore`/`.editorconfig`/`.nvmrc`/`python-version`, `docs/` (`ARCHITECTURE.md` v0, `API_CONTRACT.md`, `ONBOARDING.md`, `supervisor-log.md`), `CONTRIBUTING.md`, `LICENSE`+`CODEOWNERS`, `.github/ISSUE_TEMPLATE.md`, `infra/.env.example` 10-var contract — commits `dcad3a0` `v0.0.1` + `c7310bf` `v0.0.2` on `origin/main`
  - Ruleset active targeting `main` (`M0-10`) — restrict pushes/deletions, block force pushes, require PR + 1 leader approval + dismiss stale + conversation resolution + status checks/branches up-to-date, bypass only Admin `For pull requests only`, members `Write` — leader `sayfeldinn` only Admin
  - Board infra via API (`M0-11..13`): milestones `M0–M6` (7, `1:M0` 21 open), labels `area:*` (9 new, 19 total), issues `M0-14..M0-34` (21, `#1-21`, `milestone:1` `open`, labels `area:*`) — `gho_***` `repo` scope `2026-09-03`; board UI (`M0-11` Projects V2 `Backlog→Done` WIP `8/4/4` + fields `Area`/`Milestone`) + tag protection `v*`/`m*` (`Settings → Tags`) documented in `docs/milestones/BOARD_SETUP.md` + snapshot `BOARD.md` — auto token lacked `project` scope (`INSUFFICIENT_SCOPES`), manual 1-min Admin step remains but artifact committed `f15a28c` `v0.0.3` + `1858f1b` `v0.0.4`
  - Branch workflow `CONTRIBUTING.md:1` `<type>/<member-name>/<desc>` (`feat/fix/docs/refactor/test/chore`) + workflow `branch→push→PR→leader approval→squash-merge` + `Write` vs `Admin`
  - Tagging `v0.0.1` `dcad3a0` skeleton, `v0.0.2` `c7310bf` `.gitkeep`, `v0.0.3` `f15a28c` board setup, `v0.0.4` `1858f1b` board snapshot — `phase1-complete` reference to be tagged
  - Docs structure refactor `docs/milestones/` (`M0_IMPLEMENTATION_PLAN.md` + `README.md` index) + thin pointer `docs/STARTING_PLAN.md:3-7` (`M0` wins if conflict, `CONTRIBUTING.md` branch source)
- In progress / carried over:
  - Manual Projects board creation (`M0-11`) — `Huda` 1-min at `https://github.com/sayfeldinn/exam-integrity-system/projects` → `Backlog/This Sprint/In Progress/In Review/Done` + `Area`/`Milestone` fields + seed `21` issues (`This Sprint` `#1` `M0-14` `Hana` + `#8` `M0-21` `Adel`) — `BOARD_SETUP.md:13-35` checklist ready
  - Manual tag protection `v*`/`m*` (`Settings → Tags` or `Rulesets` `refs/tags/v*`/`m*`) — leader 1-min — `BOARD_SETUP.md:45-51`
  - Milestone `due_on` dates for `M0–M6` (`M0-12` `Ahmed` `M0 due = D-14w`, `D<12w` compress `7d` per `M0:80,118` + `docs/PROJECT_CONTEXT.md:222-235`) — TBD until defense date `D`
  - Issue assignees (`M0-13` `Moatasem+Ahmed`) — `21` issues have `Area`+`Milestone` but `assignees []` (GH handles for `Hana`, `Rodaina`, etc. not yet mapped); owners in `BOARD.md:16-41` + bodies are source of truth until handles known
- Blocked:
  - Projects V2 creation via API — token `gho_***` has `gist,repo,workflow` only, `createProjectV2` requires `project`+`read:project` (`INSUFFICIENT_SCOPES`); `gh auth status` not logged in — requires manual UI or token with `project` scope + `gh auth refresh -s project`
  - Tag protection via API — `404` old endpoint `POST /repos/.../tags/protection`, now `Rulesets` for tags (`refs/tags/v*`) — manual UI
- Decisions made this sprint:
  - Thin pointer model `docs/STARTING_PLAN.md:3-7` (`M0` canonical, `M0` wins if conflict)
  - Milestones subfolder `docs/milestones/` (`M0` + `README` index) — `B` migration `2026-09-03` (redirect `docs/M0_IMPLEMENTATION_PLAN.md:554B` for 1 sprint)
  - Empty scaffold dirs kept via `.gitkeep` (`apps/web`, `services/api/*`, `scripts`, `.github/workflows`) until `M0-14`/`M0-21`/`M0-28` (`c7310bf`)
  - Tagging convention `m{0..6}-{slug}` + semver `v0.1.0` … `v1.0.0` — `Admin`-only `v*`/`m*` via tag protection — `v0.0.1` now, release at `M0` green `M0:21-96`

## Sprint 1 — [start date] – [end date]

**Milestone:** M0 — Repo & Scaffolding

- Done:
  -
- In progress / carried over:
  -
- Blocked:
  -
- Decisions made this sprint:
  -

---

<!-- Add new entries above this line, newest on top -->
