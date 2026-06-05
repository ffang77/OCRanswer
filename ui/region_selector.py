from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QColor, QFont

class RegionSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.begin = None
        self.end = None
        self.region = None

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        self.setCursor(Qt.CursorShape.CrossCursor)
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Escape:
            self.region = None
            self.close()

    def mousePressEvent(self, e):
        self.begin = e.pos()
        self.end = e.pos()

    def mouseMoveEvent(self, e):
        self.end = e.pos()
        self.update()

    def mouseReleaseEvent(self, e):
        rect = QRect(self.begin, self.end).normalized()
        self.region = {
            "left": rect.left(),
            "top": rect.top(),
            "width": rect.width(),
            "height": rect.height()
        }
        self.close()

    def paintEvent(self, e):
        p = QPainter(self)
        p.fillRect(self.rect(), QColor(0, 0, 0, 40))
        if self.begin and self.end:
            p.setPen(Qt.GlobalColor.red)
            p.drawRect(QRect(self.begin, self.end).normalized())
        # hint text
        p.setPen(Qt.GlobalColor.white)
        p.setFont(QFont("Arial", 18))
        p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "拖拽鼠标选择监控区域  |  ESC 取消")
