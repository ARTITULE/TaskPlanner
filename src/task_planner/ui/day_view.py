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
        self.date_label.setObjectName("date_label")
        self.date_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        date_font = QFont()
        date_font.setFamily("sans-serif")
        date_font.setPointSize(50)
        self.date_label.setFont(date_font)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)

        self.task_list_widget = QWidget()
        self.task_list_widget.setObjectName("task_list_content")
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
                f"My Day<br><span style='font-size: 20pt; font-weight: normal; color: #888888;'>{self.current_date.strftime('%B %d')}</span>"
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

    def show_important_tasks(self):
        self.view_mode = "important"
        self.add_task_widget.show()
        self.date_label.setText("Important")
        self.refresh_tasks()

    def refresh_tasks(self):
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
                if task.exp_time == self.current_date:
                    show_task = True
            elif self.view_mode == "all_tasks":
                if not task.completed and not task.exp_time:
                    show_task = True
            elif self.view_mode == "completed":
                if task.completed:
                    if task.exp_time == today:
                        show_task = False
                    elif task.exp_time is None:
                        show_task = True
                    elif today - seven_days <= task.exp_time <= today + seven_days:
                        show_task = True
            elif self.view_mode == "important":
                if task.category == "Important":
                    show_task = True

            if show_task:
                task_widget = TaskWidget(task=task)
                
                # Apply current theme color to task icons
                main_win = self.window()
                if hasattr(main_win, "current_icon_color"):
                    task_widget.update_icon_color(main_win.current_icon_color)
                
                task_widget.completed_changed.connect(self.handle_task_completed)
                task_widget.important_changed.connect(self.handle_task_important)
                task_widget.request_delete.connect(self.handle_task_deleted)
                task_widget.request_edit.connect(self.handle_task_edited)
                self.task_list_layout.insertWidget(
                    self.task_list_layout.count() - 2, task_widget
                )
                
                separator = QFrame()
                separator.setFrameShape(QFrame.HLine)
                separator.setFrameShadow(QFrame.Sunken)
                separator.is_separator = True
                self.task_list_layout.insertWidget(
                    self.task_list_layout.count() - 2, separator
                )

    def handle_task_completed(self, task_id: str, completed: bool):
        self.task_manager.set_completed(task_id, completed)
        self.refresh_tasks()

    def handle_task_important(self, task_id: str, is_important: bool):
        new_category = "Important" if is_important else "None"
        self.task_manager.set_category(task_id, category=new_category)
        self.refresh_tasks()

    def handle_task_deleted(self, task_id: str):
        self.task_manager.delete_task(task_id)
        self.refresh_tasks()

    def handle_task_edited(self, task_id: str):
        self.open_edit_dialog(task_id)
