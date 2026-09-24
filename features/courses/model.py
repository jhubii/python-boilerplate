from dataclasses import dataclass


@dataclass
class Course:
    code: str
    name: str
    id: int | None = None

    def __post_init__(self) -> None:
        self.code = self.code.strip().upper()
        self.name = self.name.strip()
        if not self.code:
            raise ValueError("Course code is required.")
        if not self.name:
            raise ValueError("Course name is required.")
