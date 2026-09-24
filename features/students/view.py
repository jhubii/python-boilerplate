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

from .model import Student


class StudentView(QWidget):
    def __init__(self, service):
        super().__init__()
        self.setObjectName("studentView")
        self.service = service
        self.build_ui()
        self.setStyleSheet(Path(__file__).with_name("style.qss").read_text())
        self.refresh()

    def build_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        form.addRow("Name", self.name_input)
        form.addRow("Email", self.email_input)
        layout.addLayout(form)

        button = QPushButton("Add Student")
        button.setObjectName("primaryButton")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Email"])
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        layout.addWidget(self.table)

    def add_student(self):
        try:
            student = Student(self.name_input.text(), self.email_input.text())
        except ValueError as error:
            QMessageBox.warning(self, "Invalid Student", str(error))
            return
        self.service.add_student(student)
        self.name_input.clear()
        self.email_input.clear()
        self.refresh()

    def refresh(self):
        students = self.service.get_students()
        self.table.setRowCount(len(students))
        for row, student in enumerate(students):
            values = [student.id, student.name, student.email]
            for column, value in enumerate(values):
                self.table.setItem(row, column, QTableWidgetItem(str(value)))
