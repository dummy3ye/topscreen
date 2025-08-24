# topscreen — Scrcpy Overlay Tool

Lightweight transparent overlay for interacting with an Android device via ADB while scrcpy mirrors the device screen. The overlay provides clickable controls and keyboard shortcuts to send common ADB actions (tap, swipe, back, home). Designed to be modular and easy to extend.

Supported: Python 3.10+, PyQt5. Works on Linux / macOS / Windows where Python, adb (Android platform-tools) and optionally scrcpy are available.

## Features
- Frameless, transparent, always-on-top overlay window.
- Clickable buttons: Tap, Swipe, Back, Home.
- Keyboard shortcuts mapped to the same actions.
- Modular code: GUI (overlay/window.py) and ADB logic (overlay/actions.py) separated.
- Configurable coordinates (in code) for quick edits; easy to add JSON config later.
- Attempts to start `scrcpy` automatically if available; overlay still works without scrcpy.

## Quick start

1. Clone repo (if not already):
```bash
git clone https://github.com/dummy3ye/topscreen.git
cd topscreen
```

2. Create and activate a virtual environment (recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Ensure adb is installed and your device is connected:
```bash
adb devices
# It should list your device. If not, check USB/debug settings or adb installation.
```

5. Run the app:
```bash
python main.py
```
- If `scrcpy` is on PATH, the launcher will attempt to start it automatically.
- If you prefer to start scrcpy manually, run `scrcpy` in a separate terminal before or after launching the overlay.

## Commands & behavior

- Tap: Sends an adb input tap to configured coordinates.
- Swipe: Sends an adb input swipe between two configured coordinates (duration configurable).
- Back: Sends adb "input keyevent KEYCODE_BACK".
- Home: Sends adb "input keyevent KEYCODE_HOME".

Keyboard shortcuts (default)
- T — Tap
- S — Swipe
- B — Back
- H — Home

(You can change or expand these in the GUI module where shortcuts are registered, see Development section.)

## Configuration

Currently coordinates and durations are stored in code for simplicity. Edit the defaults in:
- `overlay/actions.py` — ADBConfig (contains fields such as tap_x, tap_y, swipe_start, swipe_end, swipe_duration)

Example snippet (edit these values to match your device/scrcpy window layout):
```python
# overlay/actions.py (example)
ADBConfig(
    tap_x=540,             # example x
    tap_y=960,             # example y
    swipe_start=(300, 1600),
    swipe_end=(800, 1600),
    swipe_duration=300     # ms
)
```

Future: You may add a JSON config loader and persist user settings to `overlay/config.json` then load those values at startup.

## Developer notes

Project layout (important files)
- `main.py` — launcher, tries to start scrcpy and initializes the Qt app.
- `overlay/__init__.py` — package shim (lazy-loads heavy GUI module).
- `overlay/init.py` — relocated initializer (keeps package re-exports consistent).
- `overlay/actions.py` — ADBController and configuration.
- `overlay/window.py` — PyQt5 overlay window (buttons, shortcuts, visual feedback).
- `requirements.txt` — PyQt5

Run the overlay in a headless dev container with X forwarding or a GUI session. On Ubuntu dev containers, ensure a working X11/Wayland socket or use remote desktop.

Unit testing suggestion
- Mock subprocess calls to `adb` and verify command arguments are constructed correctly.
- Example test libraries: `pytest` + `unittest.mock`.

Example: Run a quick import smoke test (no GUI required)
```bash
python -c "from overlay.actions import ADBController; print('ADB default:', ADBController().adb_cmd)"
```

## Troubleshooting

- "adb: command not found" — Install Android platform-tools and ensure `adb` is on PATH.
  - Debian/Ubuntu: install platform-tools manually (Google's package) or use package manager where available.
- scrcpy not found — install scrcpy or ignore; overlay still sends adb commands regardless.
- Transparent window not working (Linux) — compositor differences: ensure a compositing window manager is running and Qt supports translucency on your system.
- PyQt5 install issues — ensure your environment and pip are up-to-date. On Linux you may need OS packages for Qt dev headers in edge cases.

## Cross-platform notes

- Commands use Python subprocess list-style arguments and call `adb` and `scrcpy` by name; ensure those tools are installed per-platform:
  - Windows: Add `adb.exe` and `scrcpy.exe` to PATH.
  - macOS: Use Homebrew or platform packages.
  - Linux: Use distribution packages or official downloads (Android SDK platform-tools / scrcpy binary).

## Contributing

- Use branches and open a pull request.
- Keep GUI import lightweight for tests: `overlay/__init__.py` lazy-loads the PyQt-based `window` module to avoid requiring GUI on import.
- Add unit tests for `overlay/actions.py` by mocking subprocess calls.

## License

Choose an appropriate license for your project (e.g. MIT). Add a `LICENSE` file at the repo root.

## Contact / References

- scrcpy: https://github.com/Genymobile/scrcpy
- Android platform-tools / adb: https://developer.android.com/studio/command-line/adb

---
