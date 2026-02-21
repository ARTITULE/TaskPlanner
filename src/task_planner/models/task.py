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
from PyQt5.QtGui import QFont
from datetime import date
from dataclasses import dataclass, field

@dataclass
class Task:
    id: str 
    title: str
    description: str | None = None
    exp_time: str | None = None
    category: str | None = None
    completed: bool = False

    def to_dict(self) -> dict:
        return {
            "uuid": self.id,
            "title": self.title,
            "description": self.description,
            "exp_time": self.exp_time.isoformat() if self.exp_time else None,
            "category": self.category,
            "completed": self.completed,
        }



class TaskWidget(QWidget):

    request_delete = pyqtSignal(str)
    request_edit = pyqtSignal(str)
    completed_changed = pyqtSignal(str, bool)


    def __init__(self, task: Task, parent=None):
        super().__init__(parent)

        self.checkbox = QCheckBox()
        self.task = task
        self.task_id = task.id

        self.task_title = QLabel(task.title)
        self.task_title.setWordWrap(True)
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        self.task_title.setFont(title_font)

        if task.description:
            self.task_description = QLabel(task.description)
            self.task_description.setWordWrap(True)
            desc_font = QFont()
            desc_font.setPointSize(9)
            self.task_description.setFont(desc_font)
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

        self.checkbox.stateChanged.connect(self.emit_completed)
        self.menu_button.clicked.connect(self.show_menu)

        self.sync_from_task()

    def update_style(self):
        
        if self.task.completed:
            self.task_title.setStyleSheet(
                "color: gray; text-decoration: line-through;"
            )
            if self.task_description:
                self.task_description.setStyleSheet(
                    "color: gray; text-decoration: line-through"
                )
        else:
            self.task_title.setStyleSheet("")
            self.task_description.setStyleSheet("") if self.task_description else None

    def emit_completed(self):
        completed = self.checkbox.isChecked()

        self.task.completed = completed
        self.update_style()
        
        self.completed_changed.emit(
            self.task_id,
            self.checkbox.isChecked()
        )

    def show_menu(self):
        menu = QMenu(self)
        delete_action = menu.addAction("Delete")
        update_action = menu.addAction("Edit task")

        action = menu.exec_(
            self.menu_button.mapToGlobal(
                self.menu_button.rect().bottomLeft()
            )
        )

        if action == delete_action:
            self.request_delete.emit(self.task_id)

        if action == update_action:
            self.request_edit.emit(self.task_id)


    def refresh(self):

        self.task_title.setText(self.task.title)
        if self.task_description:
            self.task_description.setText(self.task.description)


    def sync_from_task(self):
        self.checkbox.blockSignals(True)
        self.checkbox.setChecked(self.task.completed)
        self.checkbox.blockSignals(False)

        self.update_style()
