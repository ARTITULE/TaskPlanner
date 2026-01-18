from PyQt5.QtWidgets import (
    QMainWindow,
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


class AddTaskWindow(QWidget):

    task_submitted = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.task_title = QLineEdit(placeholderText="Task name")
        self.task_description = QLineEdit(placeholderText="Task description")
        self.save_btn = QPushButton("Save Task")
        
        layout.addWidget(QLabel("Add New Task"))
        layout.addWidget(self.task_title)
        layout.addWidget(self.task_description)
        layout.addWidget(self.save_btn)
        self.setLayout(layout)

        self.save_btn.clicked.connect(self.emit_task)

    def emit_task(self):
        task_title = self.task_title.text().strip()
        task_description = self.task_description.text().strip()
        if task_title:
            if task_description:
                self.task_submitted.emit(task_title, task_description)

            else:
                self.task_submitted.emit(task_title, None)
            self.task_title.clear()
            self.task_description.clear()
