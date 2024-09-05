import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont, QPainter, QColor, QPen, QFontDatabase
from PyQt5.QtCore import Qt, QPoint, QRect
from math import cos, sin, pi
from malicious_ip_detector import MaliciousIPDetector

class CircularButton(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.text = text
        self.hovered = False
        self.setFixedSize(100, 100)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw circle
        painter.setPen(QPen(QColor("#333333"), 2))
        painter.setBrush(QColor("#4CAF50") if self.hovered else QColor("#45a049"))
        painter.drawEllipse(2, 2, 96, 96)

        # Draw text
        painter.setPen(QColor("white"))
        painter.setFont(QFont('Lato', 10, QFont.Bold))
        painter.drawText(QRect(0, 0, 100, 100), Qt.AlignCenter, self.text)

    def enterEvent(self, event):
        self.hovered = True
        self.update()

    def leaveEvent(self, event):
        self.hovered = False
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked()

    def clicked(self):
        # This method will be overridden for each button
        pass

class IDSMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.loadFonts()
        self.initUI()

    def loadFonts(self):
        QFontDatabase.addApplicationFont('Lato-Bold.ttf')

    def initUI(self):
        self.setWindowTitle('Intrusion Detection System')
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()

        # Title
        title_label = QLabel('Intrusion Detection System')
        title_label.setFont(QFont('Lato', 30, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Circular layout widget
        self.circular_widget = CircularLayoutWidget(self)
        layout.addWidget(self.circular_widget)

        main_widget.setLayout(layout)

        # Apply stylesheet
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: #f0f0f0;
                border-image: url('/images/bg.png') 0 0 0 0 stretch stretch;
            }}
            QLabel {{
                color: #333;
                margin: 20px 0;
            }}
        """)

class CircularLayoutWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.buttons = []
        self.initButtons()

    def initButtons(self):
        features = [
            ("Malicious IP\nDetection", self.openMaliciousIPDetector),
            ("Feature 2", lambda: print("Feature 2 clicked")),
            ("Feature 3", lambda: print("Feature 3 clicked")),
            ("Feature 4", lambda: print("Feature 4 clicked")),
            ("Feature 5", lambda: print("Feature 5 clicked"))
        ]

        for text, callback in features:
            button = CircularButton(text, self)
            button.clicked = callback
            self.buttons.append(button)

    def resizeEvent(self, event):
        center = self.rect().center()
        radius = min(self.width(), self.height()) // 3
        angle_step = 2 * pi / len(self.buttons)

        for i, button in enumerate(self.buttons):
            angle = i * angle_step
            x = center.x() + radius * cos(angle) - button.width() // 2
            y = center.y() + radius * sin(angle) - button.height() // 2
            button.move(int(x), int(y))

    def openMaliciousIPDetector(self):
        self.malicious_ip_detector = MaliciousIPDetector()
        self.malicious_ip_detector.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = IDSMainWindow()
    ex.show()
    sys.exit(app.exec_())