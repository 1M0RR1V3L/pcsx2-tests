import subprocess
import time
import pyautogui
import os
import signal
import pytest

PCSX2_PATH = "/home/havillon/Downloads/pcsx2-v2.4.0-linux-appimage-x64-Qt.AppImage"
ISO_PATH = "/home/havillon/Downloads/Mario Collection/Mario Collection.ISO"
REFERENCE_IMAGE = "/home/havillon/Documents/UFC/V_e_V/automatizados/reference.png"

class TestPCSX2Automation:
    def setup_method(self):
        """Setup: Clean start of the application"""
        self.process = subprocess.Popen([PCSX2_PATH, "-batch", ISO_PATH])
        time.sleep(5)

    def teardown_method(self):
        """Teardown: Close the emulator"""
        if self.process:
            os.kill(self.process.pid, signal.SIGTERM)
            self.process.wait()

    def test_game_boots_successfully(self):
        """TC01: Verify game loads to title screen"""
       
        print("Waiting for emulation to reach title screen...")
        time.sleep(15) 

        location = pyautogui.locateOnScreen(REFERENCE_IMAGE, confidence=0.8, grayscale=True)
        
        if location:
            print(f"Success! Title screen found at: {location}")
            assert True
        else:
            # Capture a screenshot of failure for debugging
            pyautogui.screenshot("failure_screenshot.png")
            pytest.fail("Title screen not found. See failure_screenshot.png")