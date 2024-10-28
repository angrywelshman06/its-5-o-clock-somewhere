from PyQt5.QtCore import QTimer, Qt, QEvent
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
import datetime
import pytz
import pycountry
import sys

class DesktopWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("5 O'Clock Widget")
        self.setWindowFlags(
            Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint | Qt.X11BypassWindowManagerHint
        )
        self.setGeometry(100, 100, 500, 500)  # Set square dimensions (300x300)

        self.countries = self.get_countries_with_5_oclock()
        self.current_index = 0

        self.background_image_path = r"C:\Users\rhysd\PycharmProjects\its-5-o-clock-somewhere\DALL·E 2023-06-19 21.05.07 - a picture of a cocktail on a beach.png"

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.static_label = QLabel("It's 5 o'clock in", self)
        self.static_label.setAlignment(Qt.AlignCenter)
        self.static_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        self.layout.addWidget(self.static_label)

        self.dynamic_label = QLabel(self)
        self.dynamic_label.setAlignment(Qt.AlignCenter)
        self.dynamic_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        self.layout.addWidget(self.dynamic_label)

        self.update_widget()

        # Timer to check the time every second
        self.time_check_timer = QTimer(self)
        self.time_check_timer.timeout.connect(self.check_time)
        self.time_check_timer.start(1000)  # 1 second in milliseconds

    def get_countries_with_5_oclock(self):
        countries = list(pytz.country_timezones.keys())
        countries_with_5_oclock = []
        for country_code in countries:
            timezones = pytz.country_timezones.get(country_code, [])
            for timezone in timezones:
                now = datetime.datetime.now(pytz.timezone(timezone))
                if now.hour == 17:
                    country = pycountry.countries.get(alpha_2=country_code)
                    if country:
                        countries_with_5_oclock.append(country)
                    break
        return countries_with_5_oclock

    def update_widget(self):
        country = self.countries[self.current_index]
        country_name = country.name
        self.dynamic_label.setText(country_name)

        self.current_index = (self.current_index + 1) % len(self.countries)

        # Update every 2 seconds (2000 milliseconds)
        QTimer.singleShot(2000, self.update_widget)

    def check_time(self):
        now = datetime.datetime.now()
        if now.minute == 0 and now.second == 0:
            self.update_countries()

    def update_countries(self):
        self.countries = self.get_countries_with_5_oclock()
        self.current_index = 0  # Reset index to start from the first country
        country = self.countries[self.current_index]
        country_name = country.name
        self.dynamic_label.setText(country_name)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos()
            event.accept()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

    def changeEvent(self, event):
        if event.type() == QEvent.ActivationChange:
            if self.isActiveWindow():
                self.activateWindow()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the background image
        pixmap = QPixmap(self.background_image_path)
        pixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        painter.drawPixmap(self.rect(), pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set Windows-like style
    app.setStyle("Fusion")

    widget = DesktopWidget()
    widget.show()

    sys.exit(app.exec_())