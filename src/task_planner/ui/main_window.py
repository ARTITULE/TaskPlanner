from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QListWidget,
    QListWidgetItem
)
from PyQt5.QtCore import Qt

from task_planner.controllers.task_manager import TaskManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Task Planner")
        self.resize(400, 400)

        self.task_manager = TaskManager()

        # Widgets
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter a task")

        self.add_button = QPushButton("Add task")
        self.delete_button = QPushButton("Delete selected")

        self.task_list = QListWidget()

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.task_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.task_list)
        layout.addWidget(self.delete_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setStyleSheet("""

            QPushButton#add_button{
                font-family : arial;
                font-size : 40px
            }
            QLineEdit{
                min-height: 50px;
                font-size : 30px
            }
            QListWidget{
                font-size : 20px
            }

        """)

        # Signals
        self.add_button.clicked.connect(self.add_task)
        self.delete_button.clicked.connect(self.delete_task)
        self.task_list.itemChanged.connect(self.on_item_changed)

    def add_task(self):
        title = self.task_input.text().strip()
        if not title:
            return

        task = self.task_manager.add_task(title)

        item = QListWidgetItem(task.title)
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(Qt.Unchecked)

        self.task_list.addItem(item)
        self.task_input.clear()

    def delete_task(self):
        row = self.task_list.currentRow()
        if row < 0:
            return

        self.task_manager.delete_task(row)
        self.task_list.takeItem(row)

    def on_item_changed(self, item: QListWidgetItem):
        row = self.task_list.row(item)
        completed = item.checkState() == Qt.Checked
        self.task_manager.set_completed(row, completed)
