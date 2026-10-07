"""
detect_live.py
--------------
Live phone detection during a session. Detection runs synchronously on
every Nth frame (not in a background thread) so the on-screen message
always reflects the latest frame with no lag. A violation is only
logged after a few consecutive detections to avoid logging a single
flickering false positive.
"""

import sys
import time

import cv2

from capture import open_camera, capture_frame
from detector import detect_forbidden_objects
from local_db import init_db, log_violation

PROCESS_EVERY_N_FRAMES = 2    # run the model every 2nd frame to keep the feed smooth
CONSECUTIVE_REQUIRED = 2      # detections in a row needed before logging a violation


def run_detection(session_id: str):
    init_db()
    cap = open_camera()

    consecutive_count = 0
    phone_visible_since = None
    text = "Starting..."
    color = (255, 255, 255)
    last_detections = []
    frame_counter = 0

    print("Detection running. Press 'q' in the window to stop.")

    try:
        while True:
            frame = capture_frame(cap)
            frame_counter += 1

            if frame_counter % PROCESS_EVERY_N_FRAMES == 0:
                detections = detect_forbidden_objects(frame)
                last_detections = detections

                if detections:
                    consecutive_count += 1
                    best = max(detections, key=lambda d: d.confidence)

                    if phone_visible_since is None:
                        phone_visible_since = time.time()
                    duration = time.time() - phone_visible_since

                    text = f"PHONE DETECTED ({duration:.0f}s, confidence={best.confidence:.2f})"
                    color = (0, 0, 255)

                    if consecutive_count >= CONSECUTIVE_REQUIRED:
                        log_violation(session_id, best.label, best.confidence)
                else:
                    consecutive_count = 0
                    phone_visible_since = None
                    text = "No forbidden object detected"
                    color = (0, 200, 0)

            display = frame.copy()

            # Draw a box around each detected phone for visual confirmation.
            for det in last_detections:
                x1, y1, x2, y2 = [int(v) for v in det.bbox]
                cv2.rectangle(display, (x1, y1), (x2, y2), (0, 0, 255), 2)

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