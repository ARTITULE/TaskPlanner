from PyQt5.QtWidgets import (
    
    QDialog,
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
from PyQt5.QtCore import pyqtSignal


class LoginDialog(QDialog):

    login_requested = pyqtSignal(str, str)
    signup_requested = pyqtSignal()

    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle("Login")
        self.setModal(True)
        self.resize(400, 200)

        self.login_label = QLabel("Login")

        self.email_label = QLabel("Email")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText = "Enter your email"

        self.password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText = "Enter your password"

        self.login_button = QPushButton("Login")
        self.signup_label = QLabel("Don't have a account?")
        self.signup_button = QPushButton("Create account")

        layout = QVBoxLayout(self)
        layout.addWidget(self.login_label)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.signup_label)
        layout.addWidget(self.signup_button)

        self.login_button.clicked.connect(self.handle_login)
        self.signup_button.clicked.connect(self.signup_requested.emit)


    def handle_login(self):
        self.login_requested.emit(
            self.email_input.text(),
            self.password_input.text()
        )


    


        





