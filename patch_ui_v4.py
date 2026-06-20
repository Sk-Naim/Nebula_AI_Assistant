import re
from pathlib import Path

filepath = "/Users/sknaimuddin/Desktop/GAntigravity/Nebula AI/ui.py"
with open(filepath, "r") as f:
    content = f.read()

# Modify HudCanvas to be rectangular and fit the box
hud_code = """
from PyQt6.QtGui import QMovie

class HudCanvas(QWidget):
    def __init__(self, face_path: str, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 400)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        self.muted = False
        self._speaking = False
        self.state = "INITIALISING"
        
        self._tick = 0
        self._halo = 0.0
        self._scale = 1.0
        self._blink = True
        self._scan = 0.0
        self._scan2 = 180.0
        
        self._rings = [0.0, 120.0, 240.0]
        self._ring_speeds = [1.5, -2.0, 1.0]
        self._pulses = []
        self._particles = []
        
        # GIF for talking
        base_dir = Path(__file__).resolve().parent
        self.movie = QMovie(str(base_dir / "nebula.gif"))
        
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setMovie(self.movie)
        self.label.hide()
        
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_tick)
        self._timer.start(30)

    @property
    def speaking(self) -> bool:
        return self._speaking

    @speaking.setter
    def speaking(self, val: bool):
        if self._speaking != val:
            self._speaking = val
            if self._speaking:
                self.label.show()
                self.movie.start()
            else:
                self.movie.stop()
                self.label.hide()

    def _update_tick(self):
        self._tick += 1
        W, H = self.width(), self.height()
        cx, cy = W / 2, H / 2
        fw = min(W, H)
        
        # Position label to fit the rectangular box (with some margins)
        margin = 40
        lw, lh = W - margin*2, H - margin*2
        self.label.setGeometry(margin, margin, lw, lh)
        
        if self.movie.isValid():
            self.movie.setScaledSize(QSize(lw, lh))
        
        # Remove any mask (ensure it's rectangular)
        self.label.setMask(QRegion())
        
        for i in range(len(self._rings)):
            self._rings[i] = (self._rings[i] + self._ring_speeds[i]) % 360
            
        self._scan = (self._scan + 3.0) % 360
        self._scan2 = (self._scan2 - 4.0) % 360
        
        if self._speaking:
            self._halo = min(1.0, self._halo + 0.1)
            self._scale = 1.0 + math.sin(self._tick * 0.5) * 0.05
        else:
            self._halo = max(0.0, self._halo - 0.05)
            self._scale = 1.0
            
        for i in range(len(self._pulses)-1, -1, -1):
            self._pulses[i] += 4.0
            if self._pulses[i] > fw * 0.7:
                self._pulses.pop(i)
        
        if len(self._particles) < 60:
            angle = random.uniform(0, math.pi * 2)
            dist = random.uniform(20, 250)
            self._particles.append([
                cx + math.cos(angle) * dist,
                cy + math.sin(angle) * dist,
                math.cos(angle) * random.uniform(0.5, 2.0),
                math.sin(angle) * random.uniform(0.5, 2.0),
                random.uniform(0.2, 1.0)
            ])
            
        for p in self._particles:
            p[0] += p[2]
            p[1] += p[3]
            p[4] -= 0.015
        self._particles = [p for p in self._particles if p[4] > 0]
        
        self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), qcol(C.BG))

        W, H = self.width(), self.height()
        cx, cy = W / 2, H / 2
        fw = min(W, H)

        # Subtle background glow
        grad = QRadialGradient(cx, cy, fw * 0.8)
        grad.setColorAt(0, qcol(C.PRI_GHO, 60))
        grad.setColorAt(1, qcol(C.BG, 0))
        p.fillRect(self.rect(), QBrush(grad))

        # grid dots
        p.setPen(QPen(qcol(C.PRI_GHO), 1))
        for x in range(0, W, 48):
            for y in range(0, H, 48):
                p.drawPoint(x, y)

        # pulse rings (only if not speaking or layered)
        for pr in self._pulses:
            a   = max(0, int(150 * (1.0 - pr / (fw * 0.8))))
            col = qcol(C.MUTED_C if self.muted else C.PRI, a)
            p.setPen(QPen(col, 1.5)); p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawEllipse(QRectF(cx - pr, cy - pr, pr * 2, pr * 2))

        # tick marks
        t_out, t_in = fw * 0.49, fw * 0.47
        p.setPen(QPen(qcol(C.PRI, 100), 1))
        for deg in range(0, 360, 10):
            rad = math.radians(deg)
            p.drawLine(
                QPointF(cx + t_out * math.cos(rad), cy - t_out * math.sin(rad)),
                QPointF(cx + t_in  * math.cos(rad), cy - t_in  * math.sin(rad)),
            )

        # status text
        sy = H - 80
        if self.muted:
            txt, col = "⊘  MUTED",     qcol(C.MUTED_C)
        elif self.speaking:
            txt, col = "●  SPEAKING",  qcol(C.PRI)
        elif self.state == "THINKING":
            txt, col = "◈  THINKING",   qcol(C.ACC)
        elif self.state == "LISTENING":
            txt, col = "●  LISTENING",  qcol(C.GREEN)
        else:
            txt, col = f"●  {self.state}", qcol(C.PRI)

        p.setPen(QPen(col, 1))
        p.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        p.drawText(QRectF(0, sy, W, 30), Qt.AlignmentFlag.AlignCenter, txt)

        # waveform
        wy = sy + 35
        N, bw = 40, 8
        wx0 = (W - N * bw) / 2
        for i in range(N):
            if self.muted: hgt, cl = 2, qcol(C.MUTED_C)
            elif self.speaking: hgt, cl = random.randint(3, 25), qcol(C.PRI)
            else: hgt, cl = int(3 + 3 * math.sin(self._tick * 0.09 + i * 0.6)), qcol(C.BORDER_B)
            p.fillRect(QRectF(wx0 + i * bw, wy + 20 - hgt, bw - 1, hgt), cl)
"""

pattern_hud = re.compile(r"class HudCanvas\(QWidget\):.*?(?=class MetricBar)", re.DOTALL)
content = pattern_hud.sub(hud_code, content)

with open(filepath, "w") as f:
    f.write(content)
