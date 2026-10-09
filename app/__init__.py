from flask import Flask
from pathlib import Path

from app.config import BASE_DIR, UPLOAD_FOLDER, DB_PATH
from app.database import init_db
from app.routes import bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY="smart-attendance-secret-key",
        UPLOAD_FOLDER=UPLOAD_FOLDER,
        DATABASE_PATH=DB_PATH,
    )

    Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
    init_db()
    app.register_blueprint(bp)
    return app
