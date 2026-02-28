from PyQt5.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QLabel, 
)
from PyQt5.QtCore import pyqtSignal
from task_planner.ui.widgets import MenuButton
from task_planner.config import USER_WINDOW_ICONS


class UserWindow(QWidget):

    login_requested = pyqtSignal()
    signup_requested = pyqtSignal()
    logout_requested = pyqtSignal()

    def __init__(self, auth_manager):
        super().__init__()

        self.auth_manager = auth_manager

        self.setWindowTitle("User")
        self.setFixedSize(350, 250)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(10)

        self.status_label = QLabel()
        self.status_label.setObjectName("user_status_label")
        self.layout.addWidget(self.status_label)

        self.login_btn = MenuButton("Login", USER_WINDOW_ICONS.get("Login"))
        self.signup_btn = MenuButton("Sign up", USER_WINDOW_ICONS.get("Sign Up"))
        self.logout_btn = MenuButton("Logout", USER_WINDOW_ICONS.get("Logout"))

        self.layout.addWidget(self.login_btn)
        self.layout.addWidget(self.signup_btn)
        self.layout.addWidget(self.logout_btn)

        self.login_btn.clicked.connect(self.login_requested.emit)
        self.signup_btn.clicked.connect(self.signup_requested.emit)
        self.logout_btn.clicked.connect(self.logout_requested.emit)

        self.refresh_ui()

    def refresh_ui(self):
        user = self.auth_manager.get_current_user()

        if user:
            self.status_label.setText(f"Logged in as {user.username}")
            self.login_btn.hide()
            self.signup_btn.hide()
            self.logout_btn.show()
        else:
            self.status_label.setText("Not logged in")
            self.login_btn.show()
            self.signup_btn.show()
            self.logout_btn.hide()
