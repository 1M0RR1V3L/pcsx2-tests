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

    def find_and_click(self, image_name, desc, wait=1, confidence=0.7, offset_x=0, offset_y=0):
        img_path = os.path.join(IMG_DIR, image_name)

        if not os.path.exists(img_path):
            print(f"ERRO CRÍTICO: Arquivo '{image_name}' não existe.")
            return False

        print(f"Buscando: {desc}...")
        try:
            location = pyautogui.locateOnScreen(img_path, confidence=confidence)
            if location:
                # 1. Pega o centro
                x, y = pyautogui.center(location)

                # 2. Aplica offset (correção de mira)
                final_x = x + offset_x
                final_y = y + offset_y

                # 3. Move o mouse suavemente
                pyautogui.moveTo(final_x, final_y, duration=0.2)
                time.sleep(0.3)

                # 4. Clica
                pyautogui.click()

                time.sleep(wait)
                return True
            else:
                print(f"FALHA VISUAL: '{image_name}' não encontrada.")
        except Exception as e:
            print(f"Erro técnico: {e}")
        return False

    def open_controllers_menu(self):
        pyautogui.hotkey('alt', 's')
        pyautogui.press('right')
        time.sleep(1.0)

        if not self.find_and_click("controllers_option.png", "Opção Controllers", wait=2):
            print("Fallback: Navegando com teclado...")
            for _ in range(10): pyautogui.press('down')
            pyautogui.press('enter')

    def test_ct011_configure_controller_port_1(self):
        """CT011: Configuração Porta 1"""
        self.open_controllers_menu()

        if not self.find_and_click("port1_tab.png", "Aba Port 1", confidence=0.9):
            pytest.fail("Falha Crítica: Não entrou na Aba Port 1")

        if not self.find_and_click("dpad_up_btn.png", "Botão D-Pad Up", offset_y=15):
            pytest.fail("Botão D-Pad Up não encontrado")

        time.sleep(1.0)
        pyautogui.press('v')
        time.sleep(0.5)

        if not self.find_and_click("cross_btn.png", "Botão Cross", confidence=0.9, offset_y=15):
            pytest.fail("Botão Cross não encontrado")

        time.sleep(1.0)
        pyautogui.press('k')
        time.sleep(0.5)

        pyautogui.screenshot("evidencia_CT011_final.png")
        pyautogui.press('esc')

    def test_ct012_configure_controller_port_2(self):
        """CT012: Configuração Porta 2"""
        self.open_controllers_menu()


        print("Focando na Aba 1 para iniciar navegação...")
        if not self.find_and_click("port1_tab.png", "Foco Inicial na Aba 1", confidence=0.9):
            pytest.fail("Não conseguiu focar na janela (Aba 1 não encontrada)")

        print("Navegando para Aba 2 via Teclado (Down + Enter)...")
        time.sleep(0.5)
        pyautogui.press('down')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(1.5)  # Espera a aba carregar visualmente


        # Configura D-Pad Up (Player 2)
        if not self.find_and_click("dpad_up_btn.png", "D-Pad Up P2", offset_y=15):
            pytest.fail("Botão D-Pad Up (P2) não encontrado - Verifique se a aba trocou corretamente")

        time.sleep(1.0)
        pyautogui.press('8')
        time.sleep(0.5)

        pyautogui.screenshot("evidencia_CT012_sucesso.png")
        pyautogui.press('esc')

    def test_ct016_auto_mapping_keyboard(self):
        """CT016: Mapeamento Automático (Keyboard)"""
        self.open_controllers_menu()

        # 1. Garante que estamos na Aba 1 (padrão para Auto Map)
        if not self.find_and_click("port1_tab.png", "Aba Port 1", confidence=0.9):
            pytest.fail("Falha Crítica: Não entrou na Aba Port 1")

        # 2. Clica no botão 'Automatic Mapping'
        # wait=1.5 é importante para dar tempo do menu dropdown desenrolar
        if not self.find_and_click("auto_map.png", "Botão Automatic Mapping", wait=1.5):
            pytest.fail("Botão 'Automatic Mapping' não encontrado (Verifique auto_map.png)")

        # 3. Seleciona a opção 'Keyboard' na lista suspensa
        # Se ele clicar no lugar errado aqui, tente adicionar offset_y=5 ou offset_x=5
        if not self.find_and_click("keyboard.png", "Opção Keyboard na lista", confidence=0.8):
            pytest.fail("Opção 'Keyboard' não encontrada na lista (Verifique keyboard.png)")

        # 4. Pausa para verificar visualmente se os campos foram preenchidos
        print("Aguardando preenchimento automático...")
        time.sleep(2.0)

        # 5. Evidência do mapeamento automático
        pyautogui.screenshot("evidencia_CT016_automap.png")

        # Fecha
        pyautogui.press('esc')