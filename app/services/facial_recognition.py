import base64
import pickle
from pathlib import Path
from typing import Any

import face_recognition
import numpy as np

from app.config import KNOWN_FACES_PATH


def _get_storage_path() -> Path:
    path = Path(KNOWN_FACES_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def load_known_faces() -> dict[str, dict[str, Any]]:
    storage = _get_storage_path()
    if not storage.exists():
        return {}
    with storage.open("rb") as handle:
        try:
            data = pickle.load(handle)
            return data if isinstance(data, dict) else {}
        except (EOFError, pickle.PickleError):
            return {}


def save_known_face(student_id: int, name: str, encoding: list[float]):
    data = load_known_faces()
    data[str(student_id)] = {"name": name, "encoding": encoding}
    with _get_storage_path().open("wb") as handle:
        pickle.dump(data, handle)


def get_best_match(unknown_encoding: list[float]) -> tuple[str | None, float | None]:
    known_data = load_known_faces()
    if not known_data:
        return None, None

    known_encodings = []
    names = []
    for student_id, info in known_data.items():
        known_encodings.append(np.array(info["encoding"], dtype=np.float64))
        names.append(f"{info['name']}::{student_id}")

    if not known_encodings:
        return None, None

    distances = face_recognition.face_distance(known_encodings, np.array(unknown_encoding, dtype=np.float64))
    best_index = int(np.argmin(distances))
    best_distance = float(distances[best_index])
    if best_distance <= 0.45:
        student_key = names[best_index].split("::")[-1]
        return student_key, best_distance
    return None, best_distance


def encode_image_from_file(image_path: str):
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)
    if not encodings:
        raise ValueError("No face detected in the uploaded image.")
    return encodings[0].tolist()


def get_student_name_from_id(student_id: str | int):
    data = load_known_faces()
    student_data = data.get(str(student_id))
    if not student_data:
        return None
    return student_data.get("name")


def decode_base64_image(base64_data: str):
    data = base64_data.split(",", 1)[1] if "," in base64_data else base64_data
    image_data = base64.b64decode(data)
    return image_data
