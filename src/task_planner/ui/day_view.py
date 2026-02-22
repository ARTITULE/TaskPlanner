from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QFrame,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QMouseEvent
from task_planner.models.task import TaskWidget
from task_planner.ui.widgets import AddTaskWidget
from datetime import date, timedelta


class DayView(QWidget):
    def __init__(self, task_manager, open_add_dialog, open_edit_dialog):
        super().__init__()

        self.task_manager = task_manager
        self.open_add_dialog = open_add_dialog
        self.open_edit_dialog = open_edit_dialog
        self.current_date = date.today()
        self.view_mode = "day"

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.date_label = QLabel(f"My Day, {self.current_date.strftime('%B %d')}")
        self.date_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        date_font = QFont()
        date_font.setFamily("sans-serif")
        date_font.setPointSize(50)
        self.date_label.setFont(date_font)
        self.date_label.setStyleSheet(
            """
            QLabel {
                background-color: #3C3C3C;
                color: white;
                padding: 40px;
                border-left: 1px solid #5A5A5A;
                border-right: 1px solid #5A5A5A;
                border-bottom: 1px solid #5A5A5A;
            }
            """
        )

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)

        self.task_list_widget = QWidget()
        self.task_list_layout = QVBoxLayout(self.task_list_widget)
        self.task_list_layout.setContentsMargins(10, 5, 10, 5)
        self.task_list_layout.setSpacing(5)

        self.add_task_widget = AddTaskWidget()
        self.add_task_widget.clicked.connect(self.open_add_dialog)
        self.task_list_layout.addWidget(self.add_task_widget)

        self.task_list_layout.addStretch()

        self.scroll_area.setWidget(self.task_list_widget)

        main_layout.addWidget(self.date_label)
        main_layout.addWidget(self.scroll_area)

        self.setLayout(main_layout)

    def set_date(self, new_date):
        self.view_mode = "day"
        self.add_task_widget.show()
        self.current_date = new_date
        if new_date == date.today():
            self.date_label.setText(
                f"My Day<br><span style='font-size: 30pt;'>{self.current_date.strftime('%B %d')}</span>"
            )
        else:
            self.date_label.setText(self.current_date.strftime('%B %d'))
        self.refresh_tasks()

    def show_all_tasks(self):
        self.view_mode = "all_tasks"
        self.add_task_widget.show()
        self.date_label.setText("Tasks")
        self.refresh_tasks()

    def show_completed_tasks(self):
        self.view_mode = "completed"
        self.add_task_widget.hide()
        self.date_label.setText("Completed")
        self.refresh_tasks()

    def refresh_tasks(self):
        # Clear existing task widgets and separators, but not the add task button or stretch
        for i in reversed(range(self.task_list_layout.count())):
            item = self.task_list_layout.itemAt(i)
            widget = item.widget()
            if widget and (isinstance(widget, TaskWidget) or getattr(widget, "is_separator", False)):
                widget.deleteLater()

        tasks = self.task_manager.load_tasks()
        today = date.today()
        seven_days = timedelta(days=7)

        for task in tasks:
            show_task = False
            if self.view_mode == "day":
                if task.exp_time == self.current_date and not task.completed:
                    show_task = True
            elif self.view_mode == "all_tasks":
                if not task.completed:
                    show_task = True
            elif self.view_mode == "completed":
                if task.completed:
                    if task.exp_time is None:
                        show_task = True
                    else:
                        if today - seven_days <= task.exp_time <= today + seven_days:
                            show_task = True

            if show_task:
                task_widget = TaskWidget(task=task)
                task_widget.completed_changed.connect(self.handle_task_completed)
                task_widget.request_delete.connect(self.handle_task_deleted)
                task_widget.request_edit.connect(self.handle_task_edited)
                # Insert new tasks before the "Add Task" button and stretch
                self.task_list_layout.insertWidget(
                    self.task_list_layout.count() - 2, task_widget
                )
                
                # Add separator after each task
                separator = QFrame()
                separator.setFrameShape(QFrame.HLine)
                separator.setFrameShadow(QFrame.Sunken)
                separator.setStyleSheet("color: #eee;")  # Subtle color
                separator.is_separator = True
                self.task_list_layout.insertWidget(
                    self.task_list_layout.count() - 2, separator
                )

    def handle_task_completed(self, task_id: str, completed: bool):
        self.task_manager.set_completed(task_id, completed)
        self.refresh_tasks()

    def handle_task_deleted(self, task_id: str):
        self.task_manager.delete_task(task_id)
        self.refresh_tasks()

    def handle_task_edited(self, task_id: str):
        self.open_edit_dialog(task_id)
