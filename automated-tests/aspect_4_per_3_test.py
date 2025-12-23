import subprocess
import time
import pyautogui
import os
import signal
import pytest
from PIL import Image

PCSX2_PATH = r"C:\\Program Files\\PCSX2\\pcsx2-qt.exe"
GAME_PATH = r'C:/Users/havil/Documents/PCSX2/games/Rumble Racing.bin'
GAME_NAME = 'Rumble Racing.bin'

BTN_SETTINGS = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_settings.png"
BTN_GRAPHICS = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_graphics.png"
BTN_ASPECT_DROPDOWN = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_aspect_dropdown.png"
BTN_SELECT_4_3 = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_select_4_3.png"

BTN_SYSTEM = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_system.png"
BTN_START_FILE = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_start_file.png"

class TestPCSX2Pillarbox:
    def setup_method(self):
        self.process = subprocess.Popen([PCSX2_PATH])
        time.sleep(5)

    def teardown_method(self):
        if self.process:
            self.process.terminate()

    def test_ct031_pillarboxing_4_3(self):
        """
        CT031: Validar inserção de bordas pretas (Pillarbox) em monitor 16:9
        Passo a Passo: Configurar 4:3 > Iniciar Jogo > Tela Cheia > Validar Bordas
        """
        
        print("Configurando Aspect Ratio para 4:3...")
        
        btn_settings = pyautogui.locateCenterOnScreen(BTN_SETTINGS, confidence=0.8)
        if btn_settings:
            pyautogui.click(btn_settings)
            time.sleep(0.5)
        else:
            pytest.fail("Botão Settings não encontrado.")

        btn_graphics = pyautogui.locateCenterOnScreen(BTN_GRAPHICS, confidence=0.8)
        if btn_graphics:
            pyautogui.click(btn_graphics)
            time.sleep(1)
        
        btn_aspect = pyautogui.locateCenterOnScreen(BTN_ASPECT_DROPDOWN, confidence=0.8)
        if btn_aspect:
            pyautogui.click(btn_aspect)
            time.sleep(0.5)
            
            btn_4_3 = pyautogui.locateCenterOnScreen(BTN_SELECT_4_3, confidence=0.8)
            if btn_4_3:
                pyautogui.click(btn_4_3)
            else:
                pyautogui.press('home')
                pyautogui.press('enter')
        
        pyautogui.press('esc')
        time.sleep(1)

        print("Iniciando o jogo...")
        
        btn_system = pyautogui.locateCenterOnScreen(BTN_SYSTEM, confidence=0.8)
        if btn_system:
            pyautogui.click(btn_system)
        
        time.sleep(0.5)
        
        btn_start = pyautogui.locateCenterOnScreen(BTN_START_FILE, confidence=0.8)
        if btn_start:
            pyautogui.click(btn_start)
        else:
            pyautogui.press('down')
            pyautogui.press('enter')

        time.sleep(2)

        pyautogui.press('f4') 
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.press('backspace')
        pyautogui.write(GAME_PATH) 
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)
        
        pyautogui.press('enter')

        print("Aguardando carregamento do jogo (20s)...")
        time.sleep(20)

        print("Alternando para Fullscreen...")
        pyautogui.hotkey('alt', 'enter')
        time.sleep(3)
        
        print("Verificando as bordas pretas...")
        
        screenshot = pyautogui.screenshot()
        width, height = screenshot.size
        
        y_center = height // 2
        
        pixel_left = screenshot.getpixel((10, y_center))
        
        pixel_right = screenshot.getpixel((width - 10, y_center))
        
        pixel_center = screenshot.getpixel((width // 2, y_center))

        print(f"Pixel Esq: {pixel_left}, Pixel Dir: {pixel_right}, Pixel Centro: {pixel_center}")

        is_left_black = sum(pixel_left) < 15 
        is_right_black = sum(pixel_right) < 15
        is_center_active = sum(pixel_center) > 15

        
        pyautogui.hotkey('alt', 'enter')

        if is_left_black and is_right_black:
            print("SUCESSO: Bordas pretas detectadas (Aspecto 4:3 respeitado).")
            assert True
        else:
            pyautogui.screenshot("erro_ct031_pillarbox.png")
            pytest.fail(f"Falha: Bordas não são pretas. Esq: {pixel_left}, Dir: {pixel_right}")