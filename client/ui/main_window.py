"""Main application window."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QWidget

from client.ui.timer_widget import TimerWidget


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Pomodoro Study Timer")
        self.resize(640, 480)
        self.setMinimumSize(520, 420)

        self._timer_widget = TimerWidget()

        #subtitle = QLabel("Local Pomodoro timer for focused study sessions.")
        #subtitle.setObjectName("subtitle")
        #subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #subtitle.setWordWrap(True)

        container = QWidget()
        container.setObjectName("appContainer")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(28)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #layout.addWidget(subtitle)
        layout.addWidget(self._timer_widget)
        self.setCentralWidget(container)

        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #071b22;
            }

            QWidget#appContainer {
                background: qlineargradient(
                    x1: 0, y1: 0,
                    x2: 1, y2: 1,
                    stop: 0 #06241d,
                    stop: 0.55 #0a2834,
                    stop: 1 #102f4a
                );
            }

            QLabel#subtitle {
                color: #b8efe1;
                font-size: 18px;
                font-weight: 500;
            }
            """
        )
