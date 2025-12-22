import subprocess
import time
import pyautogui
import os
import signal
import pytest

PCSX2_PATH = r"E:\PCSX2\pcsx2-qt.exe"
IMG_DIR = r"E:\VV\pcsx2-tests\automated-tests\images"


class TestPCSX2Controllers:
    def setup_method(self):
        self.process = subprocess.Popen([PCSX2_PATH])
        time.sleep(5)
        pyautogui.moveTo(10, 10)

    def teardown_method(self):
        if hasattr(self, 'process') and self.process:
            os.kill(self.process.pid, signal.SIGTERM)
            self.process.wait()

    def find_and_click(self, image_name, desc, wait=1):
        img_path = os.path.join(IMG_DIR, image_name)
        print(f"Buscando: {desc}...")
        try:
            location = pyautogui.locateOnScreen(img_path, confidence=0.7)
            if location:
                pyautogui.click(location)
                time.sleep(wait)
                return True
        except Exception as e:
            print(f"Erro ao localizar {desc}: {e}")
        return False

    def open_controllers_menu(self):
        """
        Abre o menu Settings e clica EXPLICITAMENTE na opção Controllers.
        Isso impede que ele abra a interface geral por engano.
        """
        pyautogui.hotkey('alt', 's')
        pyautogui.press('right')
        time.sleep(1.0)

        achou = self.find_and_click("controllers_option.png", "Opção Controllers na lista", wait=2)

        if not achou:
            print("DEBUG: Imagem não encontrada, tentando descer no menu...")
            pyautogui.press('down')
            pyautogui.press('down')
            pyautogui.press('down')
            pyautogui.press('down')
            pyautogui.press('down')
            pyautogui.press('down')
            pyautogui.press('down')
            pyautogui.press('down')
            pyautogui.press('down')
            pyautogui.press('down')
            pyautogui.press('enter')
    def test_ct011_configure_controller_port_1(self):
        """CT011: Configuração via Teclado (Porta 1)"""

        self.open_controllers_menu()

        assert self.find_and_click("port1_tab.png", "Aba Port 1"), "Aba Port 1 não encontrada"

        if self.find_and_click("dpad_up_anchor.png", "Botão D-Pad Up"):
            pyautogui.press('up')  # Tecla física
            time.sleep(0.5)

        if self.find_and_click("cross_anchor.png", "Botão Cross"):
            pyautogui.press('k')  # Tecla física
            time.sleep(0.5)

        pyautogui.screenshot("evidencia_CT011_final.png")

        pyautogui.press('esc')

    def test_ct012_configure_controller_port_2(self):
        """CT012: Configuração via Teclado (Porta 2)"""

        self.open_controllers_menu()

        assert self.find_and_click("port2_tab.png", "Aba Port 2"), "Aba Port 2 não encontrada"

        if self.find_and_click("dpad_up_anchor.png", "D-Pad Up P2"):
            pyautogui.press('num8')
            time.sleep(0.5)

        pyautogui.screenshot("evidencia_CT012_sucesso.png")

        pyautogui.press('esc')