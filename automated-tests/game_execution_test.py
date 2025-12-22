import subprocess
import time
import pyautogui
import os
import signal
import pytest

PCSX2_PATH = r"C:\\Program Files\\PCSX2\\pcsx2-qt.exe"
ISO_PATH = r'C:/Users/havil/Documents/PCSX2/games/Mario Collection'
GAME_NAME = 'Mario Collection.ISO'
REFERENCE_IMAGE = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\reference-mario.png"
BTN_SYSTEM = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_system.png"
BTN_START_FILE = r"C:\\Users\\havil\\Documents\\pcsx2-tests\\automated-tests\\images\\btn_start_file.png"

class TestPCSX2GameExecution:
    def setup_method(self):
        self.process = subprocess.Popen([PCSX2_PATH])
        time.sleep(5)

    def teardown_method(self):
        if self.process:
            self.process.terminate()

    def test_game_boots_successfully(self):
        """
        CT001: Carregar imagem de disco .iso válida 
        Passo a Passo: System > Boot ISO > Selecionar Arquivo > Abrir 
        """
       
        print("Waiting for emulation to reach title screen...")
        time.sleep(5) 

        print("Procurando menu System...")
        btn_system = pyautogui.locateCenterOnScreen(BTN_SYSTEM, confidence=0.8)
        if not btn_system:
            pytest.fail("Menu 'System' não encontrado.")
        pyautogui.click(btn_system)
        time.sleep(0.5)

        print("Clicando em Start File...")

        btn_start = pyautogui.locateCenterOnScreen(BTN_START_FILE, confidence=0.8)
        if btn_start:
            pyautogui.click(btn_start)
        else:
            print("Botão não encontrado!!!")

        time.sleep(2)


        print(f"Digitando caminho da ISO: {ISO_PATH}")

        pyautogui.press('f4') 
        time.sleep(0.5)

        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.press('backspace')

        pyautogui.write(ISO_PATH) 
        time.sleep(1)
        pyautogui.press('enter')

        time.sleep(1)

        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')

        pyautogui.write(GAME_NAME)

        pyautogui.press('enter')

        print("Aguardando inicialização do jogo...")

        time.sleep(20)

        jogo_carregou = False
        for _ in range(10):
            if pyautogui.locateOnScreen(REFERENCE_IMAGE, confidence=0.7, grayscale=True):
                jogo_carregou = True
                break
            time.sleep(3)

        if jogo_carregou:
            print("SUCESSO: Jogo identificado na tela.")
            assert True
        else:
            pyautogui.screenshot("erro_ct001.png")
            pytest.fail("O jogo não iniciou ou a imagem de referência não foi encontrada.")