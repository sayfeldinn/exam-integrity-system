# Board Setup — Manual Checklist (M0-11)

> `M0-11` `docs/milestones/M0_IMPLEMENTATION_PLAN.md:117` — GitHub Projects board creation is **manual** because the current token lacks `project` scope (`createProjectV2` requires `project` + `read:project`, but token has `gist,repo,workflow` — see log `INSUFFICIENT_SCOPES`). Milestones + labels + 21 issues are already live via API; this doc is the 1-min UI checklist to finish the board, then you use it for `M0-14..M0-34` `M0:131-182`.

## Already Done via API (no manual step)

- **Milestones 7** `M0–M6` (`1:M0 - Repo and Scaffolding` … `7:M6 - Integration Polish Defense Prep`) — `POST /repos/.../milestones` `2026-09-03` (`M0` has 21 open_issues `#1-21`)
- **Labels 9** `area:api`, `area:web`, `area:cv-identity`, `area:cv-objects`, `area:audio`, `area:risk-engine`, `area:infra`, `area:ux`, `milestone:M0` (19 total with defaults) — `POST /repos/.../labels`
- **Issues 21** `M0-14..M0-34` `#1-21` — `POST /repos/.../issues` with `milestone:1` + `labels: area:*` + `Owner` per `M0:131-182`

Verify: `https://github.com/sayfeldinn/exam-integrity-system/milestones` (7), `http://github.com/sayfeldinn/exam-integrity-system/issues` (21 open), `.../labels` (19).

## Manual — Create Projects Board (1 min, Admin only)

1. Open `https://github.com/sayfeldinn/exam-integrity-system/projects` → **New project** → **Board** (Projects V2, **Beta** — not Classic).
2. Title: `exam-integrity-system Board`
3. Columns (Board view → **Add column**):
   - `Backlog`
   - `This Sprint`
   - `In Progress`
   - `In Review (PR open)`
   - `Done`
4. WIP limits (Board settings → **Workflows** or description note):
   - `This Sprint ≤8`, `In Progress ≤4`, `In Review ≤4` (`M0:117`, `docs/milestones/M0:76-79`)
5. Custom fields (Project **Settings → Custom fields → New field**):
   - `Area` — single select: `cv-identity`, `cv-objects`, `audio`, `api`, `web`, `risk-engine`, `ux`, `infra` (matches labels `area:*` `M0:117`)
   - `Milestone` — single select: `M0`, `M1`, `M2`, `M3`, `M4`, `M5`, `M6` (mirrors GitHub Milestones `M0:80,118`)
6. Automation (optional): **Workflows** → `Item added to project` → set `Status=Backlog`; `PR opened` → `In Review`; `PR merged` → `Done` (per `M0:99` `This Sprint → In Progress → In Review → Done`).

## Manual — Seed Board with M0 Issues

1. In board, **Add items** → search `is:issue is:open milestone:"M0 - Repo and Scaffolding"` → add all 21 (`#1-21`).
2. Drag to `Backlog` (all), then move the two seeds to `This Sprint`:
   - `#1` `M0-14` `area:api` (Hana)
   - `#8` `M0-21` `area:web` (Adel)
   - Leave `M0-11..M0-13` as `Done` mental note — they were the setup tasks you just finished.
3. Add `Project` to repo: **Project Settings → Manage access** → ensure team can `Write` (board is user project, link in `README.md:11` and `docs/PROJECT_CONTEXT.md:190`).

## After Board Created

- Update this file's status to `Done` and note board URL in `docs/milestones/README.md` index (add link under `M0` row).
- Next `M0-13` `M0:119` already satisfied for `M0-14..M0-34` (issues created); `M0-11`/`M0-12` mark Done after board exists.
- `M0-30` pilot onboarding `M0:177` and `M0-31` full clones `M0:178` will use board columns to track `In Progress`.

## Tag Protection — Same Manual Step (1 min)

You approved `yes` `2026-09-03` `docs/PROJECT_CONTEXT.md:299` but API `404`. Do via UI:

`https://github.com/sayfeldinn/exam-integrity-system/settings/tags` → **New tag protection rule** → Pattern `v*` → **Add**, then Pattern `m*` → **Add** (only `Admin` can create/move `v*`/`m*`, mirrors `main` Ruleset `CONTRIBUTING.md:2`).

Or Rulesets for tags: `Settings → Rules → Rulesets → New tag ruleset` targeting `refs/tags/v*` and `refs/tags/m*` with `Restrict creations`.

---

*Delete this file after board is created, or keep as runbook for `M1–M6` similar setup. Sources: `docs/milestones/M0_IMPLEMENTATION_PLAN.md:117-119`, `docs/milestones/README.md:11`, `CONTRIBUTING.md:2`.*
