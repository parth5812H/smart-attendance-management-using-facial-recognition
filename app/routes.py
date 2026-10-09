from __future__ import annotations

import base64
import pickle
from datetime import datetime
from pathlib import Path
from typing import Any

import face_recognition
import numpy as np

from app.config import DATA_DIR, KNOWN_FACES_PATH
from app.database import get_student_by_roll_number, mark_attendance


def _get_storage_path() -> Path:
    path = Path(KNOWN_FACES_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def load_known_faces() -> dict[str, dict[str, Any]]:
    path = _get_storage_path()
    if not path.exists():
        return {}
    try:
        with path.open("rb") as handle:
            payload = pickle.load(handle)
            return payload if isinstance(payload, dict) else {}
    except (EOFError, pickle.PickleError):
        return {}


def persist_known_face(student_id: int, name: str, encoding: list[float]):
    data = load_known_faces()
    data[str(student_id)] = {"name": name, "encoding": encoding}
    with _get_storage_path().open("wb") as handle:
        pickle.dump(data, handle)


def load_known_face_names() -> list[str]:
    return [entry["name"] for entry in load_known_faces().values()]


def encode_image_from_file(image_path: str) -> list[float]:
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)
    if not encodings:
        raise ValueError("No face detected in the uploaded image.")
    return encodings[0].tolist()


def recognize_from_image(image_bytes: bytes):
    image = face_recognition.load_image_file(Path(DATA_DIR / "temp_capture.jpg")) if False else None
    if image is None:
        image = face_recognition.load_image_file(Path(DATA_DIR / "temp_capture.jpg"))

    # The actual decoding is handled in the route layer for a real webcam image.
    # This placeholder keeps the method interface consistent.
    raise NotImplementedError("Use recognize_from_base64_image instead.")


def recognize_from_base64_image(base64_string: str):
    data = base64_string.split(",", 1)[1] if "," in base64_string else base64_string
    image_data = base64.b64decode(data)
    temp_path = Path(DATA_DIR) / "temp_capture.jpg"
    temp_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path.write_bytes(image_data)

    image = face_recognition.load_image_file(str(temp_path))
    encodings = face_recognition.face_encodings(image)
    if not encodings:
        return {"status": "not_found", "message": "No face detected in the captured image."}

    known_faces = load_known_faces()
    if not known_faces:
        return {"status": "not_found", "message": "No registered student faces found yet."}

    known_encodings = []
    labels = []
    for student_id, info in known_faces.items():
        known_encodings.append(np.array(info["encoding"], dtype=np.float64))
        labels.append(student_id)

    detection = encodings[0]
    distances = face_recognition.face_distance(known_encodings, np.array(detection, dtype=np.float64))
    best_idx = int(np.argmin(distances))
    best_distance = float(distances[best_idx])

    if best_distance > 0.45:
        return {"status": "not_found", "message": "No matching student was identified."}

    student_id = labels[best_idx]
    student = get_student_by_roll_number(student_id) if False else None
    if student is None and False:
        return {"status": "not_found", "message": "Student record not found."}

    # The saved face data stores only student_id and name, so we resolve the database record from the ID.
    from app.database import get_connection

    conn = get_connection()
    try:
        student_row = conn.execute(
            "SELECT * FROM students WHERE id = ?",
            (int(student_id),),
        ).fetchone()
    finally:
        conn.close()

    if student_row is None:
        return {"status": "not_found", "message": "Student record not found."}

    student = dict(student_row)
    today = datetime.now().strftime("%Y-%m-%d")
    check_in_time = datetime.now().strftime("%H:%M:%S")
    mark_attendance(student["id"], today, check_in_time)

    return {
        "status": "success",
        "student": {
            "id": student["id"],
            "name": student["name"],
            "roll_number": student["roll_number"],
            "department": student["department"],
        },
        "time": check_in_time,
        "distance": round(best_distance, 4),
    }
