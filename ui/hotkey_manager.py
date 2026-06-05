import threading
from pynput import keyboard

class HotkeyManager:
    def __init__(self, on_f8):
        self._on_f8 = on_f8
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        def on_press(key):
            if key == keyboard.Key.f8:
                self._on_f8()
            elif key == keyboard.Key.esc:
                import os; os._exit(0)

        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
