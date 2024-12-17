from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import cv2
import numpy as np
from paddleocr import PaddleOCR

class LightRobot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        # Inicializar PaddleOCR (só faz uma vez)
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)
        
    def processar_imagem_captcha(self, caminho_imagem):
        try:
            # Ler a imagem
            image = cv2.imread(caminho_imagem)
            
            # Pré-processamento
            # Aumentar tamanho
            image = cv2.resize(image, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
            
            # Converter para escala de cinza
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Aumentar contraste
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            gray = clahe.apply(gray)
            
            # Binarização
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Salvar imagem processada
            cv2.imwrite(caminho_imagem.replace('.png', '_processada.png'), binary)
            
            # Realizar OCR
            resultado = self.ocr.ocr(binary, cls=True)
            
            if resultado:
                # Extrair texto mantendo case original
                texto = ''
                for line in resultado:
                    for word_info in line:
                        texto += word_info[1][0]  # word_info[1][0] contém o texto detectado
                
                # Limpar o texto mantendo maiúsculas e minúsculas
                texto = ''.join(c for c in texto if c.isalnum())
                print(f"Texto detectado no CAPTCHA: {texto}")
                return texto
            else:
                print("Nenhum texto detectado")
                return None
            
        except Exception as e:
            print(f"Erro ao processar CAPTCHA: {str(e)}")
            return None

    def capturar_captcha(self):
        try:
            wait = WebDriverWait(self.driver, 10)
            captcha_element = wait.until(EC.presence_of_element_located((By.ID, "imgCaptcha")))
            
            pasta_captchas = r'C:\Users\Bruno\Desktop\Workspace\Robos\Light\captchas'
            
            if not os.path.exists(pasta_captchas):
                os.makedirs(pasta_captchas)
            
            nome_arquivo = f'captcha_{time.strftime("%Y%m%d-%H%M%S")}.png'
            caminho_completo = os.path.join(pasta_captchas, nome_arquivo)
            
            # Aguardar um pouco para garantir que a imagem carregou
            time.sleep(0.5)
            
            captcha_element.screenshot(caminho_completo)
            print(f"CAPTCHA salvo em: {caminho_completo}")
            
            return caminho_completo
            
        except Exception as e:
            print(f"Erro ao capturar CAPTCHA: {str(e)}")
            return None

    def acessar_site(self):
        try:
            print("\n1. Acessando o site...")
            self.driver.get("https://nfe.light.com.br/Web/wfmAutenticar.aspx")
            wait = WebDriverWait(self.driver, 10)
            
            print("2. Preenchendo CNPJ...")
            campo_cnpj = wait.until(EC.presence_of_element_located((By.ID, "tbxCnpj")))
            campo_cnpj.send_keys("33.485.728/0001-00")
            
            print("3. Preenchendo ONS...")
            campo_ons = wait.until(EC.presence_of_element_located((By.ID, "tbxOns")))
            campo_ons.send_keys("4313")
            
            print("\n4. Iniciando processo de captura do CAPTCHA...")
            caminho_captcha = self.capturar_captcha()
            
            if caminho_captcha:
                print("\n5. Processando imagem do CAPTCHA...")
                texto_captcha = self.processar_imagem_captcha(caminho_captcha)
                
                if texto_captcha:
                    print(f"\n6. Preenchendo campo do CAPTCHA com o texto: {texto_captcha}")
                    campo_captcha = wait.until(EC.presence_of_element_located((By.ID, "tbxCodigoCaptcha")))
                    campo_captcha.send_keys(texto_captcha)
            
            print("\n7. Processo finalizado. Navegador mantido aberto para verificação.")
                    
        except Exception as e:
            print(f"\nERRO: {str(e)}")

if __name__ == "__main__":
    robo = LightRobot()
    robo.acessar_site()
    input("\nPressione ENTER para fechar o navegador...")
    robo.driver.quit()
