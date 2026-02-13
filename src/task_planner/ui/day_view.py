from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
)
from PyQt5.QtCore import Qt
from datetime import date
from task_planner.models.task import TaskWidget


class DayView(QWidget):
    def __init__(self, task_manager, open_add_dialog, open_edit_dialog):

        super().__init__()
        self.task_manager = task_manager
        self.open_add_dialog = open_add_dialog
        self.open_edit_dialog = open_edit_dialog
        self.current_date = date.today()

        self.init_ui()
        self.refresh_tasks()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        self.title_label = QLabel()
        self.layout.addWidget(self.title_label)

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter a task")

        self.add_button = QPushButton("+")
        self.add_button.setFixedWidth(32)
        self.add_button.clicked.connect(self.open_add_dialog)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.task_input)
        input_layout.addWidget(self.add_button)

        self.layout.addLayout(input_layout)

        self.task_container = QWidget()
        self.task_layout = QVBoxLayout(self.task_container)
        self.task_layout.setContentsMargins(0, 0, 0, 0)
        self.task_layout.setSpacing(4)
        self.task_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.task_container)
        scroll.setFrameShape(QScrollArea.NoFrame)

        self.layout.addWidget(scroll)

    def set_date(self, selected_date):
        self.current_date = selected_date
        self.title_label.setText(
            f"Tasks for {selected_date.strftime('%A • %d %B %Y')}"
        )
        self.refresh_tasks()

    def refresh_tasks(self):
        for i in reversed(range(self.task_layout.count() - 1)):
            widget = self.task_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()

        tasks = self.task_manager.load_tasks()

        for task in tasks:
            if task.exp_time == self.current_date:
                self.render_task(task)

    def render_task(self, task):
        widget = TaskWidget(task=task)
        widget.request_edit.connect(self.open_edit_dialog)
        widget.request_delete.connect(self.on_task_delete_requested)
        widget.completed_changed.connect(self.task_changed)
        self.task_layout.insertWidget(self.task_layout.count() - 1, widget)

    def on_task_delete_requested(self, task_id: str):

        self.task_manager.delete_task(task_id=task_id)

        for i in range (self.task_layout.count()):
            item = self.task_layout.itemAt(i)
            widget = item.widget()

            if isinstance(widget, TaskWidget) and widget.task_id == task_id:
                widget.setParent(None)
                widget.deleteLater()
                break

    def task_changed(self, task_id: str, completed: bool):
        self.task_manager.set_completed(task_id, completed)