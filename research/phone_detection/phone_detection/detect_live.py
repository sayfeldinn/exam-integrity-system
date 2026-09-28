"""
detect_live.py
--------------
Continuous live phone detection during a session. Runs the YOLO model
in a background thread so the displayed camera feed stays smooth, and
only logs a violation after a few consecutive detections (avoids
logging on a single flickering false positive).
"""

import sys
import threading
import time

import cv2

from capture import open_camera, capture_frame
from detector import detect_forbidden_objects
from local_db import init_db, log_violation

CHECK_INTERVAL = 0.5          # how often (seconds) to run the model
CONSECUTIVE_REQUIRED = 2      # detections in a row needed before logging


def run_detection(session_id: str):
    init_db()
    cap = open_camera()

    shared_state = {"text": "Starting...", "color": (255, 255, 255), "busy": False}
    lock = threading.Lock()
    consecutive_count = 0

    def process_frame(frame):
        nonlocal consecutive_count
        detections = detect_forbidden_objects(frame)

        if detections:
            consecutive_count += 1
            best = max(detections, key=lambda d: d.confidence)
            text = f"PHONE DETECTED (confidence={best.confidence:.2f})"
            color = (0, 0, 255)
            if consecutive_count >= CONSECUTIVE_REQUIRED:
                log_violation(session_id, best.label, best.confidence)
                consecutive_count = 0
        else:
            consecutive_count = 0
            text = "No forbidden object detected"
            color = (0, 200, 0)

        with lock:
            shared_state["text"] = text
            shared_state["color"] = color
            shared_state["busy"] = False

    print("Detection running. Press 'q' in the window to stop.")

    last_check_time = 0
    try:
        while True:
            frame = capture_frame(cap)
            display = frame.copy()
            now = time.time()

            with lock:
                busy = shared_state["busy"]

            if not busy and (now - last_check_time >= CHECK_INTERVAL):
                last_check_time = now
                with lock:
                    shared_state["busy"] = True
                threading.Thread(target=process_frame, args=(frame.copy(),), daemon=True).start()

            with lock:
                text = shared_state["text"]
                color = shared_state["color"]

            cv2.putText(display, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            cv2.imshow("Phone Detection", display)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    sid = sys.argv[1] if len(sys.argv) > 1 else "test-session-001"
    run_detection(sid)
