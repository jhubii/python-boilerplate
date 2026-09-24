from database.database import Database
from .model import Course


class CourseRepository:
    def __init__(self, database: Database):
        self.database = database

    def add(self, course: Course) -> Course:
        with self.database.connect() as connection:
            cursor = connection.execute(
                "INSERT INTO courses (code, name) VALUES (?, ?)",
                (course.code, course.name),
            )
            course.id = cursor.lastrowid
        return course

    def list(self) -> list[Course]:
        with self.database.connect() as connection:
            rows = connection.execute("SELECT id, code, name FROM courses").fetchall()
        return [Course(id=row[0], code=row[1], name=row[2]) for row in rows]
