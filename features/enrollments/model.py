from dataclasses import dataclass

from features.courses.model import Course
from features.students.model import Student


@dataclass
class Enrollment:
    student: Student | None
    course: Course | None
    semester: str
    id: int | None = None

    def __post_init__(self) -> None:
        self.semester = self.semester.strip()
        if self.student is None:
            raise ValueError("Select a student.")
        if self.course is None:
            raise ValueError("Select a course.")
        if self.semester not in ("1st Semester", "2nd Semester"):
            raise ValueError("Semester must be 1st Semester or 2nd Semester.")
