from PyQt5.QtWidgets import (
    QDialog,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QScrollArea,
    QSplitter,
    QDateEdit,
    QMenu,
)
from PyQt5.QtCore import Qt, pyqtSignal, QDate
from datetime import date
from task_planner.models.task import Task


class AddTaskDialog(QDialog):

    task_submitted = pyqtSignal(str, str, str, str, object)

    def __init__(self, task: Task | None = None, parent=None):

        super().__init__(parent=parent)

        self.task = task

        self.init_ui()


    def init_ui(self):

        layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        self.dialog_label = QLabel("Add New Task")

        self.task_title = QLineEdit(placeholderText="Task name")
        self.task_description = QLineEdit(placeholderText="Task description")

        self.due_date_label = QLabel("Due date")
        self.due_date_edit = QDateEdit()
        self.due_date_edit.setCalendarPopup(True)
        self.due_date_edit.setDisplayFormat("dd-MM-yyyy")
        self.due_date_edit.setSpecialValueText("No due date")
        self.due_date_edit.setDate(QDate.currentDate())
        self.due_date_edit.setMinimumDate(QDate(2000, 1, 1))

        self.category_label = QLabel("Category")
        self.category_box = QComboBox()
        self.category_box.addItems(["None", "Work", "School", "Home"])

        self.save_btn = QPushButton("Save Task")
        self.cancel_btn = QPushButton("Cancel")
            
        layout.addWidget(self.dialog_label)
        layout.addWidget(self.task_title)
        layout.addWidget(self.task_description)
        layout.addWidget(self.due_date_label)
        layout.addWidget(self.due_date_edit)
        layout.addWidget(self.category_label)
        layout.addWidget(self.category_box)

        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(button_layout)

        if self.task:
            self.dialog_label.setText("Edit Task")
            self.task_title.setText(self.task.title)
            if self.task.description:
                self.task_description.setText(self.task.description)
            if self.task.exp_time:
                date = QDate(
                    self.task.exp_time.year,
                    self.task.exp_time.month,
                    self.task.exp_time.day
                )
                self.due_date_edit.setDate(date)
            if self.task.category:
                index = self.category_box.findText(self.task.category)
                if index != -1:
                    self.category_box.setCurrentIndex(index)


        self.setLayout(layout)

        self.save_btn.clicked.connect(self.emit_task)
        self.cancel_btn.clicked.connect(self.reject)

    def emit_task(self):
        task_title = self.task_title.text().strip()
        task_description = self.task_description.text().strip() or ""
        task_category = self.category_box.currentText()
        task_category = None if task_category == "None" else task_category


        date = self.due_date_edit.date()
        exp_time = date.toPyDate() if self.due_date_edit.date() else None

        
        task_id = self.task.id if self.task else ""

        if task_title:

            self.task_submitted.emit(task_title, task_description, task_id, task_category, exp_time)

            self.task_title.clear()
            self.task_description.clear()
            self.accept()
