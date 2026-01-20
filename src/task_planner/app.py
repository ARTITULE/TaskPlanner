import sys
from PyQt5.QtWidgets import QApplication, QDialog
from task_planner.ui.main_window import MainWindow

from task_planner.ui.signup_dialog import SignupDialog
from task_planner.ui.login_dialog import LoginDialog

from task_planner.auth.auth_manager import AuthManager



def run_app():

    app = QApplication(sys.argv)

    auth_manager = AuthManager()

    main_window = MainWindow(auth_manager=auth_manager)
    main_window.show()

    login_dialog = LoginDialog(parent=main_window)

    def handle_login(username: str, password:str):
        user = auth_manager.login(username=username, password=password)
        if user:
            main_window.on_user_logged_in(user)
            login_dialog.accept()
        else:
            login_dialog.show_error("Invalid credentials")

    def open_signup():
        signup = SignupDialog(parent=main_window)

        signup.exec_()

    login_dialog.signup_requested.connect(open_signup)

    login_dialog.login_requested.connect(handle_login)

    login_dialog.exec_()




    sys.exit(app.exec_())






