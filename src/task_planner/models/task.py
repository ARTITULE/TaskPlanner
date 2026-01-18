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
from dataclasses import dataclass


@dataclass
class Task:
    id: str
    title: str
    completed: bool = False

class TaskWidget(QWidget):

    request_delete = pyqtSignal(QWidget)

    def __init__(self, title: str, description: str, parent=None):
        super().__init__(parent)

        self.checkbox = QCheckBox()
        self.task_title = QLabel(title)
        self.task_description = QLabel(description)
        


        self.menu_button = QPushButton("⋮")
        self.menu_button.setFixedWidth(64)
        self.menu_button.setFlat(True)


        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 2, 6, 2)
        layout.addWidget(self.checkbox)
        layout.addWidget(self.task_title)
        layout.addStretch()
        layout.addWidget(self.menu_button)

        self.checkbox.stateChanged.connect(self.update_style)
        self.menu_button.clicked.connect(self.show_menu)

    def update_style(self):
        if self.checkbox.isChecked():
            self.task_title.setStyleSheet(
                "color: gray; text-decoration: line-through;"
            )
        else:
            self.task_title.setStyleSheet("")

    def show_menu(self):
        menu = QMenu(self)
        delete_action = menu.addAction("Delete")

        action = menu.exec_(
            self.menu_button.mapToGlobal(
                self.menu_button.rect().bottomLeft()
            )
        )

        if action == delete_action:
            self.request_delete.emit(self)
