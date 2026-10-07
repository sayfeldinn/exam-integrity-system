# phone_detection

Detects a phone in the exam camera feed using a YOLO model, and logs a
violation to a local database after a few consecutive detections.

## Setup

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Download the YOLO weights file (`yolo11n.pt`) and place it directly in
this folder. It is not committed to the repository (see `.gitignore`).

## Run

```
python detect_live.py test-session-001
```

Press `q` in the video window to stop.

## Files

- `capture.py` — opens the camera and captures frames.
- `detector.py` — loads the YOLO model once and detects forbidden objects.
- `local_db.py` — local SQLite database for this feature's violations
  (`local_phone_detection.db`, created automatically, not committed).
- `detect_live.py` — runs detection continuously in a background thread
  so the video feed stays smooth, and logs a violation after
  `CONSECUTIVE_REQUIRED` consecutive detections.

## Notes

- `local_phone_detection.db` and `*.pt` files are local-only and are not
  meant to be committed.
- Tune `CONFIDENCE_THRESHOLD` and `FORBIDDEN_CLASS_NAMES` in `detector.py`,
  and `CONSECUTIVE_REQUIRED` in `detect_live.py`, based on testing.
