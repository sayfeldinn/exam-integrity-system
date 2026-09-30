# packages/shared

Single source of truth for Exam Integrity System types.

Both `services/api/schemas/` and `apps/web/lib/api.ts` should import from this package.

## Structure

```
packages/shared/
  types/
    session.ts      # ExamSession, SessionStatus
    violation.ts    # Violation, ViolationType
  violation.py      # Python ViolationType, SessionStatus enums
  export_openapi.py # Export OpenAPI schema from FastAPI app
  README.md
```

## Canonical Types

- **ViolationType**: `phone | person | face_loss | head_turn | voice | noise | screen_leave`
- **SessionStatus**: `pending | active | ended`
- **ExamSession**: student_id, exam_id, start_time, status
- **Violation**: session_id, type, timestamp, risk_contribution, confidence, meta

## Usage

### TypeScript (frontend)

```ts
import { Violation, ViolationType } from "@exam-integrity/shared/types/violation";
import { ExamSession, SessionStatus } from "@exam-integrity/shared/types/session";
```

### Python (API schemas)

```python
from packages.shared.violation import ViolationType, SessionStatus
```

### OpenAPI Export

```bash
python packages/shared/export_openapi.py > docs/openapi.json
```

## Rules

- Types here are the **single source of truth**
- API schemas mirror these definitions
- Frontend types are derived from these files
- Changes to contract require updating this package first
