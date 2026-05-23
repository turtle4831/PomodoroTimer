"""Client configuration."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ClientConfig:
    default_work_minutes: int = 25
    default_short_break_minutes: int = 5
    default_long_break_minutes: int = 15


config = ClientConfig()
