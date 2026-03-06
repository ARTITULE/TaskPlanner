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


class LoginDialog(QDialog):

    login_requested = pyqtSignal(str, str)
    signup_requested = pyqtSignal()

    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle("Login")
        self.setModal(True)
        self.setMinimumWidth(400)

        self.login_label = QLabel("Login")
        self.login_label.setObjectName("login_label")

        self.email_label = QLabel("Email")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")

        self.password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.toggle_password_action = self.password_input.addAction(
            QIcon(PASSWORD_ICONS.get("Hidden")), QLineEdit.TrailingPosition
        )
        self.toggle_password_action.triggered.connect(self.toggle_password_visibility)

        self.login_button = QPushButton("Login")
        self.login_button.setObjectName("login_button")
        self.login_button.setCursor(Qt.PointingHandCursor)

        self.signup_container = QHBoxLayout()
        self.signup_label = QLabel("Don't have an account?")
        self.signup_button = QPushButton("Create account")
        self.signup_button.setObjectName("signup_link_button")
        self.signup_button.setCursor(Qt.PointingHandCursor)
        self.signup_container.addWidget(self.signup_label)
        self.signup_container.addWidget(self.signup_button)
        self.signup_container.addStretch()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(15)
        
        layout.addWidget(self.login_label)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addLayout(self.signup_container)

        self.login_button.clicked.connect(self.handle_login)
        self.signup_button.clicked.connect(self.signup_requested.emit)

    def toggle_password_visibility(self):
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_password_action.setIcon(QIcon(PASSWORD_ICONS.get("Visible")))
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.toggle_password_action.setIcon(QIcon(PASSWORD_ICONS.get("Hidden")))

    def handle_login(self):
        self.login_requested.emit(
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

    


        





