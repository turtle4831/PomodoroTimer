"""Local Pomodoro timer state machine."""

from dataclasses import dataclass, field
from enum import Enum


class TimerPhase(str, Enum):
    WORK = "work"
    SHORT_BREAK = "short_break"
    LONG_BREAK = "long_break"


@dataclass
class TimerService:
    work_seconds: int = 25 * 60
    break_seconds: int = 5 * 60
    phase: TimerPhase = TimerPhase.WORK
    remaining_seconds: int = field(init=False)
    is_running: bool = False

    def __post_init__(self) -> None:
        self.remaining_seconds = self.work_seconds

    def start(self) -> None:
        self.is_running = True

    def pause(self) -> None:
        self.is_running = False

    def reset(self) -> None:
        self.is_running = False
        self.phase = TimerPhase.WORK
        self.remaining_seconds = self.work_seconds

    def set_durations(self, work_seconds: int, break_seconds: int) -> None:
        self.work_seconds = work_seconds
        self.break_seconds = break_seconds
        if not self.is_running:
            self.remaining_seconds = self._current_phase_seconds()

    def tick(self) -> bool:
        """Advance one second. Returns False when timer has finished."""
        if not self.is_running or self.remaining_seconds <= 0:
            return self.is_running

        self.remaining_seconds -= 1
        if self.remaining_seconds == 0:
            self.is_running = False
            self._advance_phase()
        return True

    def _advance_phase(self) -> None:
        if self.phase == TimerPhase.WORK:
            self.phase = TimerPhase.SHORT_BREAK
        else:
            self.phase = TimerPhase.WORK
        self.remaining_seconds = self._current_phase_seconds()

    def _current_phase_seconds(self) -> int:
        if self.phase == TimerPhase.WORK:
            return self.work_seconds
        return self.break_seconds
