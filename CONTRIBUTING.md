# Contributing — exam-integrity-system

> Single source of truth for branch workflow, Ruleset, and permissions.
> `docs/STARTING_PLAN.md` Step 2 and `docs/PROJECT_CONTEXT.md` Section 9
> reference this file. `docs/milestones/M0_IMPLEMENTATION_PLAN.md` M0-5 creates it on Day 1.

## 1. Branch naming convention (required)

All branches **must** follow:

```
<type>/<member-name>/<short-description>
```

- `type` — one of:

  | Type | Use |
  |---|---|
  | `feat/` | New feature |
  | `fix/` | Bug fix |
  | `docs/` | Documentation only |
  | `refactor/` | Code restructure, no behavior change |
  | `test/` | Tests, test infra |
  | `chore/` | Tooling, deps, CI, housekeeping |

- `member-name` — author's first name in lowercase (e.g. `seif`, `ahmed`, `sara`, `mohamed`). Use the name your team knows you by.
- `short-description` — kebab-case, short and specific.

**Examples:**

```
feat/seif/agent-tool-calling
feat/ahmed/frontend
fix/sara/api-error-handling
docs/mohamed/project-documentation
refactor/jana/cv-pipeline
test/adel/health-endpoint
chore/hana/docker-compose
```

Invalid: `feature/cv-face-detection`, `feat/agent-tool-calling` (missing member-name), `feat/Seif/AgentTool` (not kebab/lowercase).

## 2. Main branch protection — live Ruleset

Target: `main` — **Ruleset is active** via `Settings → Rules → Rulesets` (not legacy `Settings → Branches`).

| Rule | State |
|---|---|
| Restrict direct pushes/updates to `main` | **On** |
| Restrict deletions (deletion of `main` blocked) | **On** |
| Block force pushes | **On** |
| Require a pull request before merging | **On** |
| Require at least 1 approval | **On** — approval must come from sayfeldinn (only `Admin`) |
| Dismiss stale approvals when new commits are pushed | **On** |
| Require conversation resolution before merging | **On** |
| Require status checks + branches up-to-date (lint, after M0-29) | **On** after `ci.yml` lands; placeholder until then |

### Permissions / Bypass

- Only the repository `Admin` (**sayfeldinn (team lead)**) can bypass the Ruleset.
- Bypass mode: **For pull requests only** — even the admin normally opens a PR.
- Team members have **Write** access (not `Admin`) and **cannot** bypass or modify the Ruleset.
- sayfeldinn remains the **only** `Admin`. Do not grant `Admin` to others.
- For stronger “only I can approve” enforcement, use a GitHub Organization + a team containing only sayfeldinn and require review from that team (per recommendation).

## 3. PR approval ownership

- **sayfeldinn is the final reviewer/approver for every PR to `main`.** One approval from sayfeldinn is required; stale approvals are dismissed on new pushes, and all conversations must be resolved.
- Peers may review and comment for context (e.g. CV area input on schema PRs), but peer approval alone does **not** satisfy the Ruleset.
- SLA: review within **24 hours**. If no sayfeldinn review in 24h, author pings `#standup` and sayfeldinn reassigns or reviews directly. Code is `Done` only after merge, not after push.

## 4. Intended Git workflow

**Never push directly to `main` after the Ruleset is active.** The initial `git push -u origin main` in `M0-9` is the sole exception before the Ruleset exists.

For every change:

1. `git checkout -b <type>/<member-name>/<short-description>` e.g. `git checkout -b feat/seif/agent-tool-calling`
2. Commit: `git add . && git commit -m "feat: short summary"`
3. `git push -u origin <branch>`
4. Open a PR targeting `main` (ensure branch name matches §1; reference the Issue)
5. Resolve all conversations; wait for **1 approval from sayfeldinn** (stale dismissed on push)
6. sayfeldinn squash-merges. Delete the branch after merge.

If you need to update after review: push new commits to the same branch — stale approval is dismissed automatically and must be re-approved.

### Quick checks before requesting review

- Branch name matches `<type>/<member-name>/<short-description>` ?
- `git push origin main` would fail (Ruleset blocks it) — you pushed to your branch?
- PR has no unresolved conversations?
- Waiting specifically for sayfeldinn approval (not just any teammate)?

## 5. CODEOWNERS

`CODEOWNERS` requires `@sayfeldinn` (GitHub username of sayfeldinn, e.g. `@sayfeldinn`) for all paths. Peers may be listed after sayfeldinn for notification, but sayfeldinn approval is still the gate:

```
*               @sayfeldinn
/services/api/  @sayfeldinn
/apps/web/      @sayfeldinn
/infra/         @sayfeldinn
/docs/          @sayfeldinn
```

## 6. Commit style

- Conventional-ish: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:` prefix.
- Keep branch lifetime <3 days; rebase on `main` before PR; **squash-merge** to keep `main` linear.
- Never commit `node_modules/`, `.venv/`, `__pycache__/`, `.next/`, `.env` (enforced by `.gitignore`/`\.dockerignore`).

## 7. References

- Branch naming & workflow live decision: `docs/PROJECT_CONTEXT.md` §9 (2026-09-02)
- Step-by-step setup: `docs/STARTING_PLAN.md` Step 2
- M0 tasks wiring this: `docs/milestones/M0_IMPLEMENTATION_PLAN.md` M0-5, M0-6 (CODEOWNERS), M0-10 (Ruleset), M0-32 (test PR validation) — index: `docs/milestones/README.md`
