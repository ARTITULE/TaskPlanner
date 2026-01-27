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


    def open_login():
        login_dialog = LoginDialog(parent=main_window)
        
        def handle_login(email: str, password:str):
            
            user = auth_manager.login(email=email, password=password)
            print(auth_manager.get_current_user())
            if user:
                main_window.update_status_bar()
                main_window.user_page.refresh()
                login_dialog.accept()
            else:
                login_dialog.show_error("Login failed", "Invalid credentials")

        login_dialog.signup_requested.connect(open_signup)
        login_dialog.login_requested.connect(handle_login)
        login_dialog.exec_()

        

    def open_signup():
        signup_dialog = SignupDialog(parent=main_window)

        def handle_signup(name, surname, email, password):

            success = auth_manager.signup(name=name, surname=surname, email=email, password=password)

            if success:
                signup_dialog.accept()
            else:
                signup_dialog.show_error("Sign Up failed", "Invalid credentials")

        signup_dialog.signup_requested.connect(handle_signup)
        signup_dialog.login_requested.connect(open_login)
        signup_dialog.exec_()


    def handle_logout():
        auth_manager.logout()
        main_window.update_status_bar()
        main_window.user_page.refresh()


    main_window.user_page.login_requested.connect(open_login)
    main_window.user_page.signup_requested.connect(open_signup)
    main_window.user_page.logout_requested.connect(handle_logout)


    sys.exit(app.exec_())






