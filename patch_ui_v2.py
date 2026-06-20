import re
from pathlib import Path

filepath = "/Users/sknaimuddin/Desktop/GAntigravity/Nebula AI/ui.py"
with open(filepath, "r") as f:
    content = f.read()

avatar_canvas_code = """
from PyQt6.QtGui import QMovie

class AvatarCanvas(QWidget):
    def __init__(self, face_path: str, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 300)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        self.muted = False
        self._speaking = False
        self.state = "INITIALISING"
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)
        
        # Load movies
        base_dir = Path(__file__).resolve().parent
        self.movie_idle = QMovie(str(base_dir / "avatar.gif"))
        self.movie_talking = QMovie(str(base_dir / "avatar.gif"))
        
        if not self.movie_idle.isValid():
            self.label.setText("Missing avatar.gif\\nPlease place them in the folder.")
            self.label.setStyleSheet(f"color: {C.PRI}; font: 14pt 'Courier New';")
        else:
            self.label.setMovie(self.movie_idle)
            self.movie_idle.start()

    @property
    def speaking(self) -> bool:
        return self._speaking
        
    @speaking.setter
    def speaking(self, val: bool):
        if val == self._speaking:
            return
        self._speaking = val
        
        if not self.movie_idle.isValid() or not self.movie_talking.isValid():
            return
            
        if self._speaking:
            self.movie_idle.stop()
            self.label.setMovie(self.movie_talking)
            self.movie_talking.start()
        else:
            self.movie_talking.stop()
            self.label.setMovie(self.movie_idle)
            self.movie_idle.start()

    def update(self):
        super().update()
"""

# The regex should match from class HudCanvas(QWidget): to the start of class MetricBar
pattern = re.compile(r"class HudCanvas\(QWidget\):.*?(?=^class MetricBar)", re.MULTILINE | re.DOTALL)
new_content = pattern.sub(avatar_canvas_code + "\n\n", content)

# Replace the instantiation in MainWindow
new_content = new_content.replace("self.hud = HudCanvas(face_path)", "self.hud = AvatarCanvas(face_path)")

with open(filepath, "w") as f:
    f.write(new_content)
    
print("Patched successfully." if new_content != content else "Patch failed.")
