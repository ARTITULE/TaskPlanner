from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QButtonGroup
from PyQt5.QtCore import Qt, pyqtSignal, QSettings
from task_planner.ui.widgets import MenuButton, ThemeSelectionButton
from task_planner.config import THEME_ICONS

class SettingsView(QWidget):
    theme_changed = pyqtSignal(str)

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

        self.theme_label = QLabel("Theme")
        self.theme_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(self.theme_label)

        theme_layout = QHBoxLayout()
        theme_layout.setSpacing(20)
        
        self.theme_group = QButtonGroup(self)
        
        self.light_btn = ThemeSelectionButton("Light", THEME_ICONS.get("Light"))
        self.dark_btn = ThemeSelectionButton("Dark", THEME_ICONS.get("Dark"))
        self.device_btn = ThemeSelectionButton("Device", THEME_ICONS.get("Device"))
        
        self.light_btn.setMinimumWidth(100)
        self.dark_btn.setMinimumWidth(100)
        self.device_btn.setMinimumWidth(100)
        
        self.theme_group.addButton(self.light_btn)
        self.theme_group.addButton(self.dark_btn)
        self.theme_group.addButton(self.device_btn)
        
        settings = QSettings("TaskPlanner", "ThemeSettings")
        theme_preference = settings.value("theme", "device")
        
        if theme_preference == "light":
            self.light_btn.setChecked(True)
        elif theme_preference == "dark":
            self.dark_btn.setChecked(True)
        else:
            self.device_btn.setChecked(True)

        theme_layout.addWidget(self.light_btn)
        theme_layout.addWidget(self.dark_btn)
        theme_layout.addWidget(self.device_btn)
        theme_layout.addStretch()
        
        layout.addLayout(theme_layout)

        self.light_btn.clicked.connect(lambda: self.theme_changed.emit("light"))
        self.dark_btn.clicked.connect(lambda: self.theme_changed.emit("dark"))
        self.device_btn.clicked.connect(lambda: self.theme_changed.emit("device"))
        
        layout.addStretch()
