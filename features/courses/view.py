from pathlib import Path

from PyQt6.QtWidgets import (
    QFormLayout,
    QHeaderView,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .model import Course


class CourseView(QWidget):
    def __init__(self, service):
        super().__init__()
        self.setObjectName("courseView")
        self.service = service
        self.build_ui()
        self.setStyleSheet(Path(__file__).with_name("style.qss").read_text())
        self.refresh()

    def build_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()
        self.code_input = QLineEdit()
        self.name_input = QLineEdit()
        form.addRow("Code", self.code_input)
        form.addRow("Name", self.name_input)
        layout.addLayout(form)

        button = QPushButton("Add Course")
        button.setObjectName("primaryButton")
        button.clicked.connect(self.add_course)
        layout.addWidget(button)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Code", "Name"])
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        layout.addWidget(self.table)

    def add_course(self):
        try:
            course = Course(self.code_input.text(), self.name_input.text())
        except ValueError as error:
            QMessageBox.warning(self, "Invalid Course", str(error))
            return
        self.service.add_course(course)
        self.code_input.clear()
        self.name_input.clear()
        self.refresh()

    def refresh(self):
        courses = self.service.get_courses()
        self.table.setRowCount(len(courses))
        for row, course in enumerate(courses):
            values = [course.id, course.code, course.name]
            for column, value in enumerate(values):
                self.table.setItem(row, column, QTableWidgetItem(str(value)))
