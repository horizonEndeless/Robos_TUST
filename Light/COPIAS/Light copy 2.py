from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import cv2
import numpy as np
from paddleocr import PaddleOCR
import requests

class LightRobot:
    def __init__(self):
        # Lista de CNPJs e códigos ONS
        self.empresas = [
            {"cnpj": "33.485.728/0001-00", "ons": "4313", "pasta": "BRJA"},  # BRJA
            {"cnpj": "33.485.874/0001-35", "ons": "4314", "pasta": "BRJB"},  # BRJB
            {"cnpj": "19.233.858/0002-05", "ons": "3430", "pasta": "CECA"},  # CECA
            {"cnpj": "19.233.607/0002-60", "ons": "3431", "pasta": "CECB"},  # CECB
            {"cnpj": "19.560.109/0002-92", "ons": "3432", "pasta": "CECD"},  # CECD
            {"cnpj": "33.457.932/0001-17", "ons": "4415", "pasta": "CECD"},  # CECD
            {"cnpj": "33.471.379/0001-77", "ons": "4315", "pasta": "CECE"},  # CECE
            {"cnpj": "33.468.850/0001-77", "ons": "4316", "pasta": "CECE"},  # CECE
            {"cnpj": "19.560.032/0002-50", "ons": "3502", "pasta": "ITA1"},  # ITA1
            {"cnpj": "19.560.074/0002-91", "ons": "3497", "pasta": "ITA2"},  # ITA2
            {"cnpj": "19.560.833/0002-93", "ons": "3583", "pasta": "ITA3"},  # ITA3
            {"cnpj": "19.560.874/0002-23", "ons": "3530", "pasta": "ITA4"},  # ITA4
            {"cnpj": "19.560.968/0002-55", "ons": "3498", "pasta": "ITA5"},  # ITA5
            {"cnpj": "20.533.879/0002-25", "ons": "3531", "pasta": "ITA6"},  # ITA6
            {"cnpj": "20.533.473/0002-43", "ons": "3532", "pasta": "ITA7"},  # ITA7
            {"cnpj": "20.533.310/0002-60", "ons": "3537", "pasta": "ITA8"},  # ITA8
            {"cnpj": "20.533.377/0002-02", "ons": "3538", "pasta": "ITA9"},  # ITA9
            {"cnpj": "30.063.842/0002-34", "ons": "3947", "pasta": "SDBA"},  # SDBA
            {"cnpj": "29.527.877/0002-16", "ons": "3968", "pasta": "SDBC"},  # SDBC
            {"cnpj": "29.591.504/0002-96", "ons": "3969", "pasta": "SDBC"},  # SDBC
            {"cnpj": "30.062.725/0002-56", "ons": "3970", "pasta": "SDBD"},  # SDBD
            {"cnpj": "30.062.736/0002-36", "ons": "3976", "pasta": "SDBE"},  # SDBE
            {"cnpj": "30.062.738/0002-25", "ons": "3978", "pasta": "SDBF"}   # SDBF
        ]
        
        # Configurar opções do Firefox
        firefox_options = webdriver.FirefoxOptions()
        self.driver = webdriver.Firefox(options=firefox_options)
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)

    def processar_empresa(self, empresa):
        # Criar pasta específica para a empresa
        pasta_base = os.path.join(r"C:\Users\Bruno\Downloads\LIGHT\RE", empresa["pasta"])
        os.makedirs(pasta_base, exist_ok=True)
        
        try:
            print(f"\nProcessando empresa: CNPJ {empresa['cnpj']} - ONS {empresa['ons']}")
            
            # Configurar pasta de download
            self.driver.get("about:config")
            self.driver.find_element(By.ID, "warningButton").click()
            self.driver.execute_script("""
                Services.prefs.setStringPref("browser.download.dir", arguments[0]);
                Services.prefs.setIntPref("browser.download.folderList", 2);
                Services.prefs.setBoolPref("browser.download.useDownloadDir", true);
            """, pasta_base)
            
            # Acessar site e preencher dados
            self.acessar_site(empresa)
            
        except Exception as e:
            print(f"Erro ao processar empresa {empresa['cnpj']}: {str(e)}")

    def executar(self):
        try:
            for empresa in self.empresas:
                self.processar_empresa(empresa)
                time.sleep(5)  # Aguardar entre empresas
                
        except Exception as e:
            print(f"Erro na execução: {str(e)}")
        finally:
            input("\nPressione ENTER para fechar o navegador...")
            self.driver.quit()

    def acessar_site(self, empresa):
        try:
            print("\n1. Acessando o site...")
            self.driver.get("https://nfe.light.com.br/Web/wfmAutenticar.aspx")
            wait = WebDriverWait(self.driver, 10)
            
            print("2. Preenchendo CNPJ...")
            campo_cnpj = wait.until(EC.presence_of_element_located((By.ID, "tbxCnpj")))
            campo_cnpj.clear()
            campo_cnpj.send_keys(empresa["cnpj"])
            
            print("3. Preenchendo ONS...")
            campo_ons = wait.until(EC.presence_of_element_located((By.ID, "tbxOns")))
            campo_ons.clear()
            campo_ons.send_keys(empresa["ons"])
            
            print("\n4. Iniciando processo de captura do CAPTCHA...")
            caminho_captcha = self.capturar_captcha()
            
            if caminho_captcha:
                print("\n5. Processando imagem do CAPTCHA...")
                texto_captcha = self.processar_imagem_captcha(caminho_captcha)
                
                if texto_captcha:
                    print(f"\n6. Preenchendo campo do CAPTCHA com o texto: {texto_captcha}")
                    campo_captcha = wait.until(EC.presence_of_element_located((By.ID, "tbxCodigoCaptcha")))
                    campo_captcha.send_keys(texto_captcha)
                    
                    print("\n7. Clicando no botão Autenticar...")
                    botao_autenticar = wait.until(EC.element_to_be_clickable((By.ID, "btnAutenticar")))
                    botao_autenticar.click()
                    
                    print("\n8. Aguardando carregamento da página de faturas...")
                    # Aguardar até que a URL contenha o padrão esperado
                    wait.until(EC.url_contains("wfmBuscaNotas.aspx"))
                    time.sleep(3)  # Aguardar carregamento completo
                    
                    print("\n9. Selecionando filtros...")
                    # Selecionar ano 2024
                    select_ano = wait.until(EC.presence_of_element_located((By.ID, "ddlAno")))
                    select_ano.click()
                    opcao_2024 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "option[value='2024']")))
                    opcao_2024.click()
                    
                    # Selecionar competência (novembro)
                    select_competencia = wait.until(EC.presence_of_element_located((By.ID, "ddlCompetencia")))
                    select_competencia.click()
                    opcao_novembro = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "option[value='11']")))
                    opcao_novembro.click()
                    
                    print("\n10. Clicando no botão Buscar...")
                    botao_buscar = wait.until(EC.element_to_be_clickable((By.ID, "btnBuscar")))
                    botao_buscar.click()
                    
                    print("\n11. Aguardando resultados...")
                    time.sleep(2)
                    
                    print("\n12. Iniciando downloads...")
                    self.baixar_arquivos()
            
            print("\n13. Processo finalizado. Navegador mantido aberto para verificação.")
                    
        except Exception as e:
            print(f"\nERRO: {str(e)}")

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

    def baixar_arquivos(self):
        try:
            print("\n1. Localizando links de download...")
            wait = WebDriverWait(self.driver, 10)
            
            # Encontrar todos os links de download
            downloads = self.driver.find_elements(By.LINK_TEXT, "Download")
            
            for i, download_link in enumerate(downloads):
                # Pegar a linha da tabela
                row = download_link.find_element(By.XPATH, "./ancestor::tr")
                tipo = row.find_element(By.XPATH, ".//td[3]").text
                
                # Baixar apenas XML e BOL
                if tipo in ["XML", "BOL"]:
                    print(f"\n2. Baixando arquivo {tipo}...")
                    nome_arquivo = row.find_element(By.XPATH, ".//td[4]").text
                    print(f"Nome do arquivo: {nome_arquivo}")
                    
                    # Clicar no link usando JavaScript
                    self.driver.execute_script("arguments[0].click();", download_link)
                    
                    # Aguardar um pouco para o download iniciar
                    time.sleep(3)
                    
                    # Se for XML, verificar possíveis erros
                    if tipo == "XML":
                        try:
                            # Verificar mensagem de erro
                            erro_element = wait.until(EC.presence_of_element_located(
                                (By.XPATH, "//div[contains(text(), 'Download não verificado')]")
                            ))
                            
                            print(f"Erro no download do XML. Tentando novamente...")
                            # Fechar mensagem de erro se houver
                            fechar_btn = self.driver.find_element(By.CLASS_NAME, "close-button")
                            if fechar_btn:
                                fechar_btn.click()
                                time.sleep(1)
                                # Tentar novamente
                                self.driver.execute_script("arguments[0].click();", download_link)
                                time.sleep(3)
                                
                        except:
                            print(f"Download do {tipo} parece ter sido bem sucedido")
            
            print("\n3. Downloads concluídos!")
            
        except Exception as e:
            print(f"\nERRO ao baixar arquivos: {str(e)}")

    def verificar_download(self, nome_arquivo, tipo, max_tentativas=10):
        pasta_downloads = r"C:\Users\Bruno\Downloads\LIGHT\RE\BRJA"
        caminho_arquivo = os.path.join(pasta_downloads, nome_arquivo)
        
        tentativas = 0
        while tentativas < max_tentativas:
            if os.path.exists(caminho_arquivo):
                print(f"Arquivo {tipo} baixado com sucesso em: {caminho_arquivo}")
                return True
            time.sleep(1)
            tentativas += 1
        
        print(f"Arquivo {tipo} não encontrado após {max_tentativas} tentativas")
        return False

if __name__ == "__main__":
    robo = LightRobot()
    robo.executar()

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
                    
                    print("\n7. Clicando no botão Autenticar...")
                    botao_autenticar = wait.until(EC.element_to_be_clickable((By.ID, "btnAutenticar")))
                    botao_autenticar.click()
                    
                    print("\n8. Aguardando carregamento da página de faturas...")
                    # Aguardar até que a URL contenha o padrão esperado
                    wait.until(EC.url_contains("wfmBuscaNotas.aspx"))
                    time.sleep(3)  # Aguardar carregamento completo
                    
                    print("\n9. Selecionando filtros...")
                    # Selecionar ano 2024
                    select_ano = wait.until(EC.presence_of_element_located((By.ID, "ddlAno")))
                    select_ano.click()
                    opcao_2024 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "option[value='2024']")))
                    opcao_2024.click()
                    
                    # Selecionar competência (novembro)
                    select_competencia = wait.until(EC.presence_of_element_located((By.ID, "ddlCompetencia")))
                    select_competencia.click()
                    opcao_novembro = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "option[value='11']")))
                    opcao_novembro.click()
                    
                    print("\n10. Clicando no botão Buscar...")
                    botao_buscar = wait.until(EC.element_to_be_clickable((By.ID, "btnBuscar")))
                    botao_buscar.click()
                    
                    print("\n11. Aguardando resultados...")
                    time.sleep(2)
                    
                    print("\n12. Iniciando downloads...")
                    self.baixar_arquivos()
            
            print("\n13. Processo finalizado. Navegador mantido aberto para verificação.")
                    
        except Exception as e:
            print(f"\nERRO: {str(e)}")

    def verificar_download(self, nome_arquivo, tipo, max_tentativas=10):
        pasta_downloads = r"C:\Users\Bruno\Downloads\LIGHT\RE\BRJA"
        caminho_arquivo = os.path.join(pasta_downloads, nome_arquivo)
        
        tentativas = 0
        while tentativas < max_tentativas:
            if os.path.exists(caminho_arquivo):
                print(f"Arquivo {tipo} baixado com sucesso em: {caminho_arquivo}")
                return True
            time.sleep(1)
            tentativas += 1
        
        print(f"Arquivo {tipo} não encontrado após {max_tentativas} tentativas")
        return False

if __name__ == "__main__":
    robo = LightRobot()
    robo.acessar_site()
    input("\nPressione ENTER para fechar o navegador...")
    robo.driver.quit()
