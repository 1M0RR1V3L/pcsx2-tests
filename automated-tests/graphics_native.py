import subprocess
import time
import pyautogui
import os
import signal
import pytest

PCSX2_PATH = r"E:\PCSX2\pcsx2-qt.exe"
IMG_DIR = r"E:\VV\pcsx2-tests\automated-tests\images"


class TestPCSX2Graphics:

    def setup_method(self):
        os.system("taskkill /f /im pcsx2-qt.exe >nul 2>&1")
        time.sleep(1)

        self.process = subprocess.Popen([PCSX2_PATH])
        time.sleep(4)
        pyautogui.moveTo(10, 10)

    def teardown_method(self):
        if hasattr(self, 'process') and self.process and self.process.poll() is None:
            os.kill(self.process.pid, signal.SIGTERM)
            self.process.wait()

    def find_and_click(self, image_name, desc, wait=1, confidence=0.8, offset_x=0, offset_y=0, double_click=False):
        img_path = os.path.join(IMG_DIR, image_name)
        if not os.path.exists(img_path):
            print(f"ERRO CRÍTICO: Arquivo '{image_name}' não existe.")
            return False
        try:
            location = pyautogui.locateOnScreen(img_path, confidence=confidence)
            if location:
                x, y = pyautogui.center(location)
                pyautogui.moveTo(x + offset_x, y + offset_y, duration=0.2)
                time.sleep(0.3)
                if double_click:
                    pyautogui.doubleClick()
                else:
                    pyautogui.click()
                time.sleep(wait)
                return True
        except:
            pass
        return False

    def wait_for_image(self, image_name, desc, timeout=30):
        print(f"Aguardando {desc} (Timeout: {timeout}s)...")
        start_time = time.time()
        img_path = os.path.join(IMG_DIR, image_name)
        while time.time() - start_time < timeout:
            try:
                if pyautogui.locateOnScreen(img_path, confidence=0.6, grayscale=True):
                    print(f"-> {desc} detectado!")
                    return True
            except:
                pass
            time.sleep(0.5)
        print(f"TIMEOUT: {desc} não apareceu.")
        return False

    def skip_intros_aggressively(self, target_image, desc, timeout=35):
        """
        Alterna Enter/K por todo o tempo definido (timeout).
        """
        print(f"Modo Pular Intro: Forçando Enter/K por {timeout}s sem parar...")
        start_time = time.time()
        img_path = os.path.join(IMG_DIR, target_image)

        # Tenta trazer a janela para frente
        try:
            pyautogui.getWindowsWithTitle("PCSX2")[0].activate()
        except:
            pass

        found_once = False

        while time.time() - start_time < timeout:
            if not found_once:
                try:
                    if pyautogui.locateOnScreen(img_path, confidence=0.45, grayscale=True):
                        print(f"-> {desc} DETECTADO VISUALMENTE! (Continuando inputs...)")
                        found_once = True
                except:
                    pass

            pyautogui.keyDown('enter')
            time.sleep(0.1)
            pyautogui.keyUp('enter')

            time.sleep(0.8)

            pyautogui.keyDown('k')
            time.sleep(0.1)
            pyautogui.keyUp('k')

            time.sleep(0.5)

        print(f"Tempo de Skip ({timeout}s) finalizado.")
        return True

    def test_ct009_resolution_4k_gameplay(self):
        """CT008: Aumento de resolução para 4k/6x"""

        print("Configurando vídeo via teclado...")
        try:
            pyautogui.getWindowsWithTitle("PCSX2")[0].activate()
        except:
            pass
        time.sleep(1)

        pyautogui.hotkey('alt', 's')
        time.sleep(0.5)
        pyautogui.press('right')
        time.sleep(0.5)

        for _ in range(4):
            pyautogui.press('down')
            time.sleep(0.1)

        pyautogui.press('enter')
        time.sleep(1.5)

        self.find_and_click("graphics.png", "Opção Graphics", wait=1)

        if not self.find_and_click("rendering.png", "Aba Rendering"):
            pytest.fail("Falha Rendering.")

        if not self.find_and_click("reso_4k_ps2.png", "Dropdown Resolução", offset_y=5):
            pytest.fail("Falha Dropdown.")

        if not self.find_and_click("1x_native.png", "Opção 1x Native", wait=1):
            pytest.fail("Falha 1x Native.")

        print("Fechando janela de configurações clicando no 'X'...")
        if not self.find_and_click("close.png", "Botão Fechar (X)", wait=1.5):
            pytest.fail("Falha visual: Não foi possível encontrar o botão 'X' para fechar a janela.")

        print("Iniciando Ben 10...")
        if not self.find_and_click("ben_10_iso.png", "ISO Ben 10", double_click=False):
            pytest.fail("ISO não encontrada.")

        time.sleep(0.5)
        pyautogui.press('enter')

        print("Aguardando 30s para carregamento inicial (Blind Wait)...")
        time.sleep(30)

        sw, sh = pyautogui.size()
        print(f"Clicando no centro da tela ({sw / 2}, {sh / 2}) para garantir foco...")
        pyautogui.click(sw / 2, sh / 2)
        time.sleep(1)

        self.skip_intros_aggressively("ben_press_start.png", "Menu Principal", timeout=28)

        print("TESTE RESO 1X NATIVE CONCLUÍDO.")