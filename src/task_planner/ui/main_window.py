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







class MainWindow(QMainWindow):
    def __init__(self, auth_manager):
        super().__init__()

        self.auth_manager = auth_manager

        self.setWindowTitle("Task Planner")
        self.resize(1000, 600)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        self.home_page = self.init_ui()   
        self.user_page = UserWindow(auth_manager=auth_manager)
         
        self.stack.addWidget(self.home_page)     
        self.stack.addWidget(self.user_page)
           
        
        self.task_manager = TaskManager(auth_manager=auth_manager)

        self.statusBar()
        self.update_status_bar()
        self.load_tasks()

        

    def init_ui(self):
        
        self.today_btn = QPushButton("Today")
        self.calendar_btn = QPushButton("Calendar")
        self.groups_btn = QPushButton("Groups")

        self.settings_btn = QPushButton("Settings")
        self.user_btn = QPushButton("User")

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter a task")

        self.add_button = QPushButton("+")
        self.add_button.setFixedWidth(32)

        self.task_container = QWidget()
        self.task_layout = QVBoxLayout(self.task_container)
        self.task_layout.setContentsMargins(0, 0, 0, 0)
        self.task_layout.setSpacing(4)
        self.task_layout.addStretch() 

        
        self.add_button.clicked.connect(self.open_add_task_dialog)
        self.user_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.user_page))




        
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

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.task_input)
        input_layout.addWidget(self.add_button)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.task_container)
        scroll.setFrameShape(QScrollArea.NoFrame)

        app_layout = QVBoxLayout()
        app_layout.addWidget(QLabel("Tasks for Today"))
        app_layout.addLayout(input_layout)
        app_layout.addWidget(scroll)

        main_widget = QWidget()
        main_widget.setLayout(app_layout)

        
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(sidebar_widget)
        splitter.addWidget(main_widget)
        splitter.setSizes([220, 780])

        
        return splitter


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
        


    def handle_task_submitted(self, title, description, task_id, category):

        if task_id:  # EDIT
            self.task_manager.update_task(
                task_id=task_id,
                title=title,
                description=description,
                category=category,
            )

            for i in range(self.task_layout.count()):
                widget = self.task_layout.itemAt(i).widget()
                if isinstance(widget, TaskWidget) and widget.task_id == task_id:
                    widget.refresh()
                    break

        else:  # CREATE
            task = self.task_manager.add_task(
                title=title,
                description=description,
                category=category,
            )
            self.render_task(task)



    def render_task(self, task: Task):
        task_to_load = TaskWidget(task=task)
        task_to_load.request_delete.connect(self.on_task_delete_requested)
        task_to_load.request_edit.connect(self.open_edit_task_dialog)
        task_to_load.completed_changed.connect(self.task_changed)
        self.task_layout.insertWidget(self.task_layout.count() - 1, task_to_load)


    def apply_task_update(self, title, description, task_id):
        
        self.task_manager.update_task(
            task_id=task_id,
            title=title,
            description=description,
            
        )

        for i in range(self.task_layout.count()):
            widget = self.task_layout.itemAt(i).widget()
            if isinstance(widget, TaskWidget) and widget.task_id == task_id:
                widget.refresh()
                break


    def task_changed(self, task_id: str, completed: bool):
        self.task_manager.set_completed(task_id, completed)


    def on_task_delete_requested(self, task_id: str):

        self.task_manager.delete_task(task_id=task_id)

        for i in range (self.task_layout.count()):
            item = self.task_layout.itemAt(i)
            widget = item.widget()

            if isinstance(widget, TaskWidget) and widget.task_id == task_id:
                widget.setParent(None)
                widget.deleteLater()
                break


    def load_tasks(self):
        tasks = self.task_manager.load_tasks()
        for task in tasks:
            self.render_task(task=task)

#    def on_user_logged_in(self, user):
#        self.statusBar().showMessage(f"Logged in as {user.username}")


    def update_status_bar(self):
        user = self.auth_manager.get_current_user()

        if user:
            self.statusBar().showMessage(f"Logged in as {user.username}")
        else:
            self.statusBar().showMessage("Login to see your tasks")

