from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCalendarWidget
from PyQt5.QtCore import pyqtSignal


class CalendarView(QWidget):

    date_selected = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.calendar = QCalendarWidget()
        layout.addWidget(self.calendar)

        self.calendar.clicked.connect(
            lambda qdate: self.date_selected.emit(qdate.toPyDate())
        )
