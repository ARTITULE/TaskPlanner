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

    def handle_login(email: str, password:str):
        
        user = auth_manager.login(email=email, password=password)
        print(auth_manager.get_current_user())
        if user:
            main_window.on_user_logged_in(user)
            login_dialog.accept()
#        else:
#            login_dialog.show_error("Login failed", "Invalid credentials")


        

    def open_signup():
        signup_dialog = SignupDialog(parent=main_window)

        def handle_signup(name, surname, email, password):

            signup_dialog = SignupDialog(parent=main_window)
            success = auth_manager.signup(name=name, surname=surname, email=email, password=password)

            if success:
                signup_dialog.accept()
#            else:
#                signup_dialog.show_error("Sign Up failed", "Invalid credentials")

        signup_dialog.signup_requested.connect(handle_signup)
        signup_dialog.login_requested.connect(handle_login)
        signup_dialog.exec_()

    login_dialog.signup_requested.connect(open_signup)

    login_dialog.login_requested.connect(handle_login)

    login_dialog.exec_()




    sys.exit(app.exec_())






