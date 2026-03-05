from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QButtonGroup
from PyQt5.QtCore import Qt, pyqtSignal, QSettings
from task_planner.ui.widgets import MenuButton, ThemeSelectionButton, AnimatedToggle, LabeledToggle
from task_planner.config import THEME_ICONS, MENU_ICONS

class SettingsView(QWidget):
    theme_changed = pyqtSignal(str)
    calendar_settings_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        self.title_label = QLabel("Settings")
        self.title_label.setObjectName("settings_title_label")
        font = self.title_label.font()
        font.setPointSize(24)
        font.setBold(True)
        self.title_label.setFont(font)
        
        layout.addWidget(self.title_label)

        self.general_label = QLabel("General")
        self.general_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(self.general_label)

        self.compact_toggle = LabeledToggle("Compact Mode")
        layout.addWidget(self.compact_toggle)

        self.startup_label = QLabel("Startup Page")
        self.startup_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(self.startup_label)

        startup_layout = QHBoxLayout()
        startup_layout.setSpacing(10)
        self.startup_group = QButtonGroup(self)

        pages = ["My Day", "Important", "Tasks", "Completed", "Calendar"]
        self.startup_btns = {}

        for page in pages:
            btn = ThemeSelectionButton(page, MENU_ICONS.get(page))
            btn.setMinimumWidth(120)
            self.startup_group.addButton(btn)
            startup_layout.addWidget(btn)
            self.startup_btns[page] = btn
            btn.clicked.connect(lambda checked, p=page: self.save_startup_page(p))

        startup_layout.addStretch()
        layout.addLayout(startup_layout)

        settings = QSettings("TaskPlanner", "AppSettings")
        saved_page = settings.value("startup_page", "My Day")
        if saved_page in self.startup_btns:
            self.startup_btns[saved_page].setChecked(True)

        self.theme_label = QLabel("Theme")
        self.theme_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(self.theme_label)

        theme_layout = QHBoxLayout()
        theme_layout.setSpacing(20)
        self.theme_group = QButtonGroup(self)
        themes = ["Light", "Dark", "Device"]
        self.theme_btns = {}

        for theme in themes:
            btn = ThemeSelectionButton(theme, THEME_ICONS.get(theme))
            btn.setMinimumWidth(100)
            self.theme_group.addButton(btn)
            theme_layout.addWidget(btn)
            self.theme_btns[theme] = btn
            btn.clicked.connect(lambda checked, t=theme: self.theme_changed.emit(t.lower()))

        theme_layout.addStretch()
        layout.addLayout(theme_layout)

        theme_settings = QSettings("TaskPlanner", "ThemeSettings")
        theme_preference = theme_settings.value("theme", "device").capitalize()
        if theme_preference in self.theme_btns:
            self.theme_btns[theme_preference].setChecked(True)

        self.calendar_label = QLabel("Calendar")
        self.calendar_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(self.calendar_label)


        self.sunday_first_toggle = LabeledToggle("Start Week on Sunday (Default Monday)")
        cal_settings = QSettings("TaskPlanner", "CalendarSettings")
        is_sunday = cal_settings.value("sunday_first", False, type=bool)
        self.sunday_first_toggle.toggle.setChecked(is_sunday)
        
        self.sunday_first_toggle.toggle.stateChanged.connect(self.save_is_sunday_settings)
        layout.addWidget(self.sunday_first_toggle)


        self.show_completed_in_calendar = LabeledToggle("Show completed amount of tasks out of all tasks in the calendar view")
        is_show = cal_settings.value("show_completed_in_calendar", True, type=bool)
        self.show_completed_in_calendar.toggle.setChecked(is_show)

        self.show_completed_in_calendar.toggle.stateChanged.connect(self.save_show_completed_in_calendar)
        layout.addWidget(self.show_completed_in_calendar)


        self.indicator_style_toggle = LabeledToggle("Use Small Indicators")
        is_indicator = cal_settings.value("small_indicator", False, type=bool)
        self.indicator_style_toggle.toggle.setChecked(is_indicator)

        self.indicator_style_toggle.toggle.stateChanged.connect(self.save_small_indicator_style)
        layout.addWidget(self.indicator_style_toggle)


        layout.addStretch()

    def save_startup_page(self, page_name):
        settings = QSettings("TaskPlanner", "AppSettings")
        settings.setValue("startup_page", page_name)

    def save_is_sunday_settings(self):
        is_sunday = self.sunday_first_toggle.toggle.isChecked()
        settings = QSettings("TaskPlanner", "CalendarSettings")
        settings.setValue("sunday_first", is_sunday)
        self.calendar_settings_changed.emit()

    def save_show_completed_in_calendar(self):
        is_show = self.show_completed_in_calendar.toggle.isChecked()
        settings = QSettings("TaskPlanner", "CalendarSettings")
        settings.setValue("show_completed_in_calendar", is_show)
        self.calendar_settings_changed.emit()

    def save_small_indicator_style(self):
        is_small = self.indicator_style_toggle.toggle.isChecked()
        settings = QSettings("TaskPlanner", "CalendarSettings")
        settings.setValue("small_indicator", is_small)
        self.calendar_settings_changed.emit()

