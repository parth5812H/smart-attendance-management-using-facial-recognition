import sqlite3
from pathlib import Path

from app.config import DB_PATH


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = get_connection()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                roll_number TEXT NOT NULL UNIQUE,
                department TEXT NOT NULL,
                image_path TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                check_in_time TEXT NOT NULL,
                status TEXT DEFAULT 'present',
                UNIQUE(student_id, date),
                FOREIGN KEY(student_id) REFERENCES students(id)
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def add_student(name: str, roll_number: str, department: str, image_path: str):
    conn = get_connection()
    try:
        cursor = conn.execute(
            """
            INSERT INTO students (name, roll_number, department, image_path)
            VALUES (?, ?, ?, ?)
            """,
            (name, roll_number, department, image_path),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_all_students():
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM students ORDER BY created_at DESC"
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_student_by_roll_number(roll_number: str):
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM students WHERE roll_number = ?",
            (roll_number,),
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_all_attendance():
    conn = get_connection()
    try:
        rows = conn.execute(
            """
            SELECT a.id, a.date, a.check_in_time, a.status,
                   s.id AS student_id, s.name, s.roll_number, s.department
            FROM attendance a
            INNER JOIN students s ON s.id = a.student_id
            ORDER BY a.date DESC, a.check_in_time DESC
            """
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_today_attendance():
    from datetime import date

    today = date.today().isoformat()
    conn = get_connection()
    try:
        rows = conn.execute(
            """
            SELECT a.id, a.date, a.check_in_time, a.status,
                   s.id AS student_id, s.name, s.roll_number, s.department
            FROM attendance a
            INNER JOIN students s ON s.id = a.student_id
            WHERE a.date = ?
            ORDER BY a.check_in_time DESC
            """,
            (today,),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def mark_attendance(student_id: int, date_value: str, check_in_time: str):
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT OR IGNORE INTO attendance (student_id, date, check_in_time, status)
            VALUES (?, ?, ?, 'present')
            """,
            (student_id, date_value, check_in_time),
        )
        conn.commit()
    finally:
        conn.close()


def get_summary():
    students = get_all_students()
    attendance_today = get_today_attendance()
    return {
        "total_students": len(students),
        "present_today": len(attendance_today),
    }
