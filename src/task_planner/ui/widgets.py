from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QMouseEvent, QIcon, QPixmap, QPainter, QColor


def get_themed_icon(icon_path, color_hex):
    if not icon_path:
        return QIcon()
    
    source_pixmap = QPixmap(icon_path)
    if source_pixmap.isNull():
        return QIcon()

    result_pixmap = QPixmap(source_pixmap.size())
    result_pixmap.fill(Qt.transparent)

    painter = QPainter(result_pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
    painter.drawPixmap(0, 0, source_pixmap)
    
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(result_pixmap.rect(), QColor(color_hex))
    painter.end()
    
    return QIcon(result_pixmap)


class AddTaskWidget(QWidget):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setMinimumHeight(60)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        self.title_label = QLabel("+ Add a task")
        font = QFont()
        self.title_label.setFont(font)

        layout.addWidget(self.title_label)
        layout.addStretch()

        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()


class MenuButton(QPushButton):
    def __init__(self, text, icon_path, parent=None):
        super().__init__(text, parent)
        self.icon_path = icon_path
        self.setFlat(True)
        self.setCursor(Qt.PointingHandCursor)
        
        if icon_path:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(16, 16))

    def update_icon_color(self, color_hex):
        if self.icon_path:
            self.setIcon(get_themed_icon(self.icon_path, color_hex))


class ThemeSelectionButton(MenuButton):
    def __init__(self, text, icon_path, parent=None):
        super().__init__(text, icon_path, parent)
        self.setCheckable(True)


class CheckMarkWidget(QPushButton):
    state_changed = pyqtSignal(bool)

    def __init__(self, checked_icon_path, unchecked_icon_path, checked=False, parent=None):
        super().__init__(parent)
        self.checked_icon_path = checked_icon_path
        self.unchecked_icon_path = unchecked_icon_path
        self.is_checked = checked
        self.current_icon_color = None
        
        self.setFlat(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(32, 32)
        self.setIconSize(QSize(24, 24))
        
        self.clicked.connect(self.toggle_state)
        self.update_icon()

    def toggle_state(self):
        self.is_checked = not self.is_checked
        self.update_icon(self.current_icon_color)
        self.state_changed.emit(self.is_checked)

    def setChecked(self, checked):
        if self.is_checked != checked:
            self.is_checked = checked
            self.update_icon(self.current_icon_color)

    def isChecked(self):
        return self.is_checked

    def update_icon(self, color_hex=None):
        self.current_icon_color = color_hex
        path = self.checked_icon_path if self.is_checked else self.unchecked_icon_path
        if color_hex:
            self.setIcon(get_themed_icon(path, color_hex))
        else:
            self.setIcon(QIcon(path))

    def update_icon_color(self, color_hex):
        self.update_icon(color_hex)
