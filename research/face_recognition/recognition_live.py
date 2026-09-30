"""
recognition_live.py
--------------------
Continuous live face recognition against a previously enrolled student.
Runs the AI model in a background thread so the displayed camera feed
stays smooth -- the model never blocks the render loop.
"""

import time
import threading

import cv2

from embedding import extract_embedding, NoFaceDetected, MultipleFacesDetected
from local_db import get_face_data
from recognition import SIMILARITY_THRESHOLD as THRESHOLD, cosine_similarity


CHECK_INTERVAL = 0.5  # how often (seconds) to run the AI model


def run_recognition(cap, student_id: str):
    stored = get_face_data(student_id)
    if stored is None:
        print("No enrollment data found.")
        return
    stored_embedding = stored[0]

    # Warm-up: run the model once so the real first comparison isn't
    # the slow "cold start" call.
    ret, warmup_frame = cap.read()
    if ret:
        try:
            extract_embedding(warmup_frame)
        except ValueError:
            pass

    print("Recognition running. Press 'q' in the window to stop.")

    shared_state = {"text": "Starting...", "color": (255, 255, 255), "busy": False}
    lock = threading.Lock()

    def process_frame(frame):
        try:
            live_embedding = extract_embedding(frame)
            score = cosine_similarity(live_embedding, stored_embedding)
            if score >= THRESHOLD:
                text = f"MATCH - This is you (score={score:.2f})"
                color = (0, 255, 0)
            else:
                text = f"DIFFERENT FACE DETECTED! (score={score:.2f})"
                color = (0, 0, 255)
        except MultipleFacesDetected as e:
            text = f"VIOLATION: {e}"
            color = (0, 0, 255)
        except NoFaceDetected:
            text = "No face detected"
            color = (0, 165, 255)

        with lock:
            shared_state["text"] = text
            shared_state["color"] = color
            shared_state["busy"] = False

    last_check_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

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
        cv2.imshow("Recognition", display)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break