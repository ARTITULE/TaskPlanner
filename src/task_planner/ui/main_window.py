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



class TaskWidget(QWidget):

    request_delete = pyqtSignal(QWidget)

    def __init__(self, text: str, parent=None):
        super().__init__(parent)

        self.checkbox = QCheckBox()
        self.label = QLabel(text)
        self.label.setWordWrap(True)


        self.menu_button = QPushButton("⋮")
        self.menu_button.setFixedWidth(64)
        self.menu_button.setFlat(True)


        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 2, 6, 2)
        layout.addWidget(self.checkbox)
        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(self.menu_button)

        self.checkbox.stateChanged.connect(self.update_style)
        self.menu_button.clicked.connect(self.show_menu)

    def update_style(self):
        if self.checkbox.isChecked():
            self.label.setStyleSheet(
                "color: gray; text-decoration: line-through;"
            )
        else:
            self.label.setStyleSheet("")

    def show_menu(self):
        menu = QMenu(self)
        delete_action = menu.addAction("Delete")

        action = menu.exec_(
            self.menu_button.mapToGlobal(
                self.menu_button.rect().bottomLeft()
            )
        )

        if action == delete_action:
            self.request_delete.emit(self)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Task Planner")
        self.resize(1000, 600)

        
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        

        self.home_page = self.init_ui()
        
        
        self.add_task_page = AddTaskWindow()
        
        
        self.stack.addWidget(self.home_page)     
        self.stack.addWidget(self.add_task_page) 
        
        
        self.add_task_page.task_submitted.connect(self.add_task_to_list)
        self.add_task_page.save_btn.clicked.connect(self.go_to_home)
        
        
        

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

    def add_task_to_list(self, text):

        new_task = TaskWidget(text)
        new_task.request_delete.connect(self.remove_task)
        self.task_layout.insertWidget(self.task_layout.count() - 1, new_task)
        

    def remove_task(self, task: QWidget):
        task.setParent(None)
        task.deleteLater()


    def go_to_home(self):
        self.stack.setCurrentIndex(0)
