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
from task_planner.config import Categories


class AddTaskDialog(QDialog):

    task_submitted = pyqtSignal(str, str, str, str, object)

    def __init__(self, task: Task | None = None, parent=None):

        super().__init__(parent=parent)
        self.setWindowTitle("Add Task")
        self.setMinimumWidth(450)

        self.task = task

        self.init_ui()


    def init_ui(self):
        self.setStyleSheet(
            """
            QDialog {
                background-color: #2B2B2B;
            }
            QLabel {
                color: #BBBBBB;
                font-size: 13px;
                font-family: "sans-serif";
            }
            QLabel#dialog_label {
                color: #FFFFFF;
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            QLineEdit, QDateEdit, QComboBox {
                background-color: #3C3C3C;
                border: 1px solid #5A5A5A;
                border-radius: 5px;
                padding: 8px;
                color: #FFFFFF;
                font-family: "sans-serif";
            }
            QLineEdit:focus, QDateEdit:focus, QComboBox:focus {
                border: 1px solid #4A90E2;
            }
            QPushButton {
                padding: 8px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-family: "sans-serif";
            }
            QPushButton#save_btn {
                background-color: #4A90E2;
                color: white;
                border: none;
            }
            QPushButton#save_btn:hover {
                background-color: #357ABD;
            }
            QPushButton#cancel_btn {
                background-color: transparent;
                color: #BBBBBB;
                border: 1px solid #5A5A5A;
            }
            QPushButton#cancel_btn:hover {
                background-color: #3C3C3C;
                color: white;
            }
            """
        )

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.dialog_label = QLabel("Add New Task")
        self.dialog_label.setObjectName("dialog_label")

        self.task_title = QLineEdit(placeholderText="Task name")
        self.task_description = QLineEdit(placeholderText="Task description")

        self.due_date_label = QLabel("Due date")
        self.due_date_edit = QDateEdit()
        self.due_date_edit.setCalendarPopup(True)
        self.due_date_edit.setDisplayFormat("dd-MM-yyyy")
        self.due_date_edit.setKeyboardTracking(False)
        self.due_date_edit.setDate(QDate.currentDate())
        self.due_date_edit.setMinimumDate(QDate(2000, 1, 1))

        self.category_label = QLabel("Category")
        self.category_box = QComboBox()
        self.category_box.addItems(Categories)

        self.save_btn = QPushButton("Save Task")
        self.save_btn.setObjectName("save_btn")
        self.save_btn.setCursor(Qt.PointingHandCursor)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setObjectName("cancel_btn")
        self.cancel_btn.setCursor(Qt.PointingHandCursor)
            
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
