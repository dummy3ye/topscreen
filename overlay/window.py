"""Overlay GUI window for topscreen using PyQt5

Creates a frameless, transparent, always-on-top window with some buttons and
keyboard shortcuts that trigger ADBController actions.
"""
from __future__ import annotations

from typing import Optional

from PyQt5 import QtCore, QtGui, QtWidgets  # type: ignore

from .actions import ADBController, ADBConfig


class OverlayWindow(QtWidgets.QWidget):
    def __init__(self, adb_controller: Optional[ADBController] = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("topscreen overlay")
        self.adb = adb_controller or ADBController()
        self.config = self.adb.config

        self._setup_window()
        self._build_ui()
        self._setup_shortcuts()

    def _setup_window(self) -> None:
        # Frameless, always-on-top, transparent
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.Tool
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFixedSize(220, 120)

    def _build_ui(self) -> None:
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        row = QtWidgets.QHBoxLayout()

        btn_tap = QtWidgets.QPushButton("Tap")
        btn_tap.clicked.connect(self._on_tap)
        row.addWidget(btn_tap)

        btn_swipe = QtWidgets.QPushButton("Swipe")
        btn_swipe.clicked.connect(self._on_swipe)
        row.addWidget(btn_swipe)

        layout.addLayout(row)

        row2 = QtWidgets.QHBoxLayout()
        btn_back = QtWidgets.QPushButton("Back")
        btn_back.clicked.connect(self._on_back)
        row2.addWidget(btn_back)

        btn_home = QtWidgets.QPushButton("Home")
        btn_home.clicked.connect(self._on_home)
        row2.addWidget(btn_home)

        layout.addLayout(row2)

        note = QtWidgets.QLabel("Shortcuts: T=Tap, S=Swipe, B=Back, H=Home")
        note.setStyleSheet("color: white; font-size: 10px;")
        layout.addWidget(note)

        # Small drop shadow for readability
        effect = QtWidgets.QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(10)
        effect.setOffset(0, 2)
        self.setGraphicsEffect(effect)

    def _setup_shortcuts(self) -> None:
        QtWidgets.QShortcut(QtGui.QKeySequence("T"), self, activated=self._on_tap)
        QtWidgets.QShortcut(QtGui.QKeySequence("S"), self, activated=self._on_swipe)
        QtWidgets.QShortcut(QtGui.QKeySequence("B"), self, activated=self._on_back)
        QtWidgets.QShortcut(QtGui.QKeySequence("H"), self, activated=self._on_home)

    # Event handlers
    def _on_tap(self) -> None:
        success = self.adb.tap(*self.config.tap_coords)
        self._flash_feedback(success)

    def _on_swipe(self) -> None:
        success = self.adb.swipe(
            *self.config.swipe_start, *self.config.swipe_end, self.config.swipe_duration_ms
        )
        self._flash_feedback(success)

    def _on_back(self) -> None:
        success = self.adb.back()
        self._flash_feedback(success)

    def _on_home(self) -> None:
        success = self.adb.home()
        self._flash_feedback(success)

    def _flash_feedback(self, success: bool) -> None:
        # Tiny visual feedback: briefly change background color
        color = "#2ecc71" if success else "#e74c3c"
        old = self.styleSheet()
        self.setStyleSheet(f"background-color: {color}; border-radius: 8px;")
        QtCore.QTimer.singleShot(160, lambda: self.setStyleSheet(old))

    # Allow window to be dragged
    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:  # type: ignore[override]
        if event.button() == QtCore.Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:  # type: ignore[override]
        if getattr(self, "_drag_pos", None) and event.buttons() & QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()
