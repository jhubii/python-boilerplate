import sys
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from database.database import Database
from features.authentication.service import AuthenticationService
from features.authentication.view import AuthenticationView
from features.courses.service import CourseService
from features.courses.view import CourseView
from features.enrollments.service import EnrollmentService
from features.enrollments.view import EnrollmentView
from features.students.service import StudentService
from features.students.view import StudentView


class SchoolManagementWindow(QDialog):
    def __init__(self, students, courses, enrollments, authentication):
        super().__init__()
        self.authentication = authentication
        self.logged_out = False
        self.setWindowTitle("School Management System")
        self.resize(820, 560)

        self.setObjectName("mainContent")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 24)
        layout.setSpacing(14)

        header = QWidget()
        header.setObjectName("appHeader")
        header.setMinimumHeight(78)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(22, 14, 18, 14)
        header_layout.setSpacing(16)

        title_group = QVBoxLayout()
        title_group.setSpacing(2)
        title = QLabel("School Management System")
        title.setObjectName("appTitle")
        subtitle = QLabel("Manage students, courses, and enrollments")
        subtitle.setObjectName("appSubtitle")
        title_group.addWidget(title)
        title_group.addWidget(subtitle)
        header_layout.addLayout(title_group, 1)

        logout_button = QPushButton("Log Out")
        logout_button.setObjectName("logoutButton")
        logout_button.setFixedHeight(36)
        logout_button.clicked.connect(self.logout)
        header_layout.addWidget(logout_button)
        layout.addWidget(header)

        tabs = QTabWidget()
        tabs.addTab(StudentView(students), "Students")
        tabs.addTab(CourseView(courses), "Courses")
        tabs.addTab(EnrollmentView(enrollments, students, courses), "Enrollments")
        layout.addWidget(tabs)

    def logout(self):
        if QMessageBox.question(
            self,
            "Log Out",
            "Are you sure you want to log out?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        ) == QMessageBox.StandardButton.Yes:
            self.authentication.logout()
            self.logged_out = True
            self.close()


def main():
    database = Database()
    database.create_tables()

    app = QApplication(sys.argv)
    app.setStyleSheet((Path(__file__).with_name("style.qss")).read_text())

    authentication = AuthenticationService(database)
    students = StudentService(database)
    courses = CourseService(database)
    enrollments = EnrollmentService(database)

    while True:
        login_dialog = AuthenticationView(authentication)
        if login_dialog.exec() != QDialog.DialogCode.Accepted:
            return 0

        window = SchoolManagementWindow(
            students, courses, enrollments, authentication
        )
        window.exec()
        if not window.logged_out:
            return 0


if __name__ == "__main__":
    raise SystemExit(main())
