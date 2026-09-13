# face_recognition

Face Recognition service — enrollment and verification for exam proctoring.

## Running Locally

```bash
# Python 3.11.8 recommended (project pin)
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
python enrollment.py test-001
python recognition.py test-001
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `INSIGHTFACE_CTX_ID` | `-1` | ONNX Runtime context: `-1` = CPU, `0` = GPU (CUDA) |

## Files

| File | Purpose |
|------|---------|
| `enrollment.py` | Capture frames, extract embeddings, store in DB. Optionally enter recognition mode |
| `recognition.py` | Periodic face verification during exam |
| `embedding.py` | InsightFace-based face detection + embedding extraction (lazy-loaded) |
| `capture.py` | Camera handling (configurable `camera_index`) |
| `local_db.py` | SQLite dev store (replaced by Postgres in production) |
| `requirements.txt` | Pinned deps (`insightface`, `numpy<2`, `SQLAlchemy<2`, `opencv-python`) |

## Integration Notes

- Types should mirror `packages/shared` enums (`ViolationType`, `SessionStatus`) when graduating
- `local_db.py` uses `LargeBinary` for embeddings — Postgres migration will use `BYTEA`
- Threshold: 0.6 cosine similarity (unified in `recognition.py`)

## Status

Review-fixed (`fix/sayfeldinn/face-recognition-review` `PR#43`). Ready for graduation testing.
See `research/README.md` for graduation checklist.
