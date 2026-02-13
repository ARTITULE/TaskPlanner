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
    QCheckBox,
    QMenu,
)
from PyQt5.QtCore import Qt, pyqtSignal
from task_planner.models.task import Task


class AddTaskDialog(QDialog):

    task_submitted = pyqtSignal(str, str, str, str)

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
        self.category_label = QLabel("Category")
        self.category_box = QComboBox()
        self.category_box.addItems(["None", "Work", "School", "Home"])
        self.save_btn = QPushButton("Save Task")
        self.cancel_btn = QPushButton("Cancel")
            
        layout.addWidget(self.dialog_label)
        layout.addWidget(self.task_title)
        layout.addWidget(self.task_description)
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
            if self.task.category:
                index = self.category_box.findText(self.task.category)
                if index != -1:
                    self.category_box.setCurrentIndex(index=index)


        self.setLayout(layout)

        self.save_btn.clicked.connect(self.emit_task)
        self.cancel_btn.clicked.connect(self.reject)

    def emit_task(self):
        task_title = self.task_title.text().strip()
        task_description = self.task_description.text().strip() or ""
        task_category = self.category_box.currentText()
        task_category = None if task_category == "None" else task_category

        
        task_id = self.task.id if self.task else ""

        if task_title:

            self.task_submitted.emit(task_title, task_description, task_id, task_category)

            self.task_title.clear()
            self.task_description.clear()
            self.accept()
