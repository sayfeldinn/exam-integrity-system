# face_recognition

Face Recognition service — enrollment and verification for exam proctoring.

## Running Locally

```bash
# Python 3.11+ required (project pins 3.11.8 via .python-version; 3.12 works too).
# Always use a FRESH venv — never a shared/global environment.
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

## Troubleshooting

### Install

- **Never install into a shared/global env.** TensorFlow pins `ml-dtypes<0.5`
  while onnx (>=1.22) requires `>=0.5.4`; mixing them crashes model import with
  `AttributeError: module 'ml_dtypes' has no attribute 'float4_e2m1fn'`.
  `requirements.txt` floors `ml_dtypes>=0.5.4` so pip fails loudly at install
  instead of at runtime.
- **`pip list` shows both `onnxruntime` and `onnxruntime-gpu`.** Expected:
  insightface declares a hard dependency on `onnxruntime`. The
  force-reinstall line in Running Locally makes the GPU build's files
  authoritative; `pip check` stays clean.
- **`onnxruntime-gpu==1.16.3` (old pin) has no Python 3.12 wheels** — the pin
  was raised to 1.30.0 for cp311/cp312 support.

### Runtime

- `UnicodeEncodeError: 'charmap' can't encode ...` (Windows cp1252 console):
  run with `set PYTHONUTF8=1` (or `python -X utf8`).
- `google.protobuf DecodeError: Error parsing message` while loading buffalo_l
  models: usually memory/commit exhaustion — this repo's dev machine has the
  pagefile disabled. Either enable Windows system-managed pagefile, or shrink
  the model set: the insightface zip ships **two** arcface models
  (`1k3d68.onnx` + `w600k_r50.onnx`); rename the unused one to
  `1k3d68.onnx.bak` (`download(force=False)` will not re-extract it).
- Red `Failed to load cublasLt64_13.dll ...` warnings on machines without
  CUDA: harmless, models fall back to CPU.

### GPU (optional)

- `onnxruntime-gpu==1.30.0` targets CUDA 13 + cuDNN 9. Easiest setup without a
  system CUDA toolkit: `pip install "onnxruntime-gpu[cuda,cudnn]==1.30.0"`
  (pulls ~1.5 GB of NVIDIA wheels), then set `INSIGHTFACE_CTX_ID=0`.
- CPU-only machine: swap the requirements line to `onnxruntime==1.30.0` and
  skip the force-reinstall line.

## Integration Notes

- Types should mirror `packages/shared` enums (`ViolationType`, `SessionStatus`) when graduating
- `local_db.py` uses `LargeBinary` for embeddings — Postgres migration will use `BYTEA`
- Threshold: 0.6 cosine similarity (unified in `recognition.py`)

## Status

Review-fixed (`fix/sayfeldinn/face-recognition-review` `PR#43`). Ready for graduation testing.
Deps re-verified 2026-10-01 on Python 3.12 (fresh venv: install, model load,
CPU inference, module imports all pass).
See `research/README.md` for graduation checklist.
