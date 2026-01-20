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
from task_planner.ui.add_task_window import AddTaskWindow
from task_planner.models.task import TaskWidget
from task_planner.controllers.task_manager import TaskManager





class MainWindow(QMainWindow):
    def __init__(self, auth_manager):
        super().__init__()

        self.auth_manager = auth_manager

        self.setWindowTitle("Task Planner")
        self.resize(1000, 600)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        self.home_page = self.init_ui()   
        self.add_task_page = AddTaskWindow()
         
        self.stack.addWidget(self.home_page)     
        self.stack.addWidget(self.add_task_page) 
           
        self.add_task_page.task_submitted.connect(self.add_task_to_list)
        
        self.task_manager = TaskManager()
        

    def init_ui(self):
        
        self.today_btn = QPushButton("Today")
        self.calendar_btn = QPushButton("Calendar")
        self.groups_btn = QPushButton("Groups")

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter a task")

        self.add_button = QPushButton("+")
        self.add_button.setFixedWidth(32)

        self.task_container = QWidget()
        self.task_layout = QVBoxLayout(self.task_container)
        self.task_layout.setContentsMargins(0, 0, 0, 0)
        self.task_layout.setSpacing(4)
        self.task_layout.addStretch() 

        
        self.add_button.clicked.connect(lambda: self.stack.setCurrentIndex(1))



        
        sidebar_layout = QVBoxLayout()
        sidebar_layout.addWidget(QLabel("Navigation"))
        sidebar_layout.addWidget(self.today_btn)
        sidebar_layout.addWidget(self.calendar_btn)
        sidebar_layout.addWidget(self.groups_btn)
        sidebar_layout.addStretch()

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

    def add_task_to_list(self, title, description):

        task = self.task_manager.add_task(title= title, description= description)
        new_task = TaskWidget(task)
        new_task.request_delete.connect(self.on_task_delete_requested)
        new_task.completed_changed.connect(self.task_changed)
        self.task_layout.insertWidget(self.task_layout.count() - 1, new_task)
        self.go_to_home()

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


    def go_to_home(self):
        self.stack.setCurrentIndex(0)

    def on_user_logged_in(self, user):
        self.statusBar().showMessage(f"Logged in as {user.username}")
