import re
from pathlib import Path

filepath = "/Users/sknaimuddin/Desktop/GAntigravity/Nebula AI/ui.py"
with open(filepath, "r") as f:
    content = f.read()

# Update C class for pink/purple
pattern_c = re.compile(r"class C:.*?BAR_BG    = \"#011520\"", re.DOTALL)
new_c = """class C:
    BG        = "#00060a"
    PANEL     = "#11001c"
    PANEL2    = "#1a002b"
    BORDER    = "#2d004d"
    BORDER_B  = "#4a0080"
    BORDER_A  = "#2a0040"
    PRI       = "#ff00bf" # neon pink
    PRI_DIM   = "#990073"
    PRI_GHO   = "#330026"
    ACC       = "#d400ff" # purple
    ACC2      = "#ff00ff"
    GREEN     = "#00ff88"
    GREEN_D   = "#00aa55"
    RED       = "#ff3355"
    MUTED_C   = "#ff3366"
    TEXT      = "#ffccf2"
    TEXT_DIM  = "#d98cb3"
    TEXT_MED  = "#e6b3cc"
    WHITE     = "#ffffff"
    DARK      = "#0a0014"
    BAR_BG    = "#200033" """
content = pattern_c.sub(new_c, content)

# Update HudCanvas to include GIF and bigger size
hud_code = """
from PyQt6.QtGui import QMovie, QRegion

class HudCanvas(QWidget):
    def __init__(self, face_path: str, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 400) # Bigger
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
        orb_r = int(fw * 0.35 * self._scale) # Bigger orb
        
        # Position label in center
        lsz = orb_r * 2
        self.label.setGeometry(int(cx - orb_r), int(cy - orb_r), lsz, lsz)
        if self.movie.isValid():
            self.movie.setScaledSize(QSize(lsz, lsz))
            
            # Mask label to be circular
            path = QPainterPath()
            path.addEllipse(0, 0, lsz, lsz)
            region = QRegion(path.toFillPolygon().toPolygon())
            self.label.setMask(region)
        
        for i in range(len(self._rings)):
            self._rings[i] = (self._rings[i] + self._ring_speeds[i]) % 360
            
        self._scan = (self._scan + 3.0) % 360
        self._scan2 = (self._scan2 - 4.0) % 360
        
        if self._speaking:
            self._halo = min(1.0, self._halo + 0.1)
            self._scale = 1.0 + math.sin(self._tick * 0.5) * 0.05
            if self._tick % 10 == 0:
                self._pulses.append(0.0)
        else:
            self._halo = max(0.0, self._halo - 0.05)
            self._scale = 1.0
            
        for i in range(len(self._pulses)-1, -1, -1):
            self._pulses[i] += 4.0
            if self._pulses[i] > fw * 0.5:
                self._pulses.pop(i)
                
        if self._tick % 15 == 0:
            self._blink = not self._blink
            
        if len(self._particles) < 60:
            cx, cy = self.width() / 2, self.height() / 2
            angle = random.uniform(0, math.pi * 2)
            dist = random.uniform(20, 200)
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

        # Nebula background glow
        grad = QRadialGradient(cx, cy, fw * 0.6)
        grad.setColorAt(0, qcol(C.PRI, 40))
        grad.setColorAt(1, qcol(C.BG, 0))
        p.fillRect(self.rect(), QBrush(grad))

        # grid dots
        p.setPen(QPen(qcol(C.PRI_GHO), 1))
        for x in range(0, W, 48):
            for y in range(0, H, 48):
                p.drawPoint(x, y)

        r_face = fw * 0.38 # Bigger

        # halo glow
        for i in range(10):
            r   = r_face * (1.8 - i * 0.08)
            frc = 1.0 - i / 10
            a   = max(0, min(255, int(self._halo * 0.085 * frc)))
            col = qcol(C.MUTED_C if self.muted else C.PRI, a)
            p.setPen(QPen(col, 1.5)); p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawEllipse(QRectF(cx - r, cy - r, r * 2, r * 2))

        # pulse rings
        for pr in self._pulses:
            a   = max(0, int(230 * (1.0 - pr / (fw * 0.74))))
            col = qcol(C.MUTED_C if self.muted else C.PRI, a)
            p.setPen(QPen(col, 1.5)); p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawEllipse(QRectF(cx - pr, cy - pr, pr * 2, pr * 2))

        # spinning arc rings
        for idx, (r_frac, w_r, arc_l, gap) in enumerate([(0.48, 3, 115, 78), (0.40, 2, 78, 55), (0.32, 1, 56, 40)]):
            ring_r = fw * r_frac
            base   = self._rings[idx]
            a_val  = max(0, min(255, int(self._halo * (1.0 - idx * 0.18))))
            col    = qcol(C.MUTED_C if self.muted else C.PRI, a_val)
            p.setPen(QPen(col, w_r)); p.setBrush(Qt.BrushStyle.NoBrush)
            angle = base
            rect  = QRectF(cx - ring_r, cy - ring_r, ring_r * 2, ring_r * 2)
            while angle < base + 360:
                p.drawArc(rect, int(angle * 16), int(arc_l * 16))
                angle += arc_l + gap

        # scanners
        sr = fw * 0.50
        sa = min(255, int(self._halo * 1.5))
        ex = 75 if self.speaking else 44
        p.setPen(QPen(qcol(C.MUTED_C if self.muted else C.PRI, sa), 2.5))
        p.setBrush(Qt.BrushStyle.NoBrush)
        srect = QRectF(cx - sr, cy - sr, sr * 2, sr * 2)
        p.drawArc(srect, int(self._scan * 16), int(ex * 16))
        p.setPen(QPen(qcol(C.ACC, sa // 2), 1.5))
        p.drawArc(srect, int(self._scan2 * 16), int(ex * 16))

        # tick marks
        t_out, t_in = fw * 0.497, fw * 0.474
        p.setPen(QPen(qcol(C.PRI, 140), 1))
        for deg in range(0, 360, 10):
            rad = math.radians(deg)
            inn = t_in if deg % 30 == 0 else t_in + 6
            p.drawLine(
                QPointF(cx + t_out * math.cos(rad), cy - t_out * math.sin(rad)),
                QPointF(cx + inn  * math.cos(rad), cy - inn  * math.sin(rad)),
            )

        # corner brackets
        bl = 24
        bc = qcol(C.PRI, 210)
        hl, hr = cx - fw // 2, cx + fw // 2
        ht, hb = cy - fw // 2, cy + fw // 2
        p.setPen(QPen(bc, 2))
        for bx, by, dx, dy in [(hl,ht,1,1),(hr,ht,-1,1),(hl,hb,1,-1),(hr,hb,-1,-1)]:
            p.drawLine(QPointF(bx, by), QPointF(bx + dx * bl, by))
            p.drawLine(QPointF(bx, by), QPointF(bx, by + dy * bl))

        # Central orb
        orb_r = int(fw * 0.35 * self._scale)
        if not self._speaking:
            oc = (200, 0, 50) if self.muted else (120, 0, 180) # purple
            for i in range(8, 0, -1):
                r2  = int(orb_r * i / 8)
                frc = i / 8
                a   = max(0, min(255, int(self._halo * 1.1 * frc) + 30))
                p.setBrush(QBrush(QColor(int(oc[0]*frc), int(oc[1]*frc), int(oc[2]*frc), a)))
                p.setPen(Qt.PenStyle.NoPen)
                p.drawEllipse(QRectF(cx - r2, cy - r2, r2 * 2, r2 * 2))
        
        # Text label
        p.setPen(QPen(qcol(C.PRI, min(255, int(self._halo * 2) + 150)), 1))
        p.setFont(QFont("Courier New", 14, QFont.Weight.Bold))
        p.drawText(QRectF(cx - 100, cy + orb_r + 10, 200, 30), Qt.AlignmentFlag.AlignCenter, "NEBULA AI")

        # particles
        for pt in self._particles:
            a = max(0, min(255, int(pt[4] * 255)))
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QBrush(qcol(C.PRI, a)))
            p.drawEllipse(QPointF(pt[0], pt[1]), 2.5, 2.5)

        # status text
        sy = cy + fw * 0.45
        if self.muted:
            txt, col = "⊘  MUTED",     qcol(C.MUTED_C)
        elif self.speaking:
            txt, col = "●  SPEAKING",  qcol(C.PRI)
        elif self.state == "THINKING":
            sym = "◈" if self._blink else "◇"
            txt, col = f"{sym}  THINKING",   qcol(C.ACC)
        elif self.state == "PROCESSING":
            sym = "▷" if self._blink else "▶"
            txt, col = f"{sym}  PROCESSING", qcol(C.ACC)
        elif self.state == "LISTENING":
            sym = "●" if self._blink else "○"
            txt, col = f"{sym}  LISTENING",  qcol(C.GREEN)
        else:
            sym = "●" if self._blink else "○"
            txt, col = f"{sym}  {self.state}", qcol(C.PRI)

        p.setPen(QPen(col, 1))
        p.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        p.drawText(QRectF(0, sy, W, 30), Qt.AlignmentFlag.AlignCenter, txt)

        # waveform
        wy = sy + 35
        N, bw = 36, 8
        wx0 = (W - N * bw) / 2
        for i in range(N):
            if self.muted:
                hgt, cl = 2, qcol(C.MUTED_C)
            elif self.speaking:
                hgt = random.randint(3, 25)
                cl  = qcol(C.PRI) if hgt > 15 else qcol(C.PRI_DIM)
            else:
                hgt = int(3 + 3 * math.sin(self._tick * 0.09 + i * 0.6))
                cl  = qcol(C.BORDER_B)
            p.fillRect(QRectF(wx0 + i * bw, wy + 20 - hgt, bw - 1, hgt), cl)
"""

pattern_hud = re.compile(r"class HudCanvas\(QWidget\):.*?(?=class MetricBar)", re.DOTALL)
content = pattern_hud.sub(hud_code, content)

with open(filepath, "w") as f:
    f.write(content)
