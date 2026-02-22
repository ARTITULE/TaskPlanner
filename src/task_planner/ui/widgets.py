from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QMouseEvent


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
    def __init__(self, text, icon_char, parent=None):
        super().__init__(f"{icon_char}  {text}", parent)
        self.setFlat(True)
        self.setCursor(Qt.PointingHandCursor)
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

