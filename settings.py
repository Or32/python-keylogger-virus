import requests  # Used for making HTTP requests
from cryptography.fernet import Fernet  # Used for encryption/decryption
import base64  # Used for encoding/decoding

class Settings:
    def __init__(self, data_collector):
        self.data_collector = data_collector
        self.window_title = "Keylogger"  # Title of the GUI window
        self.window_geometry = (100, 100, 400, 200)  # Position and size of the GUI window
        self.time_interval = 10  # Time interval for data processing or actions
        self.server_path = "ws://localhost:8000/ws"  # Path to the WebSocket server

    def get_server_path(self):
        return self.server_path  # Retrieves the server path

    def process_data(self):
        text = self.data_collector.get_data()  # Retrieves collected data for processing

    def get_window_title(self):
        return self.window_title  # Retrieves the window title

    def get_window_geometry(self):
        return self.window_geometry  # Retrieves the window geometry

    def get_time_interval(self):
        return self.time_interval  # Retrieves the time interval
