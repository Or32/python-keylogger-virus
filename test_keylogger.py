import unittest
import threading
import time
from PyQt6.QtWidgets import QApplication
from x import KeyloggerGUI

class TestKeyloggerGUI(unittest.TestCase):

    def test_keylogging(self):
        app = QApplication([]) # Create QApplication instance first
        gui = KeyloggerGUI()
        gui.show()

        # Wait for the GUI to open
        time.sleep(1)

        # Send some test keystrokes to the keylogger
        test_keystrokes = "This is a test keystroke sequence"
        for char in test_keystrokes:
            gui.on_press(char)
            time.sleep(0.1)

        # Wait for the keylogger to finish logging or until 15 seconds have passed
        start_time = time.time()
        while not gui.done and time.time() - start_time < 15:
            time.sleep(1)

        # Check that the keylogger finished logging before the time limit expired
        self.assertTrue(gui.done)

        # Check that the logged keystrokes were sent to the server
        response = requests.get("http://127.0.0.1:8000/predict/")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode("utf-8"))
        self.assertIn("text", data)
        self.assertIn("ip", data)
        self.assertEqual(data["text"], test_keystrokes)

        # Clean up
        gui.listener.stop()
        gui.listener.join()
        gui.timer.cancel()
        gui.close()
        app.quit()

if __name__ == '__main__':
    unittest.main()
