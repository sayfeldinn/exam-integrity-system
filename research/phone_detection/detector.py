"""
detector.py
-----------
Detects forbidden objects (phones) in a frame using a YOLO model.
The model is loaded once on import, not on every call.
"""

from dataclasses import dataclass
from typing import List

import numpy as np
from ultralytics import YOLO

MODEL_PATH = "yolo11n.pt"
CONFIDENCE_THRESHOLD = 0.45           # standard working threshold for cell phone detection
IMG_SIZE = 640                         # YOLO's default — matches typical webcam feeds well
FORBIDDEN_CLASS_NAMES = {"cell phone"}

_model = YOLO(MODEL_PATH)
_phone_class_id = [k for k, v in _model.names.items() if v in FORBIDDEN_CLASS_NAMES]


@dataclass
class Detection:
    label: str
    confidence: float
    bbox: tuple  # (x1, y1, x2, y2)


def detect_forbidden_objects(frame: np.ndarray) -> List[Detection]:
    """Runs detection on a single frame and returns only the forbidden
    objects found (e.g. a phone), above CONFIDENCE_THRESHOLD."""
    results = _model.predict(
        frame, verbose=False, imgsz=IMG_SIZE, conf=CONFIDENCE_THRESHOLD,
        classes=_phone_class_id,
    )[0]

    detections: List[Detection] = []
    for box in results.boxes:
        label = _model.names[int(box.cls[0])]
        confidence = float(box.conf[0])
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        detections.append(Detection(label=label, confidence=confidence, bbox=(x1, y1, x2, y2)))
    return detections