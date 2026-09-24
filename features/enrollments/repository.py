from features.courses.model import Course
from database.database import Database
from features.students.model import Student
from .model import Enrollment


class EnrollmentRepository:
    def __init__(self, database: Database):
        self.database = database

    def add(self, enrollment: Enrollment) -> Enrollment:
        if enrollment.student.id is None or enrollment.course.id is None:
            raise ValueError("An enrollment requires saved student and course records.")
        with self.database.connect() as connection:
            cursor = connection.execute(
                "INSERT INTO enrollments (student_id, course_id, semester) VALUES (?, ?, ?)",
                (enrollment.student.id, enrollment.course.id, enrollment.semester),
            )
            enrollment.id = cursor.lastrowid
        return enrollment

    def list(self) -> list[Enrollment]:
        with self.database.connect() as connection:
            rows = connection.execute(
                """
                SELECT e.id, e.semester, s.id, s.name, s.email, c.id, c.code, c.name
                FROM enrollments e
                JOIN students s ON e.student_id = s.id
                JOIN courses c ON e.course_id = c.id
                """
            ).fetchall()
        return [
            Enrollment(
                id=row[0], semester=row[1],
                student=Student(id=row[2], name=row[3], email=row[4]),
                course=Course(id=row[5], code=row[6], name=row[7]),
            )
            for row in rows
        ]
