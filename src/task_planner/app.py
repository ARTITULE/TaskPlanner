import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from task_planner.ui.main_window import MainWindow

from task_planner.ui.main_window import MainWindow
from task_planner.auth.auth_manager import AuthManager
from task_planner.ui.login_window import LoginWindow



def run_app():

    app = QApplication(sys.argv)


    stack = QStackedWidget()

    auth_manager = AuthManager()

    login_window = LoginWindow()
    
    main_window = MainWindow()

    stack.addWidget(login_window)
    stack.addWidget(main_window)

    def handle_login(username: str, password: str):
        user = auth_manager.login(username=username, password=password)
        if user:
            stack.setCurrentWidget(main_window)

    login_window.login_requested.connect(handle_login)

    stack.resize(1000, 600)

    
    stack.show()

    sys.exit(app.exec_())





