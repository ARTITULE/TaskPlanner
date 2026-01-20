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

class SignupDialog(QDialog):

    signup_requested = pyqtSignal(str, str, str, str)
    login_requested = pyqtSignal()

    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle("Sign Up")
        self.setModal(True)
        self.resize(400, 200)

        self.signup_label = QLabel("Sign Up")

        self.name_label = QLabel("Name")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText = "Name"

        self.surname_label = QLabel("Surname")
        self.surname_input = QLineEdit()
        self.surname_input.setPlaceholderText = "Surname"

        self.email_label = QLabel("Email")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText = "Email"

        self.password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText = "Password"

        self.signup_button = QPushButton("Create account")
        self.login_label = QLabel("Already have a account")
        self.login_button = QPushButton("Login")

        layout = QVBoxLayout(self)
        layout.addWidget(self.signup_label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.surname_label)
        layout.addWidget(self.surname_input)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.signup_button)
        layout.addWidget(self.login_label)
        layout.addWidget(self.login_button)

        self.signup_button.clicked.connect(self.handle_signup)
        self.login_button.clicked.connect(self.login_requested.emit)


    def handle_signup(self):
        self.signup_requested.emit(
            self.name_input.text(),
            self.surname_input.text(),
            self.password_input.text(),
            self.password_input.text()
        )







