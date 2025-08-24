"""ADB action helpers for topscreen

Provides a small ADBController that shells out to adb to perform input events.
This keeps GUI and platform-specific logic separate.
"""
from __future__ import annotations

import shlex
import shutil
import subprocess
from dataclasses import dataclass
from typing import Tuple, Optional


@dataclass
class ADBConfig:
    tap_coords: Tuple[int, int] = (100, 100)
    swipe_start: Tuple[int, int] = (100, 300)
    swipe_end: Tuple[int, int] = (300, 300)
    swipe_duration_ms: int = 200
    adb_path: Optional[str] = None


class ADBController:
    """Controller that runs adb commands via subprocess.

    The controller is intentionally minimal. It shells out to adb so the host
    machine must have adb installed and the device connected. This keeps the
    code portable across platforms.
    """

    def __init__(self, config: Optional[ADBConfig] = None) -> None:
        self.config = config or ADBConfig()
        if not self.config.adb_path:
            self.config.adb_path = shutil.which("adb") or "adb"

    def _run(self, cmd: str) -> subprocess.CompletedProcess:
        full = f"{self.config.adb_path} {cmd}"
        # Use shlex for readable logs but call list form to be cross-platform
        parts = shlex.split(full)
        return subprocess.run(parts, capture_output=True, text=True)

    def tap(self, x: Optional[int] = None, y: Optional[int] = None) -> bool:
        x = x if x is not None else self.config.tap_coords[0]
        y = y if y is not None else self.config.tap_coords[1]
        res = self._run(f"shell input tap {x} {y}")
        return res.returncode == 0

    def swipe(
        self,
        x1: Optional[int] = None,
        y1: Optional[int] = None,
        x2: Optional[int] = None,
        y2: Optional[int] = None,
        duration_ms: Optional[int] = None,
    ) -> bool:
        x1 = x1 if x1 is not None else self.config.swipe_start[0]
        y1 = y1 if y1 is not None else self.config.swipe_start[1]
        x2 = x2 if x2 is not None else self.config.swipe_end[0]
        y2 = y2 if y2 is not None else self.config.swipe_end[1]
        duration_ms = duration_ms if duration_ms is not None else self.config.swipe_duration_ms
        res = self._run(f"shell input swipe {x1} {y1} {x2} {y2} {duration_ms}")
        return res.returncode == 0

    def back(self) -> bool:
        res = self._run("shell input keyevent KEYCODE_BACK")
        return res.returncode == 0

    def home(self) -> bool:
        res = self._run("shell input keyevent KEYCODE_HOME")
        return res.returncode == 0
