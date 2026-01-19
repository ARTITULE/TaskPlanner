from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton
)
from PyQt5.QtCore import pyqtSignal

class LoginWindow(QWidget):

    login_requested = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_btn = QPushButton("Login")

        layout.addWidget(QLabel("Login"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)

        self.login_btn.clicked.connect(self.emit_login)

    def emit_login(self):
        self.login_requested.emit(
            self.username_input.text(),
            self.password_input.text()
        )
