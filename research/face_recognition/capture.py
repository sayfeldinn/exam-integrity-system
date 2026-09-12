"""
capture.py
----------
Camera handling (opening, capturing frames).
"""

import cv2


def open_camera(camera_index: int = 0) -> cv2.VideoCapture:
    """Opens the camera and returns the VideoCapture object."""
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        raise RuntimeError(
            f"Could not open camera {camera_index}. "
            "Make sure no other application is using it."
        )
    return cap


def capture_frame(cap: cv2.VideoCapture):
    """Captures a single frame from the camera and returns it as a numpy array (BGR)."""
    ok, frame = cap.read()
    if not ok:
        raise RuntimeError("Failed to capture a frame from the camera.")
    return frame
