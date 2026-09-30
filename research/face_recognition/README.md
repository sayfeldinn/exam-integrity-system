# face_recognition

Face Recognition service — responsible for two main phases:
1. **Enrollment**: Registers the student's face embedding before the exam starts (`enrollment.py`).
2. **Recognition**: Periodic verification during the exam (`recognition.py`).

## Running Locally

```bash
pip install -r requirements.txt
python enroll_live.py test-001