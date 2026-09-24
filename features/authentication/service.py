from database.database import Database
from .model import User
from .repository import AuthenticationRepository


class AuthenticationService:
    def __init__(self, database: Database):
        self.repository = AuthenticationRepository(database)
        self.current_user: User | None = None

    def register(self, username: str, password: str, confirmation: str) -> User:
        user = User(username)
        self._validate_password(password, confirmation)
        return self.repository.add(user, password)

    def authenticate(self, username: str, password: str) -> User:
        user = User(username)
        record = self.repository.find_by_username(user.username)
        if record is None:
            raise ValueError("Invalid username or password.")
        saved_user, saved_password = record
        if password != saved_password:
            raise ValueError("Invalid username or password.")
        self.current_user = saved_user
        return saved_user

    def logout(self) -> None:
        self.current_user = None

    def _validate_password(self, password: str, confirmation: str) -> None:
        if len(password) < 8:
            raise ValueError("Password must have at least 8 characters.")
        if password != confirmation:
            raise ValueError("Passwords do not match.")
