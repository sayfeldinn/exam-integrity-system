"""
capture.py
----------
Camera handling: opening the camera and capturing frames.
"""

import cv2


def open_camera(camera_index: int = 1) -> cv2.VideoCapture:
    """Opens the camera using DSHOW backend, falling back to index 0
    if the preferred index is unavailable."""
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        raise RuntimeError("Could not open the camera. Make sure no other application is using it.")

    # Keep only the latest frame in the buffer, avoids delayed/stale frames.
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    return cap


def capture_frame(cap: cv2.VideoCapture):
    """Captures a single frame and returns it as a BGR numpy array."""
    ok, frame = cap.read()
    if not ok:
        raise RuntimeError("Failed to capture a frame from the camera.")
    return frame
