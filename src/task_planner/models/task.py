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
    QMenu,

)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from datetime import date
from dataclasses import dataclass, field
from task_planner.ui.widgets import CheckMarkWidget
from task_planner.config import CHECK_MARK_ICONS, IMPORTANT_ICONS

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
    important_changed = pyqtSignal(str, bool)


    def __init__(self, task: Task, parent=None):
        super().__init__(parent)

        self.checkbox = CheckMarkWidget(
            checked_icon_path=CHECK_MARK_ICONS.get("Checked"),
            unchecked_icon_path=CHECK_MARK_ICONS.get("Unchecked"),
            checked=task.completed
        )
        self.task = task
        self.task_id = task.id

        self.task_title = QLabel(task.title)
        self.task_title.setWordWrap(True)
        title_font = QFont()
        title_font.setFamily("sans-serif")
        title_font.setPointSize(12)
        title_font.setBold(True)
        self.task_title.setFont(title_font)

        self.task_info = QLabel()
        info_font = QFont()
        info_font.setFamily("sans-serif")
        info_font.setPointSize(9)
        self.task_info.setFont(info_font)
        


        self.important_star = CheckMarkWidget(
            checked_icon_path=IMPORTANT_ICONS.get("Filled"),
            unchecked_icon_path=IMPORTANT_ICONS.get("Outline"),
            checked=(task.category == "Important")
        )

        self.menu_button = QPushButton("⋮")
        self.menu_button.setFixedWidth(64)
        self.menu_button.setFlat(True)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 2, 6, 2)
        layout.addWidget(self.checkbox)

        text_layout = QVBoxLayout()
        text_layout.addWidget(self.task_title)
        text_layout.addWidget(self.task_info)
        
        layout.addLayout(text_layout)
        layout.addStretch()
        layout.addWidget(self.important_star)
        layout.addWidget(self.menu_button)

        self.checkbox.state_changed.connect(self.emit_completed)
        self.important_star.state_changed.connect(self.toggle_important)
        self.menu_button.clicked.connect(self.show_menu)

        self.sync_from_task()

    def toggle_important(self, is_important):
        new_category = "Important" if is_important else "None"
        self.task.category = new_category
        self.refresh()
        self.important_changed.emit(self.task_id, is_important)

    def update_icon_color(self, color_hex):
        self.checkbox.update_icon_color(color_hex)
        self.important_star.update_icon_color(color_hex)

    def update_style(self):
        
        if self.task.completed:
            self.task_title.setStyleSheet(
                "color: gray; text-decoration: line-through;"
            )
            self.task_info.setStyleSheet(
                "color: gray; text-decoration: line-through"
            )
        else:
            self.task_title.setStyleSheet("")
            self.task_info.setStyleSheet("color: #888;")

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
        
        info_parts = []
        if self.task.exp_time:
            info_parts.append(self.task.exp_time.strftime("%d/%m"))
        
        if self.task.category and self.task.category != "None":
            info_parts.append(self.task.category)
        
        if info_parts:
            self.task_info.setText(" | ".join(info_parts))
            self.task_info.show()
        else:
            self.task_info.hide()


    def sync_from_task(self):
        self.checkbox.blockSignals(True)
        self.checkbox.setChecked(self.task.completed)
        self.checkbox.blockSignals(False)

        self.refresh()
        self.update_style()
