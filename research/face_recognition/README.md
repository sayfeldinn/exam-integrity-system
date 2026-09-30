# face_recognition

Face Recognition service — enrollment and verification for exam proctoring.

## Running Locally

```bash
# Python 3.11+ required (project pins 3.11.8 via .python-version; 3.12 works too).
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
# insightface also depends on CPU `onnxruntime`, whose files overwrite the GPU
# build's during install. Re-assert the GPU build so CUDA stays discoverable:
pip install --force-reinstall --no-deps onnxruntime-gpu==1.30.0
python enrollment.py test-001
python recognition.py test-001
```

On machines without CUDA this is still safe: ONNX Runtime logs red
`Failed to load cublasLt64_13.dll ...` warnings at startup, then runs on CPU
(this spike defaults to CPU anyway via `INSIGHTFACE_CTX_ID=-1`).

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
| `requirements.txt` | Pinned deps (`insightface==2.0`, `onnxruntime-gpu==1.30.0`, `onnx==1.22.0`, `ml_dtypes>=0.5.4` guard, `opencv-python==5.0.0.93`, `numpy==2.5.3`, `SQLAlchemy==2.0.35`) |
| `tests/` | Local test scripts (e.g. `mock_visibility_monitor.py`) |


See `research/README.md` for graduation checklist.
