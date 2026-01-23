from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QScrollArea,
    QSplitter,
    QCheckBox,
    QMenu,

)
from PyQt5.QtCore import Qt, pyqtSignal
import uuid
from dataclasses import dataclass, field

@dataclass
class Task:
    id: str 
    title: str
    description: str | None = None
    exp_time = None
    creator_name = None
    category = None
    completed: str = "completed"
    deleted: bool = False

    def to_dict(self) -> dict:
        return {
            #"uuid": self.id,
            "title": self.title,
            "description": self.description,
            "exp_time": self.exp_time,
            #"creator_name": self.creator_name,
            "category": self.category,
            "completed": self.completed,
            #"deleted": self.deleted,
        }



class TaskWidget(QWidget):

    request_delete = pyqtSignal(str)
    completed_changed = pyqtSignal(str, bool)


    def __init__(self, task: Task, parent=None):
        super().__init__(parent)

        self.checkbox = QCheckBox()
        self.task = task
        self.task_id = task.id

        self.task_title = QLabel(task.title)
        self.task_title.setWordWrap(True)

        if task.description:
            self.task_description = QLabel(task.description)
            self.task_description.setWordWrap(True)
        else:
            self.task_description = None
        


        self.menu_button = QPushButton("⋮")
        self.menu_button.setFixedWidth(64)
        self.menu_button.setFlat(True)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 2, 6, 2)
        layout.addWidget(self.checkbox)

        text_layout = QVBoxLayout()
        text_layout.addWidget(self.task_title)

        if self.task.description:
            text_layout.addWidget(self.task_description)
        
        layout.addLayout(text_layout)
        layout.addStretch()
        layout.addWidget(self.menu_button)

        self.checkbox.stateChanged.connect(self.update_style)
        self.checkbox.stateChanged.connect(self.emit_completed)
        self.menu_button.clicked.connect(self.show_menu)

    def update_style(self):
        self.task.completed = self.checkbox.isChecked()
        if self.task.completed:
            self.task_title.setStyleSheet(
                "color: gray; text-decoration: line-through;"
            )
        else:
            self.task_title.setStyleSheet("")

    def emit_completed(self):
        self.completed_changed.emit(
            self.task_id,
            self.checkbox.isChecked()
        )

    def show_menu(self):
        menu = QMenu(self)
        delete_action = menu.addAction("Delete")

        action = menu.exec_(
            self.menu_button.mapToGlobal(
                self.menu_button.rect().bottomLeft()
            )
        )

        if action == delete_action:
            self.request_delete.emit(self.task_id)
