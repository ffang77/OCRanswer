import os
import datetime

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")

def log(ocr_text="", answer="", error=""):
    os.makedirs(LOG_DIR, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fname = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
    with open(os.path.join(LOG_DIR, fname), "a", encoding="utf-8") as f:
        f.write(f"\n{ts}\n")
        if ocr_text:
            f.write(f"OCR:\n{ocr_text}\n")
        if answer:
            f.write(f"ANSWER:\n{answer}\n")
        if error:
            f.write(f"ERROR:\n{error}\n")
        f.write("-" * 40 + "\n")
