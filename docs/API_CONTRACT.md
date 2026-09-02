# API Contract — exam-integrity-system (v0, M0-19)

> Freeze: `students` / `sessions` / `violations` JSON + `GET /api/v1/health`.
> Created in `M0-19` `M0:136` (sayfeldinn approval required). Canonical for `M0-14..M0-25` and future CV work.
> Types mirrored in `packages/shared` — single source of truth `M0:49`.

## 1. Health (M0)

### `GET /api/v1/health` — public (no auth `M0:32`)

- **Response 200:**

```json
{"status":"ok"}
```

- **Redirect:** `GET /health` → `302 /api/v1/health`
- **OpenAPI snippet:**

```yaml
/api/v1/health:
  get:
    summary: Health check (public)
    responses:
      '200':
        content:
          application/json:
            schema: {type: object, properties: {status: {type: string, enum: [ok]}}, required: [status]}
```

- **Web usage:** `apps/web` client-side `fetch(${process.env.NEXT_PUBLIC_API_URL}/api/v1/health)` with fallback UI `API unreachable — check docker logs api` `M0:151`.

## 2. Students (v0, M0-18)

Table: `students` — `id PK`, `university_id UNIQUE`, `role enum`, etc. (`docs/ARCHITECTURE.md:3`)

**Example:**

```json
{
  "id": "uuid",
  "name": "Seif Eldeen Nasser",
  "university_id": "2023XXXX",
  "registered_photo_ref": "s3://bucket/students/uuid.jpg",
  "role": "student",
  "created_at": "2026-09-03T00:00:00Z"
}
```

- `role`: `student | proctor | admin` (enum)
- `hashed_password` never exposed in API.

## 3. Sessions (v0)

**Example:**

```json
{
  "id": "uuid",
  "student_id": "uuid",
  "exam_id": "exam-2026-final",
  "start_time": "2026-09-03T10:00:00Z",
  "status": "active",
  "created_at": "2026-09-03T10:00:00Z"
}
```

- `status`: `pending | active | ended` (enum)

## 4. Violations (v0)

**Example:**

```json
{
  "id": "uuid",
  "session_id": "uuid",
  "type": "face_loss",
  "timestamp": "2026-09-03T10:05:23Z",
  "risk_contribution": 0.3,
  "confidence": 0.92,
  "meta": {"duration_ms": 4500}
}
```

- `type`: `phone | person | face_loss | head_turn | voice | noise | screen_leave` (enum)
- `risk_contribution`: `float 0.0–1.0` (`CHECK 0-1`)
- `confidence`: `float 0.0–1.0`
- `meta`: `jsonb` free-form (e.g. `{"duration_ms":...}`, `{"heading":"left"}`)

## 5. Shared Types

`packages/shared` MUST mirror this contract:

```
packages/shared/types/student.ts + student.py
packages/shared/types/session.ts + session.py
packages/shared/types/violation.ts + violation.py
```

Both `services/api/schemas` and `apps/web/lib/api.ts` import shared types — no `any` duplication (DoD `M0:49`).

---

*Extensions in M1+ append here with version note; do not break v0 fields.*
