# topscreen — Scrcpy Overlay Tool

topscreen is a small Python utility that places a transparent always-on-top
overlay over your desktop and provides quick buttons and keyboard shortcuts
to send ADB input events (tap, swipe, back, home) to a connected Android
device. It pairs nicely with scrcpy which mirrors the device screen.

Features
- Transparent, draggable, always-on-top overlay window
- Clickable buttons for Tap, Swipe, Back, Home
- Keyboard shortcuts: T, S, B, H
- Modular code (separate GUI and ADB helper modules)
- Configurable coordinates via `ADBConfig` in `overlay/actions.py`

Requirements
- Python 3.10+
- PyQt5
- adb (Android platform-tools) on PATH
- (Optional) scrcpy for live mirroring

Installation
1. Create a virtualenv and activate it.
2. Install requirements:

```bash
pip install -r requirements.txt
```

Usage
1. Connect your Android device via USB (or make sure adb can see it).
2. Optionally start scrcpy or let the app try to start it for you:

```bash
python main.py
```

3. Use the overlay buttons or press keys (T/S/B/H) to send input events.

Configuration
- Default coordinates are stored in `ADBConfig` in `overlay/actions.py`.
	Edit `tap_coords`, `swipe_start`, `swipe_end`, and `swipe_duration_ms` to
	customize behavior. In the future this can be moved to a JSON or GUI.

Development notes
- The overlay uses PyQt5's translucent window features; behavior may vary
	slightly by OS/compositor. Tested on Linux and Windows with Python 3.10+.

Security and safety
- This tool shells out to `adb` and requires a trusted device. It does not
	ship ADB binaries. Use at your own risk.

License
MIT

