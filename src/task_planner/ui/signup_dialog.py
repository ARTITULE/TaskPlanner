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
    QMessageBox,
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from task_planner.config import PASSWORD_ICONS

class SignupDialog(QDialog):

    signup_requested = pyqtSignal(str, str, str, str)
    login_requested = pyqtSignal()

    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle("Sign Up")
        self.setModal(True)
        self.setMinimumWidth(400)

        self.signup_title_label = QLabel("Sign Up")
        self.signup_title_label.setObjectName("signup_title_label")

        self.name_label = QLabel("Name")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")

        self.surname_label = QLabel("Surname")
        self.surname_input = QLineEdit()
        self.surname_input.setPlaceholderText("Enter your surname")

        self.email_label = QLabel("Email")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")

        self.password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Create a password")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.toggle_password_action = self.password_input.addAction(
            QIcon(PASSWORD_ICONS.get("Hidden")), QLineEdit.TrailingPosition
        )
        self.toggle_password_action.triggered.connect(self.toggle_password_visibility)

        self.signup_button = QPushButton("Create account")
        self.signup_button.setObjectName("signup_button")
        self.signup_button.setCursor(Qt.PointingHandCursor)

        self.login_container = QHBoxLayout()
        self.login_label = QLabel("Already have an account?")
        self.login_button = QPushButton("Login")
        self.login_button.setObjectName("login_link_button")
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_container.addWidget(self.login_label)
        self.login_container.addWidget(self.login_button)
        self.login_container.addStretch()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(15)
        
        layout.addWidget(self.signup_title_label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.surname_label)
        layout.addWidget(self.surname_input)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.signup_button)
        layout.addLayout(self.login_container)

        self.signup_button.clicked.connect(self.handle_signup)
        self.login_button.clicked.connect(self.login_requested.emit)

    def toggle_password_visibility(self):
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_password_action.setIcon(QIcon(PASSWORD_ICONS.get("Visible")))
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.toggle_password_action.setIcon(QIcon(PASSWORD_ICONS.get("Hidden")))



    def handle_signup(self):
        self.signup_requested.emit(
            self.name_input.text(),
            self.surname_input.text(),
            self.email_input.text(),
            self.password_input.text()
        )

    def show_error(self, title: str, message: str):
        QMessageBox.critical(
            self,
            title,
            message,
            QMessageBox.Ok
        )






