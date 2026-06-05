
import dxcam

class ScreenCapture:
    def __init__(self):
        self.camera = dxcam.create()

    def grab(self, region):
        l,t,w,h = region["left"],region["top"],region["width"],region["height"]
        return self.camera.grab(region=(l,t,l+w,t+h))
