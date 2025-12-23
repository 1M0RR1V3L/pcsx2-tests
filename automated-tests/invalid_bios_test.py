import subprocess
import time
import pyautogui
import pytest
import os

PCSX2_PATH = r"C:\\Program Files\\PCSX2\\pcsx2-qt.exe"
EMPTY_BIOS_PATH = r"C:\\Users\\havil\\Documents\\PCSX2\\empty_bios"
BTN_SETTINGS = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_settings.png"
BTN_BIOS_TAB = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_bios_tab.png"
BTN_BROWSE = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_browse.png"
BTN_SYSTEM = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_system.png"
BTN_START_BIOS = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_start_bios.png"
REF_ERROR_BIOS = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\ref_error_bios.png"

class TestPCSX2BiosException:
    def setup_method(self):
        if not os.path.exists(EMPTY_BIOS_PATH):
            os.makedirs(EMPTY_BIOS_PATH)
        self.process = subprocess.Popen([PCSX2_PATH])
        time.sleep(5)

    def teardown_method(self):
        if self.process:
            self.process.terminate()

    def test_ct028_missing_bios_error(self):
        """
        CT028: Tentativa de inicialização sem arquivo de BIOS válido
        Passo a Passo: Configurar diretório vazio > Iniciar BIOS > Validar Mensagem de Erro
        """
        
        btn_settings = pyautogui.locateCenterOnScreen(BTN_SETTINGS, confidence=0.8)
        if btn_settings:
            pyautogui.click(btn_settings)
            time.sleep(0.5)
        else:
            pytest.fail("Botão Settings não encontrado.")

        btn_bios_tab = pyautogui.locateCenterOnScreen(BTN_BIOS_TAB, confidence=0.8)
        if btn_bios_tab:
            pyautogui.click(btn_bios_tab)
            time.sleep(0.5)
        
        btn_browse = pyautogui.locateCenterOnScreen(BTN_BROWSE, confidence=0.8)
        if btn_browse:
            pyautogui.click(btn_browse)
            time.sleep(2)
            
            pyautogui.press('f4') 
            time.sleep(0.5)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            pyautogui.press('backspace')
            pyautogui.write(EMPTY_BIOS_PATH) 
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(1)
            
            pyautogui.press('enter')
            time.sleep(1)
        
        pyautogui.press('esc')
        time.sleep(1)

        btn_system = pyautogui.locateCenterOnScreen(BTN_SYSTEM, confidence=0.8)
        if btn_system:
            pyautogui.click(btn_system)
            time.sleep(0.5)
        
        btn_start_bios = pyautogui.locateCenterOnScreen(BTN_START_BIOS, confidence=0.8)
        if btn_start_bios:
            pyautogui.click(btn_start_bios)
        else:
            pyautogui.press('down')
            pyautogui.press('down')
            pyautogui.press('enter')

        time.sleep(2)

        error_popup = pyautogui.locateOnScreen(REF_ERROR_BIOS, confidence=0.8, grayscale=True)
        
        if error_popup:
            assert True
            pyautogui.press('enter')
        else:
            pyautogui.screenshot("erro_ct028_popup_nao_encontrado.png")
            pytest.fail("Falha: A janela de erro de BIOS não foi detectada.")