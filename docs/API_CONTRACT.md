# API Contract

Frozen contract for Exam Integrity System API responses.

> **Source of truth**: `packages/shared/` types are canonical.  
> API schemas (`services/api/schemas/`) and frontend imports (`apps/web/lib/api.ts`) consume them.

---

## Endpoints

### `GET /api/v1/health`

Health check verifying API and database connectivity.

**Response** `200 OK`

```json
{
  "status": "ok",
  "database": "healthy"
}
```

**Response** `200 OK` (degraded)

```json
{
  "status": "degraded",
  "database": "unhealthy: connection refused"
}
```

---

### `GET /api/v1/students/{student_id}/sessions`

List of exam sessions for a student.

**Response** `200 OK`

```json
{
  "sessions": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "student_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "exam_id": "MATH-301-MID",
      "start_time": "2025-01-15T09:00:00Z",
      "status": "active",
      "created_at": "2025-01-15T08:59:58Z"
    }
  ]
}
```

---

### `GET /api/v1/sessions/{session_id}/violations`

List of violations recorded for an exam session.

**Response** `200 OK`

```json
{
  "violations": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "session_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "type": "phone",
      "timestamp": "2025-01-15T09:15:32Z",
      "risk_contribution": 0.85,
      "confidence": 0.92,
      "meta": {
        "bbox": [120, 200, 300, 450],
        "frame_url": "/frames/session123/frame_0450.jpg"
      }
    },
    {
      "id": "a1b2c3d4-5678-9abc-def0-1234567890ab",
      "session_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "type": "face_loss",
      "timestamp": "2025-01-15T09:22:10Z",
      "risk_contribution": 0.6,
      "confidence": 0.78,
      "meta": {
        "duration_seconds": 12
      }
    }
  ]
}
```

---

## Types

### `Student`

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "name": "Ahmed Ali",
  "university_id": "20210123",
  "registered_photo_ref": "/photos/20210123.jpg",
  "role": "student",
  "created_at": "2025-01-10T08:00:00Z"
}
```

### `ExamSession`

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "student_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "exam_id": "MATH-301-MID",
  "start_time": "2025-01-15T09:00:00Z",
  "status": "pending",
  "created_at": "2025-01-15T08:59:58Z"
}
```

### `Violation`

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "session_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "type": "phone",
  "timestamp": "2025-01-15T09:15:32Z",
  "risk_contribution": 0.85,
  "confidence": 0.92,
  "meta": {}
}
```

---

## Enums

### `UserRole`

`"student"` | `"proctor"` | `"admin"`

### `SessionStatus`

`"pending"` | `"active"` | `"ended"`

### `ViolationType`

`"phone"` | `"person"` | `"face_loss"` | `"head_turn"` | `"voice"` | `"noise"` | `"screen_leave"`

---

## OpenAPI Snippet

```yaml
openapi: 3.1.0
info:
  title: Exam Integrity System API
  version: 0.1.0
paths:
  /api/v1/health:
    get:
      operationId: healthCheck
      summary: Health check
      responses:
        "200":
          description: API and database health status
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/HealthResponse"
components:
  schemas:
    HealthResponse:
      type: object
      required: [status, database]
      properties:
        status:
          type: string
          enum: [ok, degraded]
        database:
          type: string
    ExamSession:
      type: object
      required: [id, student_id, exam_id, start_time, status, created_at]
      properties:
        id:
          type: string
          format: uuid
        student_id:
          type: string
          format: uuid
        exam_id:
          type: string
        start_time:
          type: string
          format: date-time
        status:
          $ref: "#/components/schemas/SessionStatus"
        created_at:
          type: string
          format: date-time
    SessionStatus:
      type: string
      enum: [pending, active, ended]
    Violation:
      type: object
      required: [id, session_id, type, timestamp, risk_contribution, confidence, meta]
      properties:
        id:
          type: string
          format: uuid
        session_id:
          type: string
          format: uuid
        type:
          $ref: "#/components/schemas/ViolationType"
        timestamp:
          type: string
          format: date-time
        risk_contribution:
          type: number
          minimum: 0
          maximum: 1
        confidence:
          type: number
          minimum: 0
          maximum: 1
        meta:
          type: object
    ViolationType:
      type: string
      enum: [phone, person, face_loss, head_turn, voice, noise, screen_leave]
```
