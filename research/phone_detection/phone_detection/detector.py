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

MODEL_PATH = "yolo11n.pt"          # place the weights file next to this module
CONFIDENCE_THRESHOLD = 0.5
FORBIDDEN_CLASS_NAMES = {"cell phone"}  # COCO class name used by the model

_model = YOLO(MODEL_PATH)


@dataclass
class Detection:
    label: str
    confidence: float
    bbox: tuple  # (x1, y1, x2, y2)


def detect_forbidden_objects(frame: np.ndarray) -> List[Detection]:
    """Runs detection on a single frame and returns only the forbidden
    objects found (e.g. a phone), above CONFIDENCE_THRESHOLD."""
    results = _model.predict(frame, verbose=False)[0]

    detections: List[Detection] = []
    for box in results.boxes:
        label = _model.names[int(box.cls[0])]
        confidence = float(box.conf[0])
        if label in FORBIDDEN_CLASS_NAMES and confidence >= CONFIDENCE_THRESHOLD:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            detections.append(Detection(label=label, confidence=confidence, bbox=(x1, y1, x2, y2)))
    return detections
