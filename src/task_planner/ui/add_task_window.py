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

    task_submitted = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.input = QLineEdit(placeholderText="What needs to be done?")
        self.save_btn = QPushButton("Save Task")
        
        layout.addWidget(QLabel("Add New Task"))
        layout.addWidget(self.input)
        layout.addWidget(self.save_btn)
        self.setLayout(layout)

        self.save_btn.clicked.connect(self.emit_task)

    def emit_task(self):
        text = self.input.text().strip()
        if text:
            self.task_submitted.emit(text)
            self.input.clear()
