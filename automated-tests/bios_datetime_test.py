import subprocess
import time
import pyautogui
import os
import signal
import pytest

PCSX2_PATH = r"C:\\Program Files\\PCSX2\\pcsx2-qt.exe"
BTN_SYSTEM = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_system.png"
BTN_START_BIOS = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_start_bios.png"
REF_SYS_CONFIG = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\ref_sys_config.png"
REF_DATE_CHECK = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\ref_date_check.png"

class TestPCSX2BiosPersistence:
    def setup_method(self):
        self.process = None

    def start_emulator(self):
        self.process = subprocess.Popen([PCSX2_PATH])
        time.sleep(5)

    def kill_emulator(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.process = None

    def teardown_method(self):
        self.kill_emulator()

    def navigate_to_date_time(self):
        print("Procurando menu System...")
        btn_system = pyautogui.locateCenterOnScreen(BTN_SYSTEM, confidence=0.8)
        if not btn_system:
            pytest.fail("Menu 'System' não encontrado.")
        pyautogui.click(btn_system)
        time.sleep(0.5)

        print("Clicando em Start BIOS...")
        btn_bios = pyautogui.locateCenterOnScreen(BTN_START_BIOS, confidence=0.8)
        if btn_bios:
            pyautogui.click(btn_bios)
        else:
            pyautogui.press('down')
            pyautogui.press('down') 
            pyautogui.press('enter')

        print("Aguardando BIOS...")
        time.sleep(15)

        print('Seta para baixo')
        pyautogui.press('down', presses=3)
        time.sleep(2)

        print('Confirma')
        pyautogui.press('k') # X
        time.sleep(2)

        if not pyautogui.locateOnScreen(REF_SYS_CONFIG, confidence=0.7, grayscale=True):
            print("Alerta: Tela de System Configuration não confirmada.")

        pyautogui.press('down')
        time.sleep(0.5)
        pyautogui.press('k') # X
        time.sleep(1)

    def test_ct027_bios_clock_persistence(self):
        """
        CT027: Ajuste do Relógio e Validação de Persistência
        Fluxo: Alterar Data -> Fechar Emulador -> Reabrir -> Validar Data
        """
        
        print(">>> INÍCIO: Abrindo emulador para alterar data...")
        self.start_emulator()
        
        self.navigate_to_date_time()

        print("Alterando ano/hora...") 
        for i in range (0, 19):
            pyautogui.press('down') # Muda o valor 2025 -> 2005
            time.sleep(0.5)

        pyautogui.press('k') # X
        time.sleep(1)
        
        pyautogui.press('i') # Triângulo
        time.sleep(1)

        print("Fechando emulador para testar persistência...")
        self.kill_emulator()
        time.sleep(2) # Espera o processo morrer totalmente

        print(">>> REINÍCIO: Abrindo emulador para validar...")
        self.start_emulator()

        self.navigate_to_date_time()

        print("Validando se a alteração persistiu...")
        time.sleep(1)
        
        data_persistiu = False
        if pyautogui.locateOnScreen(REF_DATE_CHECK, confidence=0.8, grayscale=True):
            data_persistiu = True
        
        if data_persistiu:
            print("SUCESSO: A data modificada foi encontrada após reiniciar.")
            assert True
        else:
            pyautogui.screenshot("../images/falha_persistência_CT027.png")
            # Se não tiver a imagem, o teste falha, pois não podemos garantir que salvou
            pytest.fail("A data configurada não foi mantida ou a imagem de referência não bateu.")