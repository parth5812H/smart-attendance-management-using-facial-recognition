from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_FOLDER = str(DATA_DIR / "uploads")
DB_PATH = str(DATA_DIR / "attendance.db")
KNOWN_FACES_PATH = str(DATA_DIR / "known_faces.pkl")
