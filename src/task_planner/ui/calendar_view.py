from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCalendarWidget
from PyQt5.QtCore import pyqtSignal, Qt, QDate, QEvent, QRect, QSettings
from PyQt5.QtGui import QColor, QFont, QPainter, QBrush, QPen
from task_planner.ui.widgets import MenuButton
from task_planner.config import CALENDAR_ICONS


class CustomCalendar(QCalendarWidget):
    def __init__(self, task_manager, parent=None):
        super().__init__(parent)
        self.task_manager = task_manager
        self.show_completed = True
        self.show_small = False
        self.add_task_calendar = False

        font = self.font()
        font.setPointSize(18)
        font.setBold(True)
        self.setFont(font)

        for child in self.findChildren(QWidget):
            child.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() in [QEvent.Wheel, QEvent.KeyPress, QEvent.KeyRelease]:
            return True
        return super().eventFilter(obj, event)

    def paintCell(self, painter, rect, date):
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)
        
        if date == self.selectedDate():
            painter.fillRect(rect, self.palette().highlight())
            painter.setPen(self.palette().highlightedText().color())
        else:
            if date.month() == self.monthShown():
                painter.setPen(self.palette().text().color())
            else:
                painter.setPen(Qt.gray)
        
        date_font = QFont("sans-serif", 14)
        painter.setFont(date_font)
        painter.drawText(rect.adjusted(0, 5, -8, 0), Qt.AlignRight | Qt.AlignTop, str(date.day()))

        if self.task_manager is None:
            painter.restore()
            return

        tasks = self.task_manager.tasks
        py_date = date.toPyDate()
        
        imp_pending = 0
        reg_pending = 0
        completed = 0
        total_pending = 0
        
        for task in tasks:
            if task.exp_time == py_date:
                total_pending += 1
                if task.completed:
                    completed += 1
                elif task.category == "Important":
                    imp_pending += 1
                else:
                    reg_pending += 1

        is_compact = self.show_small or self.add_task_calendar
        indicator_size = 12 if is_compact else 14
        indicator_font = QFont("sans-serif", 9 if is_compact else 11)
        painter.setFont(indicator_font)
        
        v_spacing = 2
        left_x = rect.left() + 5
        
        def draw_badge(count, bg_color, text_color, x, y, label_suffix="", total_count=None):
            if total_count is not None and not is_compact:
                unit = "task" if total_count == 1 else "tasks"
                text = f"{count} / {total_count} {unit}{label_suffix}"
            elif total_count is not None and is_compact:
                text = f"{count} / {total_count}"
            elif not is_compact:
                text = f"{count} task{label_suffix}" if count == 1 else f"{count} tasks{label_suffix}"
            else:
                text = f"{count}"
            
            text_rect = painter.fontMetrics().boundingRect(text)
            badge_width = text_rect.width() + 8
            bg_rect = QRect(x, y, badge_width, indicator_size)
            
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(bg_color))
            painter.drawRoundedRect(bg_rect, 4, 4)
            
            painter.setPen(QPen(text_color))
            painter.drawText(bg_rect, Qt.AlignCenter, text)
            return badge_width + 4

        if self.add_task_calendar:
            current_y = rect.bottom() - (indicator_size + v_spacing)
            if self.show_completed and completed > 0:
                draw_badge(completed, QColor("#28A745"), Qt.white, left_x, current_y, total_count=total_pending)
                current_y -= (indicator_size + v_spacing)
            if reg_pending > 0:
                draw_badge(reg_pending, QColor("#5A5A5A"), Qt.white, left_x, current_y)
                current_y -= (indicator_size + v_spacing)
            if imp_pending > 0:
                draw_badge(imp_pending, QColor("#FF8C00"), Qt.white, left_x, current_y)
        elif self.show_small:
            current_x = left_x
            current_y = rect.bottom() - 18
            if self.show_completed and completed > 0:
                current_x += draw_badge(completed, QColor("#28A745"), Qt.white, current_x, current_y, total_count=total_pending)
            if reg_pending > 0:
                current_x += draw_badge(reg_pending, QColor("#5A5A5A"), Qt.white, current_x, current_y)
            if imp_pending > 0:
                current_x += draw_badge(imp_pending, QColor("#FF8C00"), Qt.white, current_x, current_y)
        else:
            current_y = rect.bottom() - 18
            if self.show_completed and completed > 0:
                draw_badge(completed, QColor("#28A745"), Qt.white, left_x, current_y, " done", total_count=total_pending)
                current_y -= (14 + v_spacing)
            if reg_pending > 0:
                draw_badge(reg_pending, QColor("#5A5A5A"), Qt.white, left_x, current_y)
                current_y -= (14 + v_spacing)
            if imp_pending > 0:
                draw_badge(imp_pending, QColor("#FF8C00"), Qt.white, left_x, current_y)
        
        painter.restore()


class CalendarView(QWidget):

    date_selected = pyqtSignal(object)

    def __init__(self, task_manager):
        super().__init__()
        self.task_manager = task_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        header_layout = QHBoxLayout()
        
        self.prev_btn = MenuButton("", CALENDAR_ICONS.get("Previous"))
        self.prev_btn.setFixedWidth(40)
        if not CALENDAR_ICONS.get("Previous"):
            self.prev_btn.setText("<")
        
        self.next_btn = MenuButton("", CALENDAR_ICONS.get("Next"))
        self.next_btn.setFixedWidth(40)
        if not CALENDAR_ICONS.get("Next"):
            self.next_btn.setText(">")

        self.month_label = QLabel()
        self.month_label.setAlignment(Qt.AlignCenter)
        self.month_label.setObjectName("calendar_header_label")
        font = self.month_label.font()
        font.setPointSize(24)
        font.setBold(True)
        self.month_label.setFont(font)

        header_layout.addWidget(self.prev_btn)
        header_layout.addStretch()
        header_layout.addWidget(self.month_label)
        header_layout.addStretch()
        header_layout.addWidget(self.next_btn)

        self.calendar = CustomCalendar(task_manager=self.task_manager)
        self.calendar.setGridVisible(True)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.setNavigationBarVisible(False)
        self.apply_settings()

        layout.addLayout(header_layout)
        layout.addWidget(self.calendar)

        self.prev_btn.clicked.connect(self.calendar.showPreviousMonth)
        self.next_btn.clicked.connect(self.calendar.showNextMonth)
        self.calendar.currentPageChanged.connect(self.update_header_label)
        
        self.calendar.clicked.connect(
            lambda qdate: self.date_selected.emit(qdate.toPyDate())
        )

        self.update_header_label(self.calendar.yearShown(), self.calendar.monthShown())

    def update_header_label(self, year, month):
        display_date = QDate(year, month, 1)
        self.month_label.setText(display_date.toString("MMMM yyyy"))

    def apply_settings(self):
        settings = QSettings("TaskPlanner", "CalendarSettings")
        is_sunday = settings.value("sunday_first", False, type=bool)
        is_show = settings.value("show_completed_in_calendar", True, type=bool)
        is_small = settings.value("small_indicator", False, type=bool)
        
        if is_sunday:
            self.calendar.setFirstDayOfWeek(Qt.Sunday)
        else:
            self.calendar.setFirstDayOfWeek(Qt.Monday)

        self.calendar.show_completed = is_show
        self.calendar.show_small = is_small
        self.calendar.update()
