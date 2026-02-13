from PyQt5.QtWidgets import (
    QMainWindow,
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
from PyQt5.QtCore import Qt, pyqtSignal
from task_planner.ui.add_task_dialog import AddTaskDialog
from task_planner.models.task import TaskWidget
from task_planner.controllers.task_manager import TaskManager
from task_planner.ui.user_window import UserWindow
from task_planner.models.task import Task
from datetime import date
from task_planner.ui.day_view import DayView
from task_planner.ui.calendar_view import CalendarView








class MainWindow(QMainWindow):
    def __init__(self, auth_manager):
        super().__init__()

        self.auth_manager = auth_manager
        self.task_manager = TaskManager(auth_manager=auth_manager)

        self.setWindowTitle("Task Planner")
        self.resize(1000, 600)

        self.init_ui()
         

           
        

        self.statusBar()
        self.update_status_bar()
        self.day_view.set_date(date.today())


        

    def init_ui(self):
        
        self.today_btn = QPushButton("Today")
        self.calendar_btn = QPushButton("Calendar")
        self.groups_btn = QPushButton("Groups")

        self.settings_btn = QPushButton("Settings")
        self.user_btn = QPushButton("User")

        




        self.content_stack = QStackedWidget()

        self.day_view = DayView(
            task_manager=self.task_manager,
            open_add_dialog=self.open_add_task_dialog,
            open_edit_dialog=self.open_edit_task_dialog,
        )

        self.calendar_view = CalendarView()
        self.user_page = UserWindow(auth_manager=self.auth_manager)

        self.content_stack.addWidget(self.day_view)
        self.content_stack.addWidget(self.calendar_view)
        self.content_stack.addWidget(self.user_page)


        self.today_btn.clicked.connect(self.show_today)
        self.calendar_btn.clicked.connect(self.show_calendar)
        self.calendar_view.date_selected.connect(self.on_date_selected)
        self.user_btn.clicked.connect(self.show_user_page)
        
        sidebar_layout = QVBoxLayout()
        sidebar_layout.addWidget(QLabel("Navigation"))
        sidebar_layout.addWidget(self.today_btn)
        sidebar_layout.addWidget(self.calendar_btn)
        sidebar_layout.addWidget(self.groups_btn)
        sidebar_layout.addStretch()

        settings_btn_layout = QHBoxLayout()
        settings_btn_layout.addWidget(self.settings_btn)
        settings_btn_layout.addWidget(self.user_btn)

        sidebar_layout.addLayout(settings_btn_layout)


        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar_layout)


        
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(sidebar_widget)
        splitter.addWidget(self.content_stack)
        splitter.setSizes([220, 780])

        
        self.setCentralWidget(splitter)



    def open_add_task_dialog(self):
        dialog = AddTaskDialog()
        dialog.task_submitted.connect(self.handle_task_submitted)
        dialog.exec_()


    def open_edit_task_dialog(self, task_id: str):
        task = self.task_manager.get_task(task_id)

        if not task:
            return
        
        dialog = AddTaskDialog(task=task, parent=self)
        dialog.task_submitted.connect(self.handle_task_submitted)
        dialog.exec_()
        


    def handle_task_submitted(self, title, description, task_id, category, exp_time):

        if task_id:
            self.task_manager.update_task(
                task_id=task_id,
                title=title,
                description=description,
                exp_time=exp_time,
                category=category,
            )
        else:
            self.task_manager.add_task(
                title=title,
                description=description,
                exp_time=exp_time,
                category=category,
            )

        self.day_view.refresh_tasks()

    def show_today(self):
        self.day_view.set_date(date.today())
        self.content_stack.setCurrentWidget(self.day_view)

    def show_calendar(self):
        self.content_stack.setCurrentWidget(self.calendar_view)

    def show_user_page(self):
        self.content_stack.setCurrentWidget(self.user_page)

    def on_date_selected(self, selected_date):
        self.day_view.set_date(selected_date)
        self.content_stack.setCurrentWidget(self.day_view)






#    def on_user_logged_in(self, user):
#        self.statusBar().showMessage(f"Logged in as {user.username}")


    def update_status_bar(self):
        user = self.auth_manager.get_current_user()

        if user:
            self.statusBar().showMessage(f"Logged in as {user.username}")
        else:
            self.statusBar().showMessage("Login to see your tasks")

