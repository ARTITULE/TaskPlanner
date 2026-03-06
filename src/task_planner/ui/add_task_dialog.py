from PyQt5.QtWidgets import (
    QDialog,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QCalendarWidget,
)
from PyQt5.QtCore import Qt, pyqtSignal, QDate, QSettings
from task_planner.models.task import Task
from task_planner.config import Categories, CALENDAR_ICONS
from task_planner.ui.widgets import MenuButton
from task_planner.ui.calendar_view import CustomCalendar


class AddTaskDialog(QDialog):

    task_submitted = pyqtSignal(str, str, str, str, object)

    def __init__(self, task: Task | None = None, parent=None):

        super().__init__(parent=parent)
        self.setWindowTitle("Add Task")
        self.setMinimumWidth(450)

        self.task = task

        self.init_ui()


    def init_ui(self):
        task_manager = None
        if self.parent() and hasattr(self.parent(), 'task_manager'):
            task_manager = self.parent().task_manager

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.dialog_label = QLabel("Add New Task")
        self.dialog_label.setObjectName("dialog_label")

        self.task_title = QLineEdit(placeholderText="Task name")
        self.task_title.setObjectName("task_title")

        self.task_description = QLineEdit(placeholderText="Task description")
        self.task_description.setObjectName("task_description")

        self.due_date_label = QLabel("Due date")
        
        self.add_date_btn = QPushButton("+ Add Due Date")
        self.add_date_btn.setObjectName("add_date_btn")
        self.add_date_btn.setCursor(Qt.PointingHandCursor)

        self.due_date_edit = QDateEdit()
        self.due_date_edit.setCalendarPopup(True)
        self.due_date_edit.setDisplayFormat("dd-MM-yyyy")
        self.due_date_edit.setKeyboardTracking(False)
        self.due_date_edit.setDate(QDate.currentDate())
        self.due_date_edit.setMinimumDate(QDate(2000, 1, 1))

        self.calendar = CustomCalendar(task_manager=task_manager)
        self.calendar.add_task_calendar = True
        self.calendar.setFixedSize(400, 400)
        self.calendar.setGridVisible(True)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.setNavigationBarVisible(False)
        self.due_date_edit.setCalendarWidget(self.calendar)

        self.calendar_header = QWidget()
        header_layout = QHBoxLayout(self.calendar_header)
        header_layout.setContentsMargins(5, 5, 5, 5)
        
        self.prev_btn = MenuButton("", CALENDAR_ICONS.get("Previous"))
        self.prev_btn.setFixedWidth(30)
        if not CALENDAR_ICONS.get("Previous"): self.prev_btn.setText("<")
        
        self.next_btn = MenuButton("", CALENDAR_ICONS.get("Next"))
        self.next_btn.setFixedWidth(30)
        if not CALENDAR_ICONS.get("Next"): self.next_btn.setText(">")
        
        self.month_label = QLabel()
        self.month_label.setAlignment(Qt.AlignCenter)
        font = self.month_label.font()
        font.setPointSize(14)
        font.setBold(True)
        self.month_label.setFont(font)
        
        header_layout.addWidget(self.prev_btn)
        header_layout.addStretch()
        header_layout.addWidget(self.month_label)
        header_layout.addStretch()
        header_layout.addWidget(self.next_btn)

        if self.calendar.layout():
            self.calendar.layout().setContentsMargins(0, 0, 0, 0)
            self.calendar.layout().insertWidget(0, self.calendar_header)
        
        self.prev_btn.clicked.connect(self.calendar.showPreviousMonth)
        self.next_btn.clicked.connect(self.calendar.showNextMonth)
        self.calendar.currentPageChanged.connect(self.update_header_label)
        self.update_header_label(self.calendar.yearShown(), self.calendar.monthShown())
        
        self.clear_date_btn = QPushButton("✕")
        self.clear_date_btn.setObjectName("clear_date_btn")
        self.clear_date_btn.setFixedSize(35, 35)
        self.clear_date_btn.setCursor(Qt.PointingHandCursor)

        self.date_edit_container = QWidget()
        self.date_edit_layout = QHBoxLayout(self.date_edit_container)
        self.date_edit_layout.setContentsMargins(0, 0, 0, 0)
        self.date_edit_layout.setSpacing(10)
        self.date_edit_layout.addWidget(self.due_date_edit)
        self.date_edit_layout.addWidget(self.clear_date_btn)
        self.date_edit_container.hide()

        self.category_label = QLabel("Category")
        self.category_box = QComboBox()
        self.category_box.addItems(Categories)

        self.save_btn = QPushButton("Save Task")
        self.save_btn.setObjectName("save_btn")
        self.save_btn.setCursor(Qt.PointingHandCursor)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setObjectName("cancel_btn")
        self.cancel_btn.setCursor(Qt.PointingHandCursor)
            
        layout.addWidget(self.dialog_label)
        layout.addWidget(self.task_title)
        layout.addWidget(self.task_description)
        layout.addWidget(self.due_date_label)
        layout.addWidget(self.add_date_btn)
        layout.addWidget(self.date_edit_container)
        layout.addWidget(self.category_label)
        layout.addWidget(self.category_box)

        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(button_layout)

        if self.task:
            self.dialog_label.setText("Edit Task")
            self.task_title.setText(self.task.title)
            if self.task.description:
                self.task_description.setText(self.task.description)
            if self.task.exp_time:
                self.show_date_picker()
                date_val = QDate(
                    self.task.exp_time.year,
                    self.task.exp_time.month,
                    self.task.exp_time.day
                )
                self.due_date_edit.setDate(date_val)
            if self.task.category:
                index = self.category_box.findText(self.task.category)
                if index != -1:
                    self.category_box.setCurrentIndex(index)


        self.setLayout(layout)

        self.save_btn.clicked.connect(self.emit_task)
        self.cancel_btn.clicked.connect(self.reject)
        self.add_date_btn.clicked.connect(self.show_date_picker)
        self.clear_date_btn.clicked.connect(self.hide_date_picker)

    def update_header_label(self, year, month):
        display_date = QDate(year, month, 1)
        self.month_label.setText(display_date.toString("MMMM yyyy"))

    def show_date_picker(self):
        self.add_date_btn.hide()
        self.date_edit_container.show()

    def hide_date_picker(self):
        self.date_edit_container.hide()
        self.add_date_btn.show()

    def emit_task(self):
        task_title = self.task_title.text().strip()
        task_description = self.task_description.text().strip() or ""
        task_category = self.category_box.currentText()
        task_category = None if task_category == "None" else task_category

        if self.date_edit_container.isVisible():
            date_val = self.due_date_edit.date()
            exp_time = date_val.toPyDate()
        else:
            exp_time = None

        
        task_id = self.task.id if self.task else ""

        if task_title:

            self.task_submitted.emit(task_title, task_description, task_id, task_category, exp_time)

            self.task_title.clear()
            self.task_description.clear()
            self.accept()
