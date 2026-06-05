import json, time, threading, sys, os

os.environ["FLAGS_use_mkldnn"] = "0"

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from ui.overlay_window import OverlayWindow
from ui.region_selector import RegionSelector
from ui.hotkey_manager import HotkeyManager
from core.screen_capture import ScreenCapture
from core.ocr_engine import OCREngine
from core.text_detector import TextDetector
from core.deepseek_client import DeepSeekClient
from core import logger

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

def load_cfg():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_cfg(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4, ensure_ascii=False)

def region_valid(r):
    return r and r.get("width", 0) >= 50 and r.get("height", 0) >= 50

def select_region(app):
    selector = RegionSelector()
    while selector.isVisible():
        app.processEvents()
    return selector.region

app = QApplication(sys.argv)
cfg = load_cfg()

r = None
while not region_valid(r):
    r = select_region(app)
cfg["region"] = r
save_cfg(cfg)

overlay = OverlayWindow()
overlay.show()

capture = ScreenCapture()
ocr = OCREngine()
detector = TextDetector(cfg["similarity_threshold"])
client = DeepSeekClient(cfg["api_key"], cfg["base_url"], cfg["model"])

paused = threading.Event()  # set = paused

def reselect():
    paused.set()
    overlay.update_signal.emit("重新框选...", "")
    # must run region selector on UI thread
    QTimer.singleShot(0, _do_reselect)

def _do_reselect():
    global cfg
    cfg["region"] = select_region(app)
    save_cfg(cfg)
    detector.last_text = ""
    overlay.update_signal.emit("就绪", "")
    paused.clear()

HotkeyManager(on_f8=reselect)

def worker():
    while True:
        try:
            if paused.is_set():
                time.sleep(0.2)
                continue

            overlay.update_signal.emit("OCR中...", "")
            img = capture.grab(cfg["region"])
            if img is None:
                time.sleep(1)
                continue

            txt = ocr.recognize(img)
            if len(txt.strip()) < 20:
                time.sleep(cfg["ocr_interval"])
                continue

            if detector.changed(txt):
                overlay.update_signal.emit("推理中...", txt[:500])
                ans = client.ask(txt)
                logger.log(ocr_text=txt, answer=ans)
                overlay.update_signal.emit("完成", ans)
                time.sleep(cfg["cooldown_after_answer"])

            time.sleep(cfg["ocr_interval"])

        except Exception as e:
            logger.log(error=str(e))
            overlay.update_signal.emit("异常", str(e))
            time.sleep(3)

threading.Thread(target=worker, daemon=True).start()
sys.exit(app.exec())
