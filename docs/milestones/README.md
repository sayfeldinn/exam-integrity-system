# Milestone Plans — exam-integrity-system

> Per-milestone execution specs. Canonical tracking lives in GitHub Milestones/Projects
> (`docs/PROJECT_CONTEXT.md:190-192` — not a doc). This folder is the **verifiable
> how** for each `M0–M6`; `docs/STARTING_PLAN.md:3-7` is the 10-min orientation
> (`M0` wins if conflict). Each plan is created from the `M0` template (`M0:3-17`).

## Index

| # | Plan | Target | Scope | Status |
|---|---|---|---|---|
| M0 | [`M0_IMPLEMENTATION_PLAN.md`](./M0_IMPLEMENTATION_PLAN.md) | Week 1–2 | Skeleton, `services/api` + `apps/web` scaffolded, Ruleset, `docker compose up` on 2 OSes | Active — DoD `M0:21-96`, Phases `M0:99-186`, Exit `M0:349-360` |
| M1 | `M1_IMPLEMENTATION_PLAN.md` | Week 3–4 | Student registration flow, ID/photo capture, DB schema for students | Planned — drafted at `M0-34` `M0:182` |
| M2 | `M2_IMPLEMENTATION_PLAN.md` | Week 5–6 | Live face verification end-to-end (client capture → CV service → API) | Planned |
| M3 | `M3_IMPLEMENTATION_PLAN.md` | Week 7–8 | Periodic identity re-checks during an active session | Planned |
| M4 | `M4_IMPLEMENTATION_PLAN.md` | Week 9–10 | Risk signal fusion (head pose, face loss, etc.) feeding a basic risk score | Planned |
| M5 | `M5_IMPLEMENTATION_PLAN.md` | Week 11–12 | Working dashboard: live sessions, alerts, risk scores | Planned |
| M6 | `M6_IMPLEMENTATION_PLAN.md` | Week 13+ | End-to-end testing, demo rehearsal, report/slides finalized | Planned |

Timeline assumes ~12–14 week runway (`docs/PROJECT_CONTEXT.md:222-235`); `M0` due = `D-14w` (defense date `D`).

## How to use

- **New joiner:** read `docs/STARTING_PLAN.md` (10 min), then the active `M*` plan in this folder.
- **Leader/PM:** each `M*` defines Definition of Done, Phases `ID | Task | Depends on | Est. | Owner`, risks, and Exit Checklist (copy-pasteable into Milestone description). Turn each row into a GitHub Issue tagged `Area` + `Milestone`.
- **Process:** `M0-34` (`M0:182`) drafts `M1` issues; `Exit` `M0:358` closes `M0` and freezes `docs/API_CONTRACT.md`. Update this index when a milestone closes.

## Conventions

- Compose path: `infra/docker-compose.yml` via `docker compose -f infra/docker-compose.yml up` (not root) — `M0:14`
- Branch naming: `<type>/<member-name>/<short-description>` per `CONTRIBUTING.md:1` (`feat/ fix/ docs/ refactor/ test/ chore/`)
- Ruleset: `Settings → Rules → Rulesets` targeting `main` per `CONTRIBUTING.md:2` / `M0-10` `M0:116` (not legacy `Settings → Branches`)
- Durable docs stay flat in `docs/` (`ARCHITECTURE.md`, `API_CONTRACT.md`, `ONBOARDING.md`); per-milestone execution lives here.

## References

- Full feature/MVP context: `docs/PROJECT_CONTEXT.md`
- Durable decisions: `docs/PROJECT_CONTEXT.md:275-291` (Section 9)
- Sprint-by-sprint progress: `docs/PROGRESS_LOG.md`, `docs/supervisor-log.md`
