#!/usr/bin/env python3
"""topscreen - Scrcpy overlay launcher

This script starts scrcpy (if available) and launches a small transparent
overlay window with buttons and keyboard shortcuts to send ADB input events.

Usage: python main.py
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

from overlay.actions import ADBController
from overlay.window import OverlayWindow


def find_executable(name: str) -> Optional[str]:
	return shutil.which(name)


def main() -> int:
	# Try to start scrcpy if available; don't fail if it's not
	scrcpy_path = find_executable("scrcpy")
	scrcpy_proc = None
	if scrcpy_path:
		try:
			scrcpy_proc = subprocess.Popen([scrcpy_path])
			print("Started scrcpy (pid=%s)" % scrcpy_proc.pid)
		except Exception as exc:  # pragma: no cover - system dependent
			print("Failed to start scrcpy:", exc)
	else:
		print("scrcpy not found in PATH. You can still use the overlay with adb.")

	# Launch Qt overlay
	try:
		from PyQt5 import QtWidgets  # type: ignore
	except Exception as exc:  # pragma: no cover - user environment
		print("PyQt5 import failed:", exc)
		return 2

	app = QtWidgets.QApplication(sys.argv)

	adb = ADBController()
	win = OverlayWindow(adb_controller=adb)
	win.show()

	try:
		rc = app.exec_()
	finally:
		# Cleanup scrcpy if we started it
		if scrcpy_proc and scrcpy_proc.poll() is None:
			try:
				scrcpy_proc.terminate()
			except Exception:
				pass

	return int(rc)


if __name__ == "__main__":
	raise SystemExit(main())

