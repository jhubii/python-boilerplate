from dataclasses import dataclass
import re

_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass
class Student:
    name: str
    email: str
    id: int | None = None

    def __post_init__(self) -> None:
        self.name = self.name.strip()
        self.email = self.email.strip().lower()
        if not self.name:
            raise ValueError("Student name is required.")
        if len(self.name) < 2:
            raise ValueError("Student name must have at least 2 characters.")
        if not _EMAIL_PATTERN.fullmatch(self.email):
            raise ValueError("Enter a valid email address.")
