from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QMouseEvent, QIcon


class AddTaskWidget(QWidget):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setMinimumHeight(60)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        self.title_label = QLabel("+ Add a task")
        font = QFont()
        self.title_label.setFont(font)

        layout.addWidget(self.title_label)
        layout.addStretch()

        self.setStyleSheet(
            """
            AddTaskWidget {
                background-color: #f0f0f0;
                border: 1px dashed #aaa;
                border-radius: 5px;
            }
            AddTaskWidget:hover {
                background-color: #e0e0e0;
            }
        """
        )
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()


class MenuButton(QPushButton):
    def __init__(self, text, icon_path, parent=None):
        super().__init__(text, parent)
        self.setFlat(True)
        self.setCursor(Qt.PointingHandCursor)
        
        if icon_path:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(16, 16))

        self.setStyleSheet(
            """
            QPushButton {
                text-align: left;
                padding: 8px;
                border: none;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #444;
            }
        """
        )


class CheckMarkWidget(QPushButton):
    state_changed = pyqtSignal(bool)

    def __init__(self, checked_icon_path, unchecked_icon_path, checked=False, parent=None):
        super().__init__(parent)
        self.checked_icon = QIcon(checked_icon_path)
        self.unchecked_icon = QIcon(unchecked_icon_path)
        self.is_checked = checked
        
        self.setFlat(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(32, 32)
        self.setIconSize(QSize(24, 24))
        
        self.clicked.connect(self.toggle_state)
        self.update_icon()

    def toggle_state(self):
        self.is_checked = not self.is_checked
        self.update_icon()
        self.state_changed.emit(self.is_checked)

    def setChecked(self, checked):
        if self.is_checked != checked:
            self.is_checked = checked
            self.update_icon()

    def isChecked(self):
        return self.is_checked

    def update_icon(self):
        self.setIcon(self.checked_icon if self.is_checked else self.unchecked_icon)

