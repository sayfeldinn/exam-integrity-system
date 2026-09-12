import sys
import time
import numpy as np
import cv2

print("Loading AI model, please wait...")
from embedding import extract_embedding, average_embeddings
from local_db import init_db, save_face_data, get_face_data
from capture import save_live_photo
print("Model loaded successfully.")

STUDENT_ID = "test-001"
FRAME_COUNT = 4
THRESHOLD = 0.6


def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def open_camera():
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        raise RuntimeError("Camera failed to open")
    return cap


def run_enrollment(cap):
    embeddings = []
    frames = []
    frame_target_times = [time.time() + 2 * (i + 1) for i in range(FRAME_COUNT)]
    next_capture_idx = 0

    while next_capture_idx < FRAME_COUNT:
        ret, frame = cap.read()
        if not ret:
            break

        remaining = frame_target_times[next_capture_idx] - time.time()
        display = frame.copy()

        if remaining > 0:
            text = f"Capturing photo {next_capture_idx + 1}/{FRAME_COUNT} in {remaining:.1f}s"
        else:
            text = f"Captured {next_capture_idx + 1}/{FRAME_COUNT}!"

        cv2.putText(display, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow("Enrollment", display)
        cv2.waitKey(1)

        if remaining <= 0:
            try:
                emb = extract_embedding(frame)
                embeddings.append(emb)
                frames.append(frame)
                print(f"[enroll] Photo {next_capture_idx + 1}: captured successfully")
            except ValueError as e:
                print(f"[enroll] Photo {next_capture_idx + 1} skipped: {e}")
            next_capture_idx += 1

    cv2.destroyWindow("Enrollment")

    if not embeddings:
        print("Enrollment failed: no valid face detected in any frame.")
        return False

    final_embedding = average_embeddings(embeddings)
    live_photo_path = save_live_photo(frames[0], STUDENT_ID)
    save_face_data(STUDENT_ID, final_embedding, live_photo_path)

    confirm_frame = frames[-1].copy()
    cv2.putText(confirm_frame, "This is YOU - Enrolled successfully!",
                (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    cv2.imshow("Enrollment", confirm_frame)
    cv2.waitKey(2000)
    cv2.destroyWindow("Enrollment")

    print("Enrollment successful. Moving to recognition mode...")
    return True


def get_stored_embedding():
    stored = get_face_data(STUDENT_ID)
    if stored is None:
        return None
    # Handle both possible return shapes: dict or tuple
    if isinstance(stored, dict):
        return np.array(stored["embedding"])
    return np.array(stored[0])


def run_recognition(cap):
    stored_embedding = get_stored_embedding()
    if stored_embedding is None:
        print("No enrollment data found.")
        return

    print("Recognition running. Press 'q' in the window to stop.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        display = frame.copy()

        try:
            live_embedding = extract_embedding(frame)
            score = cosine_similarity(live_embedding, stored_embedding)
            if score >= THRESHOLD:
                text = f"MATCH - This is you (score={score:.2f})"
                color = (0, 255, 0)
            else:
                text = f"DIFFERENT FACE DETECTED! (score={score:.2f})"
                color = (0, 0, 255)
        except ValueError:
            text = "No face detected"
            color = (0, 165, 255)

        cv2.putText(display, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        cv2.imshow("Recognition", display)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


def main():
    init_db()
    cap = open_camera()
    try:
        if run_enrollment(cap):
            run_recognition(cap)
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()