import subprocess
import time
import pyautogui
import pytest

PCSX2_PATH = r"C:\\Program Files\\PCSX2\\pcsx2-qt.exe"
BTN_SYSTEM = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_system.png"
BTN_START_BIOS = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_start_bios.png"
REF_SYS_CONFIG_EN = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\ref_sys_config_en.png"
REF_LANG_PT_CHECK = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\ref_lang_pt_check.png"

class TestPCSX2LanguageChange:
    def setup_method(self):
        self.process = subprocess.Popen([PCSX2_PATH])
        time.sleep(5)

    def teardown_method(self):
        if self.process:
            self.process.terminate()

    def test_ct026_change_language(self):
        """
        CT026: Configuração inicial de idioma e alteração via menu
        Passo a Passo: System > Start BIOS > System Configuration > Idioma > Português > Validar
        """
        
        btn_system = pyautogui.locateCenterOnScreen(BTN_SYSTEM, confidence=0.8)
        if btn_system:
            pyautogui.click(btn_system)
            time.sleep(0.5)
        else:
            pytest.fail("Menu 'System' não encontrado.")

        btn_bios = pyautogui.locateCenterOnScreen(BTN_START_BIOS, confidence=0.8)
        if btn_bios:
            pyautogui.click(btn_bios)
        else:
            pyautogui.press('down')
            pyautogui.press('down') 
            pyautogui.press('enter')

        time.sleep(20)

        pyautogui.press('down')
        time.sleep(0.5)
        pyautogui.press('k')
        time.sleep(2)

        if not pyautogui.locateOnScreen(REF_SYS_CONFIG_EN, confidence=0.7, grayscale=True):
            pass 

        for _ in range(4):
            pyautogui.press('down')
            time.sleep(0.2)
        
        pyautogui.press('k')
        time.sleep(1)

        for _ in range(6):
            pyautogui.press('right')
            time.sleep(0.2)

        pyautogui.press('k')
        time.sleep(1)

        pyautogui.press('i')
        time.sleep(2)

        if pyautogui.locateOnScreen(REF_LANG_PT_CHECK, confidence=0.8, grayscale=True):
            assert True
        else:
            pyautogui.screenshot("erro_ct026_idioma.png")
            pytest.fail("Falha: O idioma não parece ter mudado para Português (Texto de referência não encontrado).")