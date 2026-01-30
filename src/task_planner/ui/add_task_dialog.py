from PyQt5.QtWidgets import (
    QDialog,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QScrollArea,
    QSplitter,
    QCheckBox,
    QMenu,
)
from PyQt5.QtCore import Qt, pyqtSignal
from task_planner.models.task import Task


class AddTaskDialog(QDialog):

    task_submitted = pyqtSignal(str, str, object)

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
        self.save_btn = QPushButton("Save Task")
        self.cancel_btn = QPushButton("Cancel")
            
        layout.addWidget(self.dialog_label)
        layout.addWidget(self.task_title)
        layout.addWidget(self.task_description)

        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.save_btn)

        layout.addLayout(button_layout)

        if self.task:
            self.dialog_label.setText("Edit Task")
            self.task_title.setText(self.task.title)
            if self.task.description:
                self.task_description.setText(self.task.description)


        self.setLayout(layout)

        self.save_btn.clicked.connect(self.emit_task)

    def emit_task(self):
        task_title = self.task_title.text().strip()
        task_description = self.task_description.text().strip()

        
        task_id = self.task.id if self.task else None

        if task_title:
            if task_description:
                self.task_submitted.emit(task_title, task_description, task_id)
                

            else:
                self.task_submitted.emit(task_title, None, task_id)
            self.task_title.clear()
            self.task_description.clear()
            self.accept()
