"""Local Pomodoro timer display (placeholder)."""

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QStyle,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

from client.config import config
from client.services.timer_service import TimerPhase, TimerService


class TimerWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("timerCard")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._service = TimerService(
            work_seconds=config.default_work_minutes * 60,
            break_seconds=config.default_short_break_minutes * 60,
        )

        self._display = QLabel(self._format_time(self._service.remaining_seconds))
        self._display.setObjectName("timerDisplay")
        self._display.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._phase_label = QLabel("Work")
        self._phase_label.setObjectName("phaseLabel")
        self._phase_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._notification_label = QLabel("Notifications will appear when a timer ends.")
        self._notification_label.setObjectName("notificationLabel")
        self._notification_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._notification_label.setWordWrap(True)

        self._start_button = QPushButton("Start")
        self._pause_button = QPushButton("Pause")
        self._reset_button = QPushButton("Reset")

        self._work_minutes_input = QSpinBox()
        self._work_minutes_input.setRange(1, 180)
        self._work_minutes_input.setValue(config.default_work_minutes)
        self._work_minutes_input.setSuffix(" min")

        self._break_minutes_input = QSpinBox()
        self._break_minutes_input.setRange(1, 60)
        self._break_minutes_input.setValue(config.default_short_break_minutes)
        self._break_minutes_input.setSuffix(" min")

        self._start_button.clicked.connect(self._on_start)
        self._pause_button.clicked.connect(self._on_pause)
        self._reset_button.clicked.connect(self._on_reset)
        self._work_minutes_input.valueChanged.connect(self._on_duration_changed)
        self._break_minutes_input.valueChanged.connect(self._on_duration_changed)

        self._tick = QTimer(self)
        self._tick.setInterval(1000)
        self._tick.timeout.connect(self._on_tick)
        self._tray_icon = self._create_tray_icon()

        settings = QHBoxLayout()
        settings.setSpacing(16)
        settings.setAlignment(Qt.AlignmentFlag.AlignCenter)
        settings.addWidget(self._setting_group("Work", self._work_minutes_input))
        settings.addWidget(self._setting_group("Break", self._break_minutes_input))

        controls = QHBoxLayout()
        controls.setSpacing(14)
        controls.setAlignment(Qt.AlignmentFlag.AlignCenter)
        controls.addWidget(self._start_button)
        controls.addWidget(self._pause_button)
        controls.addWidget(self._reset_button)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 36, 36, 36)
        layout.setSpacing(22)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._display)
        layout.addWidget(self._phase_label)
        layout.addWidget(self._notification_label)
        layout.addLayout(settings)
        layout.addLayout(controls)

        self.setStyleSheet(
            """
            QWidget#timerCard {
                background-color: rgba(7, 40, 48, 210);
                border: 1px solid #1f6f70;
                border-radius: 24px;
            }

            QLabel#timerDisplay {
                color: #dffcf5;
                font-size: 88px;
                font-weight: 800;
                letter-spacing: 2px;
            }

            QLabel#phaseLabel {
                color: #70d6c4;
                font-size: 20px;
                font-weight: 700;
                text-transform: uppercase;
            }

            QLabel#notificationLabel {
                color: #b8efe1;
                font-size: 14px;
                font-weight: 500;
            }

            QLabel#settingLabel {
                color: #9cdccb;
                font-size: 14px;
                font-weight: 700;
            }

            QWidget#settingGroup {
                background-color: rgba(10, 77, 95, 120);
                border: 1px solid #1f6f70;
                border-radius: 14px;
                padding: 8px;
            }

            QSpinBox {
                background-color: #082935;
                border: 1px solid #41b9a9;
                border-radius: 10px;
                color: #e8fffb;
                font-size: 15px;
                font-weight: 700;
                min-width: 92px;
                padding: 8px 10px;
            }

            QSpinBox::up-button,
            QSpinBox::down-button {
                width: 18px;
                border: none;
                background-color: #0f6d65;
            }

            QPushButton {
                background-color: #0f6d65;
                border: 1px solid #41b9a9;
                border-radius: 12px;
                color: #e8fffb;
                font-size: 16px;
                font-weight: 700;
                min-width: 96px;
                padding: 12px 18px;
            }

            QPushButton:hover {
                background-color: #12867b;
                border-color: #67ddce;
            }

            QPushButton:pressed {
                background-color: #0a4d5f;
            }
            """
        )

    def _create_tray_icon(self) -> QSystemTrayIcon | None:
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return None

        tray_icon = QSystemTrayIcon(self)
        tray_icon.setToolTip("Pomodoro Study Timer")
        tray_icon.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation)
        )
        tray_icon.show()
        return tray_icon

    def _setting_group(self, label: str, input_widget: QSpinBox) -> QWidget:
        label_widget = QLabel(label)
        label_widget.setObjectName("settingLabel")
        label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        group = QWidget()
        group.setObjectName("settingGroup")
        layout = QVBoxLayout(group)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(6)
        layout.addWidget(label_widget)
        layout.addWidget(input_widget)
        return group

    def _on_start(self) -> None:
        self._service.start()
        self._set_duration_inputs_enabled(False)
        if not self._tick.isActive():
            self._tick.start()

    def _on_pause(self) -> None:
        self._service.pause()
        self._set_duration_inputs_enabled(True)
        self._tick.stop()

    def _on_reset(self) -> None:
        self._service.reset()
        self._tick.stop()
        self._set_duration_inputs_enabled(True)
        self._refresh_display()

    def _on_tick(self) -> None:
        finished_phase = self._service.phase
        if self._service.tick():
            self._refresh_display()
        else:
            self._tick.stop()
            self._set_duration_inputs_enabled(True)
            self._refresh_display()
            self._notify_timer_finished(finished_phase)

    def _on_duration_changed(self) -> None:
        self._service.set_durations(
            work_seconds=self._work_minutes_input.value() * 60,
            break_seconds=self._break_minutes_input.value() * 60,
        )
        self._refresh_display()

    def _refresh_display(self) -> None:
        self._display.setText(self._format_time(self._service.remaining_seconds))
        self._phase_label.setText(self._format_phase(self._service.phase))

    def _set_duration_inputs_enabled(self, enabled: bool) -> None:
        self._work_minutes_input.setEnabled(enabled)
        self._break_minutes_input.setEnabled(enabled)

    def _notify_timer_finished(self, finished_phase: TimerPhase) -> None:
        if finished_phase == TimerPhase.WORK:
            title = "Work session complete"
            message = "Break Time!!!!"
        else:
            title = "Break complete"
            message = "Break is over. Ready for another work session? :3"

        self._notification_label.setText(message)
        QApplication.beep()

        if self._tray_icon is not None and QSystemTrayIcon.supportsMessages():
            self._tray_icon.showMessage(
                title,
                message,
                QSystemTrayIcon.MessageIcon.Information,
                5000,
            )

    def _format_time(self, total_seconds: int) -> str:
        minutes, seconds = divmod(total_seconds, 60)
        return f"{minutes:02d}:{seconds:02d}"

    def _format_phase(self, phase: TimerPhase) -> str:
        return phase.value.replace("_", " ").title()
