from dataclasses import dataclass


@dataclass
class Student:
    id: int | None = None
    name: str = ""
    roll_number: str = ""
    department: str = ""
    image_path: str = ""
    created_at: str | None = None


@dataclass
class AttendanceRecord:
    id: int | None = None
    student_id: int = 0
    date: str = ""
    check_in_time: str = ""
    status: str = "present"
    name: str = ""
    roll_number: str = ""
    department: str = ""
