from database.database import Database
from .model import Enrollment
from .repository import EnrollmentRepository


class EnrollmentService:
    def __init__(self, database: Database):
        self.repository = EnrollmentRepository(database)

    def add_enrollment(self, enrollment: Enrollment) -> Enrollment:
        return self.repository.add(enrollment)

    def get_enrollments(self) -> list[Enrollment]:
        return self.repository.list()
