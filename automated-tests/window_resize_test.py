import subprocess
import time
import pyautogui
import pytest

PCSX2_PATH = r"C:\\Program Files\\PCSX2\\pcsx2-qt.exe"
GAME_PATH = r'C:/Users/havil/Documents/PCSX2/games/Rumble Racing.bin'
BTN_SETTINGS = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_settings.png"
BTN_GRAPHICS = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_graphics.png"
BTN_ASPECT_DROPDOWN = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_aspect_dropdown.png"
BTN_SELECT_STRETCH = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_select_stretch.png"
BTN_SYSTEM = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_system.png"
BTN_START_FILE = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_start_file.png"

class TestPCSX2StretchWindow:
    def setup_method(self):
        self.process = subprocess.Popen([PCSX2_PATH])
        time.sleep(5)

    def teardown_method(self):
        if self.process:
            self.process.terminate()

    def test_ct030_stretch_window(self):
        """
        CT030: Validar ajuste fluido ao redimensionar a janela manualmente
        Passo a Passo: Configurar Stretch > Iniciar Jogo > Redimensionar Janela > Validar Preenchimento
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
            
            btn_stretch = pyautogui.locateCenterOnScreen(BTN_SELECT_STRETCH, confidence=0.8)
            if btn_stretch:
                pyautogui.click(btn_stretch)
            else:
                pyautogui.press('end') 
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

        screen_width, screen_height = pyautogui.size()
        center_x, center_y = screen_width // 2, screen_height // 2
        
        pyautogui.click(center_x, center_y) 
        time.sleep(1)

        pyautogui.keyDown('alt')
        pyautogui.press('space')
        pyautogui.keyUp('alt')
        time.sleep(0.5)
        
        pyautogui.press('s') 
        pyautogui.press('t') 
        time.sleep(0.5)

        for _ in range(20):
            pyautogui.press('right')
        
        pyautogui.press('enter')
        time.sleep(2)

        screenshot = pyautogui.screenshot()
        width, height = screenshot.size
        
        y_center = height // 2
        
        pixel_left = screenshot.getpixel((50, y_center))
        pixel_right = screenshot.getpixel((width - 50, y_center))
        
        is_left_black = sum(pixel_left) < 15
        is_right_black = sum(pixel_right) < 15

        if not is_left_black and not is_right_black:
            assert True
        else:
            pyautogui.screenshot("erro_ct030_stretch.png")
            pytest.fail(f"Falha: Bordas pretas detectadas. Esq: {pixel_left}, Dir: {pixel_right}")