# research/

Experimental features live here first. Validate, test, review — then graduate to `services/` when production-ready.

## Convention

| Rule | Detail |
|------|--------|
| **Entry** | New features start in `research/<feature-name>/` |
| **Validation** | Test locally, get review, fix issues |
| **Graduation** | Move to `services/<feature-name>/` when production-ready |
| **Naming** | `research/<feature-name>/` (no member names) |
| **Docker** | Research features don't get Dockerfiles until graduation |
| **DB** | Research can use local SQLite; graduation means migrating to Postgres |

## Current Research

| Feature | Status | Owner |
|---------|--------|-------|
| `face_recognition/` | Enrollment + recognition spike, needs review fixes | Jana |
| `face_monitor/` | MediaPipe face visibility monitor, superseded by face_recognition | Jana |

## Graduation Checklist

- [ ] Code review passed
- [ ] Tests written and passing
- [ ] No hardcoded paths/credentials
- [ ] Cross-platform (not Windows-only)
- [ ] DB migrated from SQLite to Postgres (if applicable)
- [ ] Integrated with `services/api` schemas
- [ ] Dockerfile added
