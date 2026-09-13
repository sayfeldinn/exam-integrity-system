# research/

Experimental features live here first. Validate, test, review — then graduate to `services/` when production-ready.

## Convention

| Rule | Detail |
|------|--------|
| **Entry** | New features start in `research/<feature-name>/` |
| **Validation** | Test locally, get review, fix issues |
| **Graduation** | Move to `services/<feature-name>/` when production-ready |
| **Naming** | `research/<feature-name>/` (no member names) |
| **Branch** | Use `feat/<member-name>/<desc>` — same as production branches |
| **Docker** | Research features don't get Dockerfiles until graduation |
| **DB** | Research can use local SQLite; graduation means migrating to Postgres |
| **CODEOWNERS** | `/research/` requires `@sayfeldinn` + `@Jana` |

## Current Research

| Feature | Status | Branch | Merged | Fix Branch |
|---------|--------|--------|--------|------------|
| `face_recognition/` | Review-fixed, spike complete | `feat/jana/face-recognition` `PR#41` | develop | `fix/sayfeldinn/face-recognition-review` `PR#43` → main `PR#44` |
| `face_monitor/` | Superseded by face_recognition | `feat/jana/face-detection` `PR#42` | develop | — |

## Graduation Checklist

Before moving to `services/<feature-name>/`:

- [ ] Code review passed (sayfeldinn + domain CODEOWNERS)
- [ ] Tests written and passing
- [ ] No hardcoded paths/credentials
- [ ] Cross-platform (not Windows-only)
- [ ] DB migrated from SQLite to Postgres (if applicable)
- [ ] Integrated with `packages/shared` types
- [ ] Dockerfile added
- [ ] README updated with setup instructions
- [ ] Branch type changed to `feat/<member>/` for services work
