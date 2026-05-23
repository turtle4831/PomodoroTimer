"""Application bootstrap and window wiring."""

from PyQt6.QtWidgets import QApplication

from client.ui.main_window import MainWindow


def create_app() -> QApplication:
    application = QApplication([])
    application.setApplicationName("Pomodoro Study Timer")
    application.setOrganizationName("PomodoroTimer")
    return application


def run_app() -> int:
    app = create_app()
    window = MainWindow()
    window.show()
    return app.exec()
