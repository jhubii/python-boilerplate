from pathlib import Path

from PyQt6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHeaderView,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .model import Enrollment


class EnrollmentView(QWidget):
    def __init__(self, enrollment_service, student_service, course_service):
        super().__init__()
        self.setObjectName("enrollmentView")
        self.enrollment_service = enrollment_service
        self.student_service = student_service
        self.course_service = course_service
        self.build_ui()
        self.setStyleSheet(Path(__file__).with_name("style.qss").read_text())
        self.refresh()

    def build_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()
        self.student_input = QComboBox()
        self.course_input = QComboBox()
        self.semester_input = QComboBox()
        self.semester_input.addItems(["1st Semester", "2nd Semester"])
        form.addRow("Student", self.student_input)
        form.addRow("Course", self.course_input)
        form.addRow("Semester", self.semester_input)
        layout.addLayout(form)

        add_button = QPushButton("Add Enrollment")
        add_button.setObjectName("primaryButton")
        add_button.clicked.connect(self.add_enrollment)
        layout.addWidget(add_button)
        refresh_button = QPushButton("Refresh Students and Courses")
        refresh_button.setObjectName("secondaryButton")
        refresh_button.clicked.connect(self.refresh)
        layout.addWidget(refresh_button)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "Student", "Course", "Semester"])
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        layout.addWidget(self.table)

    def add_enrollment(self):
        student = self.student_input.currentData()
        course = self.course_input.currentData()
        try:
            enrollment = Enrollment(student, course, self.semester_input.currentText())
        except ValueError as error:
            QMessageBox.warning(self, "Invalid Enrollment", str(error))
            return
        self.enrollment_service.add_enrollment(enrollment)
        self.semester_input.setCurrentIndex(0)
        self.refresh()

    def refresh(self):
        self.student_input.clear()
        for student in self.student_service.get_students():
            self.student_input.addItem(student.name, student)
        self.course_input.clear()
        for course in self.course_service.get_courses():
            self.course_input.addItem(course.code, course)

        enrollments = self.enrollment_service.get_enrollments()
        self.table.setRowCount(len(enrollments))
        for row, enrollment in enumerate(enrollments):
            values = [
                enrollment.id,
                enrollment.student.name,
                enrollment.course.code,
                enrollment.semester,
            ]
            for column, value in enumerate(values):
                self.table.setItem(row, column, QTableWidgetItem(str(value)))
