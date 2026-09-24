from database.database import Database
from .model import Course
from .repository import CourseRepository


class CourseService:
    def __init__(self, database: Database):
        self.repository = CourseRepository(database)

    def add_course(self, course: Course) -> Course:
        return self.repository.add(course)

    def get_courses(self) -> list[Course]:
        return self.repository.list()
