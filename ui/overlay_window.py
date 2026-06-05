
from PyQt6.QtWidgets import QWidget,QVBoxLayout,QLabel,QTextEdit,QApplication
from PyQt6.QtCore import Qt,pyqtSignal

class OverlayWindow(QWidget):

    update_signal = pyqtSignal(str,str)

    def __init__(self):
        super().__init__()

        self.status = QLabel("Ready")
        self.text = QTextEdit()
        self.text.setReadOnly(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.status)
        layout.addWidget(self.text)

        self.resize(520,380)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        geo = QApplication.primaryScreen().availableGeometry()
        self.move(geo.width()-540, geo.height()-420)

        self.update_signal.connect(self._update)

    def _update(self,status,text):
        self.status.setText(status)
        self.text.setPlainText(text)
