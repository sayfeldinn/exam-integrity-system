# face_recognition

Face Recognition service — enrollment and verification for exam proctoring.

## Running Locally

```bash
pip install -r requirements.txt
python enrollment.py test-001
python recognition.py test-001
python enroll_live.py test-001
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `INSIGHTFACE_CTX_ID` | `-1` | ONNX Runtime context: `-1` = CPU, `0` = GPU (CUDA) |

## Files

| File | Purpose |
|------|---------|
| `enrollment.py` | Capture frames, extract embeddings, store in DB. Optionally enter recognition mode |
| `enroll_live.py` | Live enrollment: capture, enroll, then continuous recognition in one session |
| `recognition.py` | Periodic face verification during exam (shared `cosine_similarity` + `SIMILARITY_THRESHOLD`) |
| `recognition_live.py` | Continuous live recognition with a background-threaded model (smooth camera feed) |
| `embedding.py` | Insightface-based face detection + embedding extraction |
| `capture.py` | Camera handling |
| `local_db.py` | SQLite dev store (replaced by Postgres in production) |
