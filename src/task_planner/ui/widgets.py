from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy, QPushButton, QCheckBox
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QPropertyAnimation, QEasingCurve, pyqtProperty, QRect, QPoint
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
        self.setStyleSheet("QPushButton { text-align: center; padding: 10px; }")


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


class AnimatedToggle(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 28)
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.NoFocus)
        self.setStyleSheet("QCheckBox::indicator { width: 0px; height: 0px; }")
        self._handle_position = 3
        self.animation = QPropertyAnimation(self, b"handle_position", self)
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.stateChanged.connect(self.setup_animation)

    def mouseReleaseEvent(self, e):
        self.setChecked(not self.isChecked())

    @pyqtProperty(int)
    def handle_position(self):
        return self._handle_position

    @handle_position.setter
    def handle_position(self, pos):
        self._handle_position = pos
        self.update()

    def setup_animation(self, state):
        self.animation.stop()
        if state:
            self.animation.setEndValue(self.width() - 25)
        else:
            self.animation.setEndValue(3)
        self.animation.start()

    def paintEvent(self, e):
        contRect = self.rect()
        handleRect = QRect(self._handle_position, 3, 22, 22)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        if not self.isChecked():
            painter.setBrush(QColor("#CCCCCC"))
            painter.drawRoundedRect(0, 0, contRect.width(), contRect.height(), 14, 14)
            painter.setBrush(QColor("#FFFFFF"))
            painter.drawEllipse(handleRect)
        else:
            painter.setBrush(QColor("#4A90E2"))
            painter.drawRoundedRect(0, 0, contRect.width(), contRect.height(), 14, 14)
            painter.setBrush(QColor("#FFFFFF"))
            painter.drawEllipse(handleRect)
        painter.end()


class LabeledToggle(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(30)
        
        self.toggle = AnimatedToggle()
        self.label = QLabel(text)
        
        layout.addWidget(self.toggle)
        layout.addWidget(self.label)
        layout.addStretch()
