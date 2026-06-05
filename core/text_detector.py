
from difflib import SequenceMatcher

class TextDetector:
    def __init__(self, threshold=0.95):
        self.last_text = ""
        self.threshold = threshold

    def changed(self, text):
        if not self.last_text:
            self.last_text = text
            return True

        sim = SequenceMatcher(None, self.last_text, text).ratio()

        if sim < self.threshold:
            self.last_text = text
            return True

        return False
