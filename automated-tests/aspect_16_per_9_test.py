import subprocess
import time
import pyautogui
import pytest

PCSX2_PATH = r"C:\\Program Files\\PCSX2\\pcsx2-qt.exe"
GAME_PATH = r'C:/Users/havil/Documents/PCSX2/games/Rumble Racing.bin'
BTN_SETTINGS = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_settings.png"
BTN_GRAPHICS = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_graphics.png"
BTN_ASPECT_DROPDOWN = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_aspect_dropdown.png"
BTN_SELECT_16_9 = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_select_16_9.png"
BTN_SYSTEM = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_system.png"
BTN_START_FILE = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_start_file.png"

class TestPCSX2Widescreen:
    def setup_method(self):
        self.process = subprocess.Popen([PCSX2_PATH])
        time.sleep(5)

    def teardown_method(self):
        if self.process:
            self.process.terminate()

    def test_ct029_widescreen_fill(self):
        """
        CT029: Validar preenchimento total em monitor Widescreen
        Passo a Passo: Configurar 16:9 > Iniciar Jogo > Tela Cheia > Validar Ausência de Bordas
        """
        
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
            
            btn_16_9 = pyautogui.locateCenterOnScreen(BTN_SELECT_16_9, confidence=0.8)
            if btn_16_9:
                pyautogui.click(btn_16_9)
            else:
                pyautogui.press('down')
                pyautogui.press('down') 
                pyautogui.press('enter')
        
        pyautogui.press('esc')
        time.sleep(1)

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

        time.sleep(20)

        pyautogui.hotkey('alt', 'enter')
        time.sleep(3)

        screenshot = pyautogui.screenshot()
        width, height = screenshot.size
        
        y_center = height // 2
        
        pixel_left = screenshot.getpixel((10, y_center))
        pixel_right = screenshot.getpixel((width - 10, y_center))
        
        is_left_active = sum(pixel_left) > 20
        is_right_active = sum(pixel_right) > 20

        pyautogui.hotkey('alt', 'enter')

        if is_left_active and is_right_active:
            assert True
        else:
            pyautogui.screenshot("erro_ct029_widescreen.png")
            pytest.fail(f"Falha: Bordas pretas detectadas em modo Widescreen. Esq: {pixel_left}, Dir: {pixel_right}")