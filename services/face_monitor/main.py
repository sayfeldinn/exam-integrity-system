import cv2
import mediapipe as mp
import time

# =========================
# MediaPipe Initialization
# =========================
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# =========================
# Camera Setup
# =========================
camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if not camera.isOpened():
    print("❌ Camera could not be opened")
    exit()

# =========================
# Timing & Persistence Variables
# =========================
warning_start_time = None
WARNING_DURATION = 2.0  # Seconds required to confirm a warning

normal_start_time = time.time()
VERIFICATION_DELAY = 4.0  # Updated to 4 seconds of stable state for verification
is_verified = False

# =========================
# Face Detection Setup
# =========================
with mp_face_detection.FaceDetection(
    model_selection=0, 
    min_detection_confidence=0.5
) as face_detection:

    while camera.isOpened():
        success, frame = camera.read()

        if not success:
            print("❌ Could not read frame")
            break

        h, w, _ = frame.shape
        
        # Flip frame horizontally for a natural mirror view
        frame = cv2.flip(frame, 1)
        
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image_rgb)

        # =========================
        # Face Count & Frame Check
        # =========================
        face_count = 0
        out_of_frame = False

        if results.detections:
            face_count = len(results.detections)
            
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                x, y, w_box, h_box = bboxC.xmin, bboxC.ymin, bboxC.width, bboxC.height
                
                # Check if face is near frame boundaries
                if x < 0.02 or y < 0.02 or (x + w_box) > 0.98 or (y + h_box) > 0.98:
                    out_of_frame = True

        # =========================
        # State & Logic Evaluation
        # =========================
        is_warning_condition = (face_count == 0) or (face_count > 1) or out_of_frame

        # Status styling defaults (Normal)
        status_text = "STATUS: NORMAL (1 Face Detected)"
        status_color = (0, 200, 0)  # Professional Green
        banner_color = (30, 30, 30) # Dark sleek background

        if face_count == 0:
            status_text = "WARNING: No Face Detected!"
            status_color = (0, 0, 255) # Red
            is_verified = False
            normal_start_time = None
        elif face_count > 1:
            status_text = f"WARNING: Multiple Faces Detected ({face_count})!"
            status_color = (0, 140, 255) # Orange/Amber
            is_verified = False
            normal_start_time = None
        elif out_of_frame:
            status_text = "WARNING: Face Out of Frame / Too Close to Edge!"
            status_color = (0, 140, 255)
            is_verified = False
            normal_start_time = None
        else:
            # Normal state handling with 4-second verification timer
            if normal_start_time is None:
                normal_start_time = time.time()
            
            elapsed_normal_time = time.time() - normal_start_time
            if elapsed_normal_time >= VERIFICATION_DELAY:
                is_verified = True
                status_text = "STATUS: VERIFIED & STABLE"
                status_color = (0, 255, 120) # Bright Mint Green

        # Draw face bounding boxes nicely
        if results.detections:
            for detection in results.detections:
                mp_drawing.draw_detection(frame, detection)

        # =========================
        # Professional UI Overlay Rendering
        # =========================
        # Top Header Banner Background
        cv2.rectangle(frame, (0, 0), (w, 55), banner_color, -1)
        
        # Status Text
        cv2.putText(
            frame,
            status_text,
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            status_color,
            2
        )

        # Face Count Indicator on Top Right
        count_str = f"Faces: {face_count}"
        cv2.putText(
            frame,
            count_str,
            (w - 140, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (200, 200, 200),
            1
        )

        # Bottom Footer Instruction Bar
        cv2.rectangle(frame, (0, h - 35), (w, h), banner_color, -1)
        cv2.putText(
            frame,
            "Exam Proctoring System v1.0  |  Press 'q' or ESC to Exit",
            (20, h - 12),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (170, 170, 170),
            1
        )

        # =========================
        # Show Frame
        # =========================
        cv2.imshow("Exam Integrity - Professional Monitor", frame)

        # =========================
        # Exit Condition
        # =========================
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break

# =========================
# Cleanup
# =========================
camera.release()
cv2.destroyAllWindows()