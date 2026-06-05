from paddleocr import PaddleOCR

class OCREngine:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang="ch")

    def recognize(self, image):
        try:
            result = self.ocr.ocr(image, cls=True)
            txts = []
            if result and result[0]:
                for line in result[0]:
                    txts.append(line[1][0])
            return "\n".join(txts)
        except Exception as e:
            print(f"[OCR ERROR] {e}")
            return ""
