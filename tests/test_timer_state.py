"""Tests for local timer service."""

from client.services.timer_service import TimerPhase, TimerService


def test_timer_reset_restores_work_duration():
    service = TimerService(work_seconds=60)
    service.remaining_seconds = 10
    service.phase = TimerPhase.SHORT_BREAK

    service.reset()

    assert service.phase == TimerPhase.WORK
    assert service.remaining_seconds == 60
    assert service.is_running is False


def test_timer_tick_counts_down():
    service = TimerService(work_seconds=3)
    service.start()

    assert service.tick() is True
    assert service.remaining_seconds == 2

    service.remaining_seconds = 1
    service.tick()

    assert service.phase == TimerPhase.SHORT_BREAK
    assert service.is_running is False


def test_timer_moves_to_break_when_work_finishes():
    service = TimerService(work_seconds=1, break_seconds=5)
    service.start()

    still_running = service.tick()

    assert still_running is False
    assert service.phase == TimerPhase.SHORT_BREAK
    assert service.remaining_seconds == 5
    assert service.is_running is False


def test_set_durations_updates_idle_timer():
    service = TimerService(work_seconds=60, break_seconds=30)

    service.set_durations(work_seconds=25 * 60, break_seconds=5 * 60)

    assert service.work_seconds == 25 * 60
    assert service.break_seconds == 5 * 60
    assert service.remaining_seconds == 25 * 60
