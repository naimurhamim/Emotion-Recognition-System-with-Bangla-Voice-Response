import sys
import os
import base64
import json
import threading
import urllib.request
import urllib.error

import cv2
import numpy as np

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QLineEdit, QFrame, QProgressBar,
    QGraphicsDropShadowEffect, QSizePolicy
)
from PyQt6.QtCore import (
    Qt, QTimer, QThread, pyqtSignal, QPropertyAnimation,
    QEasingCurve, QSize
)
from PyQt6.QtGui import (
    QImage, QPixmap, QFont, QColor, QPalette, QLinearGradient,
    QPainter, QBrush, QPen, QFontDatabase
)
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl

# ── Constants ─────────────────────────────────────────────────────────────────
API_BASE = "http://127.0.0.1:8000"

COLORS = {
    "black":      "#0a0a0a",
    "black2":     "#111111",
    "black3":     "#1a1a1a",
    "black4":     "#222222",
    "black5":     "#2a2a2a",
    "gold":       "#d4af37",
    "gold2":      "#c9a227",
    "gold3":      "#b8941f",
    "silver":     "#c0c0c0",
    "silver2":    "#a8a8a8",
    "silver3":    "#888888",
    "silver_dim": "#555555",
    "text":       "#e8e8e8",
    "text2":      "#a0a0a0",
    "danger":     "#c0392b",
    "success":    "#27ae60",
}

EMOTION_COLORS = {
    "happy":     "#d4af37",
    "sad":       "#3498db",
    "depressed": "#8e44ad",
    "angry":     "#c0392b",
    "surprised": "#e67e22",
    "fear":      "#7f8c8d",
    "disgust":   "#27ae60",
    "neutral":   "#888888",
}

EMOTION_LABELS = {
    "happy": "HAPPY", "sad": "SAD", "depressed": "DEPRESSED",
    "angry": "ANGRY", "surprised": "SURPRISED", "fear": "FEAR",
    "disgust": "DISGUST", "neutral": "NEUTRAL",
}


# ── Worker Thread for API Call ────────────────────────────────────────────────
class AnalyzeWorker(QThread):
    result_ready = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, frames_b64, user_name):
        super().__init__()
        self.frames_b64 = frames_b64
        self.user_name = user_name

    def run(self):
        try:
            payload = json.dumps({
                "frames": self.frames_b64,
                "user_name": self.user_name
            }).encode("utf-8")

            req = urllib.request.Request(
                f"{API_BASE}/analyze",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                self.result_ready.emit(data)
        except urllib.error.URLError as e:
            self.error_occurred.emit(f"API bağlantı hatası: {str(e)}\nBackend চালু আছে কি? python run.py")
        except Exception as e:
            self.error_occurred.emit(str(e))


# ── Styled Widgets ────────────────────────────────────────────────────────────
def make_shadow(radius=20, color="#d4af37", opacity=60):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(radius)
    c = QColor(color)
    c.setAlpha(opacity)
    shadow.setColor(c)
    shadow.setOffset(0, 0)
    return shadow

def styled_btn(text, color="silver"):
    btn = QPushButton(text)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setMinimumHeight(40)
    btn.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
    if color == "gold":
        btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 {COLORS['gold']}, stop:1 {COLORS['gold3']});
                color: #0a0a0a;
                border: none;
                border-radius: 8px;
                padding: 8px 20px;
                font-weight: bold;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{ background: {COLORS['gold2']}; }}
            QPushButton:disabled {{ opacity: 0.4; background: #444; color: #888; }}
        """)
    elif color == "danger":
        btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {COLORS['danger']};
                border: 1px solid {COLORS['danger']};
                border-radius: 8px;
                padding: 8px 20px;
            }}
            QPushButton:hover {{ background: {COLORS['danger']}; color: white; }}
            QPushButton:disabled {{ opacity: 0.3; }}
        """)
    else:
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLORS['black4']};
                color: {COLORS['silver']};
                border: 1px solid {COLORS['silver_dim']};
                border-radius: 8px;
                padding: 8px 20px;
            }}
            QPushButton:hover {{ background: {COLORS['black5']}; color: {COLORS['text']}; border-color: {COLORS['silver2']}; }}
            QPushButton:disabled {{ opacity: 0.3; }}
        """)
    return btn


# ── Camera Panel ──────────────────────────────────────────────────────────────
class CameraPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_frame)
        self.current_frame = None
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['black2']};
                border: 1px solid {COLORS['black5']};
                border-radius: 16px;
            }}
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        # Title
        title = QLabel("● LIVE CAMERA")
        title.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {COLORS['silver2']}; letter-spacing: 2px; background: transparent; border: none;")
        layout.addWidget(title)

        # Name input
        name_lbl = QLabel("YOUR NAME")
        name_lbl.setFont(QFont("Segoe UI", 7, QFont.Weight.Bold))
        name_lbl.setStyleSheet(f"color: {COLORS['text2']}; letter-spacing: 1px; background: transparent; border: none;")
        layout.addWidget(name_lbl)

        self.name_input = QLineEdit("নাঈমুর")
        self.name_input.setMinimumHeight(36)
        self.name_input.setFont(QFont("Segoe UI", 10))
        self.name_input.setStyleSheet(f"""
            QLineEdit {{
                background: {COLORS['black3']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['black5']};
                border-radius: 8px;
                padding: 6px 12px;
            }}
            QLineEdit:focus {{ border-color: {COLORS['gold3']}; }}
        """)
        layout.addWidget(self.name_input)

        # Video display
        self.video_label = QLabel()
        self.video_label.setMinimumSize(400, 300)
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setStyleSheet(f"""
            QLabel {{
                background: {COLORS['black3']};
                border: 1px solid {COLORS['black5']};
                border-radius: 10px;
                color: {COLORS['silver_dim']};
                font-size: 12px;
                letter-spacing: 2px;
            }}
        """)
        self.video_label.setText("CAMERA OFF")
        layout.addWidget(self.video_label)

        # Camera buttons
        btn_row = QHBoxLayout()
        self.start_btn = styled_btn("Start Camera", "silver")
        self.stop_btn = styled_btn("Stop Camera", "danger")
        self.stop_btn.setEnabled(False)
        self.start_btn.clicked.connect(self.start_camera)
        self.stop_btn.clicked.connect(self.stop_camera)
        btn_row.addWidget(self.start_btn)
        btn_row.addWidget(self.stop_btn)
        layout.addLayout(btn_row)

        # Settings row
        settings_row = QHBoxLayout()

        frame_col = QVBoxLayout()
        fl = QLabel("FRAMES")
        fl.setFont(QFont("Segoe UI", 7, QFont.Weight.Bold))
        fl.setStyleSheet(f"color: {COLORS['text2']}; letter-spacing: 1px; background: transparent; border: none;")
        self.frame_combo = QComboBox()
        self.frame_combo.addItems(["3 Frames", "5 Frames", "7 Frames", "10 Frames"])
        self.frame_combo.setCurrentIndex(1)
        self._style_combo(self.frame_combo)
        frame_col.addWidget(fl)
        frame_col.addWidget(self.frame_combo)

        interval_col = QVBoxLayout()
        il = QLabel("INTERVAL")
        il.setFont(QFont("Segoe UI", 7, QFont.Weight.Bold))
        il.setStyleSheet(f"color: {COLORS['text2']}; letter-spacing: 1px; background: transparent; border: none;")
        self.interval_combo = QComboBox()
        self.interval_combo.addItems(["300ms", "500ms", "800ms"])
        self.interval_combo.setCurrentIndex(1)
        self._style_combo(self.interval_combo)
        interval_col.addWidget(il)
        interval_col.addWidget(self.interval_combo)

        settings_row.addLayout(frame_col)
        settings_row.addLayout(interval_col)
        layout.addLayout(settings_row)

        # Analyze button
        self.analyze_btn = styled_btn("  Analyze Emotion", "gold")
        self.analyze_btn.setMinimumHeight(48)
        self.analyze_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.analyze_btn.setEnabled(False)
        self.analyze_btn.setGraphicsEffect(make_shadow(24, COLORS['gold'], 80))
        layout.addWidget(self.analyze_btn)

    def _style_combo(self, combo):
        combo.setMinimumHeight(34)
        combo.setStyleSheet(f"""
            QComboBox {{
                background: {COLORS['black3']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['black5']};
                border-radius: 8px;
                padding: 4px 10px;
                font-size: 9pt;
            }}
            QComboBox::drop-down {{ border: none; }}
            QComboBox QAbstractItemView {{
                background: {COLORS['black3']};
                color: {COLORS['text']};
                selection-background-color: {COLORS['black5']};
            }}
        """)

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.video_label.setText("CAMERA NOT FOUND")
            return
        self.timer.start(33)
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.analyze_btn.setEnabled(True)

    def stop_camera(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.cap = None
        self.current_frame = None
        self.video_label.setText("CAMERA OFF")
        self.video_label.setPixmap(QPixmap())
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.analyze_btn.setEnabled(False)

    def _update_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame.copy()
                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb.shape
                img = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
                pix = QPixmap.fromImage(img).scaled(
                    self.video_label.width(), self.video_label.height(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.video_label.setPixmap(pix)

    def capture_frames(self):
        count_map = {"3 Frames": 3, "5 Frames": 5, "7 Frames": 7, "10 Frames": 10}
        interval_map = {"300ms": 0.3, "500ms": 0.5, "800ms": 0.8}
        count = count_map[self.frame_combo.currentText()]
        interval = interval_map[self.interval_combo.currentText()]
        return count, interval

    def get_frame_b64(self):
        if self.current_frame is None:
            return None
        _, buf = cv2.imencode(".jpg", self.current_frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        return base64.b64encode(buf).decode("utf-8")

    def get_user_name(self):
        return self.name_input.text().strip() or "নাঈমুর"


# ── Result Panel ──────────────────────────────────────────────────────────────
class ResultPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.player = QMediaPlayer()
        self.audio_out = QAudioOutput()
        self.player.setAudioOutput(self.audio_out)
        self.audio_out.setVolume(1.0)
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['black2']};
                border: 1px solid {COLORS['black5']};
                border-radius: 16px;
            }}
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        # Title
        title = QLabel("◆ ANALYSIS RESULT")
        title.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {COLORS['gold']}; letter-spacing: 2px; background: transparent; border: none;")
        layout.addWidget(title)

        # Emotion display box
        self.emotion_box = QFrame()
        self.emotion_box.setMinimumHeight(110)
        self.emotion_box.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['black3']};
                border: 1px solid {COLORS['black5']};
                border-radius: 12px;
            }}
        """)
        ebox_layout = QVBoxLayout(self.emotion_box)
        ebox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.emotion_icon = QLabel("?")
        self.emotion_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.emotion_icon.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        self.emotion_icon.setStyleSheet(f"color: {COLORS['silver_dim']}; background: transparent; border: none;")
        ebox_layout.addWidget(self.emotion_icon)

        self.emotion_label = QLabel("Waiting...")
        self.emotion_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.emotion_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.emotion_label.setStyleSheet(f"color: {COLORS['gold']}; letter-spacing: 2px; background: transparent; border: none;")
        ebox_layout.addWidget(self.emotion_label)

        self.emotion_sub = QLabel("Start camera and analyze")
        self.emotion_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.emotion_sub.setFont(QFont("Segoe UI", 8))
        self.emotion_sub.setStyleSheet(f"color: {COLORS['text2']}; background: transparent; border: none;")
        ebox_layout.addWidget(self.emotion_sub)

        layout.addWidget(self.emotion_box)

        # Score bars section
        score_title = QLabel("EMOTION SCORES")
        score_title.setFont(QFont("Segoe UI", 7, QFont.Weight.Bold))
        score_title.setStyleSheet(f"color: {COLORS['text2']}; letter-spacing: 1.5px; background: transparent; border: none;")
        layout.addWidget(score_title)

        self.score_container = QVBoxLayout()
        self.score_container.setSpacing(5)
        score_wrap = QWidget()
        score_wrap.setStyleSheet("background: transparent;")
        score_wrap.setLayout(self.score_container)
        layout.addWidget(score_wrap)

        self.score_placeholder = QLabel("No data yet")
        self.score_placeholder.setStyleSheet(f"color: {COLORS['silver_dim']}; font-size: 9pt; background: transparent; border: none;")
        self.score_container.addWidget(self.score_placeholder)

        # Response text
        resp_title = QLabel("RESPONSE")
        resp_title.setFont(QFont("Segoe UI", 7, QFont.Weight.Bold))
        resp_title.setStyleSheet(f"color: {COLORS['text2']}; letter-spacing: 1.5px; background: transparent; border: none;")
        layout.addWidget(resp_title)

        self.response_label = QLabel("Emotion analyze korle ekhane response ashbe...")
        self.response_label.setWordWrap(True)
        self.response_label.setFont(QFont("Segoe UI", 9))
        self.response_label.setStyleSheet(f"""
            color: {COLORS['text']};
            background: {COLORS['black3']};
            border: 1px solid {COLORS['black5']};
            border-radius: 8px;
            padding: 10px;
        """)
        self.response_label.setMinimumHeight(60)
        layout.addWidget(self.response_label)

        # Audio controls
        audio_row = QHBoxLayout()
        self.play_btn = styled_btn("▶  Play Voice", "silver")
        self.play_btn.setEnabled(False)
        self.play_btn.clicked.connect(self._play_audio)
        self.replay_btn = styled_btn("↺  Replay", "silver")
        self.replay_btn.setEnabled(False)
        self.replay_btn.clicked.connect(self._replay_audio)
        audio_row.addWidget(self.play_btn)
        audio_row.addWidget(self.replay_btn)
        layout.addLayout(audio_row)

        # Frame info
        self.frame_info = QLabel("")
        self.frame_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame_info.setFont(QFont("Segoe UI", 8))
        self.frame_info.setStyleSheet(f"color: {COLORS['silver_dim']}; background: transparent; border: none;")
        layout.addWidget(self.frame_info)

        layout.addStretch()

    def update_result(self, data):
        emotion = data.get("dominant_emotion", "neutral").lower()
        color = EMOTION_COLORS.get(emotion, COLORS['silver'])
        label = EMOTION_LABELS.get(emotion, emotion.upper())

        # Emotion box
        self.emotion_box.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['black3']};
                border: 1px solid {color};
                border-radius: 12px;
            }}
        """)
        icons = {"happy":"★","sad":"●","depressed":"▼","angry":"■","surprised":"◆","fear":"▲","disgust":"◉","neutral":"○"}
        self.emotion_icon.setText(icons.get(emotion, "?"))
        self.emotion_icon.setStyleSheet(f"color: {color}; background: transparent; border: none; font-size: 28pt; font-weight: bold;")
        self.emotion_label.setText(label)
        self.emotion_label.setStyleSheet(f"color: {color}; letter-spacing: 2px; background: transparent; border: none; font-size: 18pt; font-weight: bold;")
        self.emotion_sub.setText(f"Detected from {data.get('frame_count', 0)} frames")

        # Score bars
        self._clear_scores()
        scores = data.get("avg_scores", {})
        dominant = emotion
        if scores:
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            for emo, score in sorted_scores:
                self._add_score_bar(emo, score, emo.lower() == dominant)

        # Response
        self.response_label.setText(data.get("response_text", ""))
        self.response_label.setStyleSheet(f"""
            color: {COLORS['text']};
            background: rgba(212,175,55,0.04);
            border: 1px solid {COLORS['gold3']};
            border-radius: 8px;
            padding: 10px;
        """)

        # Audio
        audio_url = data.get("audio_url", "")
        if audio_url:
            full_url = f"{API_BASE}{audio_url}"
            self.player.setSource(QUrl(full_url))
            self.play_btn.setEnabled(True)
            self.replay_btn.setEnabled(True)
            self.player.play()

        self.frame_info.setText(f"Analyzed {data.get('frame_count', 0)} frames  •  {label}")

    def _clear_scores(self):
        while self.score_container.count():
            item = self.score_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _add_score_bar(self, emotion, score, is_dominant):
        row = QWidget()
        row.setStyleSheet("background: transparent;")
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(8)

        lbl = QLabel(emotion.capitalize())
        lbl.setFixedWidth(80)
        lbl.setFont(QFont("Segoe UI", 8))
        lbl.setStyleSheet(f"color: {COLORS['text2']}; background: transparent;")
        row_layout.addWidget(lbl)

        bar_bg = QFrame()
        bar_bg.setFixedHeight(6)
        bar_bg.setStyleSheet(f"background: {COLORS['black4']}; border-radius: 3px;")
        bar_bg.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        fill_color = COLORS['gold'] if is_dominant else COLORS['silver_dim']
        pct = min(100, int(score))
        bar_fill = QFrame(bar_bg)
        bar_fill.setFixedHeight(6)
        bar_fill.setStyleSheet(f"background: {fill_color}; border-radius: 3px;")
        bar_fill.setFixedWidth(max(4, int(pct * 2)))

        row_layout.addWidget(bar_bg)

        val = QLabel(f"{pct}%")
        val.setFixedWidth(36)
        val.setFont(QFont("Segoe UI", 8))
        val.setAlignment(Qt.AlignmentFlag.AlignRight)
        val.setStyleSheet(f"color: {COLORS['silver_dim']}; background: transparent;")
        row_layout.addWidget(val)

        self.score_container.addWidget(row)

    def _play_audio(self):
        self.player.play()

    def _replay_audio(self):
        self.player.setPosition(0)
        self.player.play()


# ── Status Bar ────────────────────────────────────────────────────────────────
class StatusBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(32)
        self.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['black2']};
                border-top: 1px solid {COLORS['black4']};
                border-radius: 0px;
            }}
        """)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)

        self.dot = QLabel("●")
        self.dot.setFont(QFont("Segoe UI", 8))
        self.dot.setStyleSheet(f"color: {COLORS['silver_dim']}; background: transparent; border: none;")
        layout.addWidget(self.dot)

        self.msg = QLabel("Ready")
        self.msg.setFont(QFont("Segoe UI", 8))
        self.msg.setStyleSheet(f"color: {COLORS['silver_dim']}; background: transparent; border: none;")
        layout.addWidget(self.msg)
        layout.addStretch()

    def set_status(self, text, state="idle"):
        self.msg.setText(text)
        colors = {"idle": COLORS['silver_dim'], "ready": COLORS['success'],
                  "loading": COLORS['gold'], "error": COLORS['danger']}
        c = colors.get(state, COLORS['silver_dim'])
        self.dot.setStyleSheet(f"color: {c}; background: transparent; border: none;")
        self.msg.setStyleSheet(f"color: {c}; background: transparent; border: none;")


# ── Main Window ───────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Emotion Recognition System")
        self.setMinimumSize(960, 680)
        self.resize(1100, 720)
        self._captured_frames = []
        self._capture_count = 0
        self._capture_target = 0
        self._capture_interval = 500
        self._capture_timer = QTimer()
        self._capture_timer.timeout.connect(self._do_capture)
        self._setup_ui()
        self._apply_global_style()

    def _apply_global_style(self):
        self.setStyleSheet(f"""
            QMainWindow {{ background: {COLORS['black']}; }}
            QWidget {{ background: {COLORS['black']}; color: {COLORS['text']}; }}
            QScrollBar {{ background: {COLORS['black3']}; }}
        """)

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = QFrame()
        header.setFixedHeight(64)
        header.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 {COLORS['black2']}, stop:1 {COLORS['black3']});
                border-bottom: 1px solid {COLORS['gold3']};
            }}
        """)
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(24, 0, 24, 0)

        logo = QLabel("◉")
        logo.setFont(QFont("Segoe UI", 18))
        logo.setStyleSheet(f"color: {COLORS['gold']}; background: transparent; border: none;")
        h_layout.addWidget(logo)

        title = QLabel("Emotion Recognition System")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {COLORS['gold']}; background: transparent; border: none; letter-spacing: 1px;")
        h_layout.addWidget(title)
        h_layout.addStretch()

        subtitle = QLabel("Your face tells a story — we listen.")
        subtitle.setFont(QFont("Segoe UI", 9))
        subtitle.setStyleSheet(f"color: {COLORS['silver3']}; font-style: italic; background: transparent; border: none;")
        h_layout.addWidget(subtitle)

        main_layout.addWidget(header)

        # Content area
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(16)

        self.cam_panel = CameraPanel()
        self.result_panel = ResultPanel()

        content_layout.addWidget(self.cam_panel, 1)
        content_layout.addWidget(self.result_panel, 1)

        main_layout.addWidget(content, 1)

        # Status bar
        self.status_bar = StatusBar()
        main_layout.addWidget(self.status_bar)

        # Connect analyze button
        self.cam_panel.analyze_btn.clicked.connect(self._start_analyze)

    def _start_analyze(self):
        if not self.cam_panel.cap:
            return

        count, interval_sec = self.cam_panel.capture_frames()
        self._captured_frames = []
        self._capture_count = 0
        self._capture_target = count
        self._capture_interval = int(interval_sec * 1000)

        self.cam_panel.analyze_btn.setEnabled(False)
        self.cam_panel.analyze_btn.setText("Capturing...")
        self.status_bar.set_status("Capturing frames...", "loading")

        self._capture_timer.start(self._capture_interval)

    def _do_capture(self):
        b64 = self.cam_panel.get_frame_b64()
        if b64:
            self._captured_frames.append(b64)
        self._capture_count += 1
        self.status_bar.set_status(
            f"Capturing frame {self._capture_count}/{self._capture_target}...", "loading"
        )

        if self._capture_count >= self._capture_target:
            self._capture_timer.stop()
            self._send_to_api()

    def _send_to_api(self):
        self.cam_panel.analyze_btn.setText("Analyzing...")
        self.status_bar.set_status("Sending to AI engine...", "loading")

        self.worker = AnalyzeWorker(
            self._captured_frames,
            self.cam_panel.get_user_name()
        )
        self.worker.result_ready.connect(self._on_result)
        self.worker.error_occurred.connect(self._on_error)
        self.worker.start()

    def _on_result(self, data):
        self.result_panel.update_result(data)
        emotion = data.get("dominant_emotion", "neutral")
        self.status_bar.set_status(f"Done — detected: {emotion.upper()}", "ready")
        self._reset_analyze_btn()

    def _on_error(self, msg):
        self.status_bar.set_status(f"Error: {msg}", "error")
        self.result_panel.response_label.setText(f"Error: {msg}")
        self._reset_analyze_btn()

    def _reset_analyze_btn(self):
        self.cam_panel.analyze_btn.setEnabled(True)
        self.cam_panel.analyze_btn.setText("  Analyze Emotion")

    def closeEvent(self, event):
        self.cam_panel.stop_camera()
        event.accept()


# ── Entry Point ───────────────────────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Dark palette
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(COLORS['black']))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(COLORS['text']))
    palette.setColor(QPalette.ColorRole.Base, QColor(COLORS['black2']))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(COLORS['black3']))
    palette.setColor(QPalette.ColorRole.Text, QColor(COLORS['text']))
    palette.setColor(QPalette.ColorRole.Button, QColor(COLORS['black3']))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(COLORS['text']))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(COLORS['gold']))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(COLORS['black']))
    app.setPalette(palette)

    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
