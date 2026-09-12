"""
capture.py
----------
Responsible for camera handling (opening, capturing frames) and saving/loading student photos.
"""

import os
import cv2

LIVE_PHOTOS_DIR = os.path.join(os.path.dirname(__file__), "live_photos")
os.makedirs(LIVE_PHOTOS_DIR, exist_ok=True)


def open_camera(camera_index: int = 0) -> cv2.VideoCapture:
    """Opens the camera and returns the VideoCapture object."""
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        raise RuntimeError("Could not open the camera. Make sure no other application is using it.")
    return cap

def capture_frame(cap: cv2.VideoCapture):
    """Captures a single frame from the camera and returns it as a numpy array (BGR)."""
    ok, frame = cap.read()
    if not ok:
        raise RuntimeError("Failed to capture a frame from the camera.")
    return frame


def capture_multiple_frames(camera_index: int = 0, count: int = 5, delay_frames: int = 5):
    """
    Opens the camera and captures `count` frames with a slight delay between them
    so the student can shift slightly between frames.
    """
    cap = open_camera(camera_index)
    frames = []
    try:
        while len(frames) < count:
            for _ in range(delay_frames):
                cap.read()  # Dummy reads to clear buffer/create delay
            frame = capture_frame(cap)
            frames.append(frame)
    finally:
        cap.release()
    return frames


def save_live_photo(frame, student_id: str) -> str:
    """Saves a frame as an image on disk and returns its file path."""
    filename = f"{student_id}_live.jpg"
    filepath = os.path.join(LIVE_PHOTOS_DIR, filename)
    cv2.imwrite(filepath, frame)
    return filepath


def load_live_photo(student_id: str):
    """Returns the saved student photo as a numpy array, or None if it doesn't exist."""
    filepath = os.path.join(LIVE_PHOTOS_DIR, f"{student_id}_live.jpg")
    if not os.path.exists(filepath):
        return None
    return cv2.imread(filepath)