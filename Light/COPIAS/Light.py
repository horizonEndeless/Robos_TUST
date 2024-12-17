import tkinter as tk
from tkinter import ttk, messagebox
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
from multiprocessing import Pool
import math

class LightRobot:
    def __init__(self):
        # Lista RE
        self.empresas_re = [
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
        
        # Lista AE
        self.empresas_ae = [
            {"cnpj": "30.520.122/0001-70", "ons": "3859", "pasta": "SJP1"},  # SJP I
            {"cnpj": "30.432.007/0001-79", "ons": "3860", "pasta": "SJP2"},  # SJP II
            {"cnpj": "30.486.042/0001-45", "ons": "3861", "pasta": "SJP3"},  # SJP III
            {"cnpj": "30.425.445/0001-84", "ons": "3862", "pasta": "SJP4"},  # SJP IV
            {"cnpj": "30.456.405/0001-08", "ons": "3863", "pasta": "SJP5"},  # SJP V
            {"cnpj": "30.421.756/0001-75", "ons": "3864", "pasta": "SJP6"}   # SJP VI
        ]
        
        self.empresas = []  # Será preenchida após a seleção
        self.empresas_com_erro = []  # Adicionado aqui
        
    def iniciar_interface(self):
        # Criar janela
        self.root = tk.Tk()
        self.root.title("Light Robot - Seleção de Empresas")
        self.root.geometry("400x300")
        
        # Estilo
        style = ttk.Style()
        style.configure("TButton", padding=10)
        style.configure("TLabel", padding=10, font=("Arial", 12))
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True, fill="both")
        
        # Label
        ttk.Label(main_frame, text="Selecione o tipo de empresa:", style="TLabel").pack()
        
        # Botões
        ttk.Button(main_frame, text="RE - Rio energy", 
                  command=lambda: self.selecionar_tipo("RE")).pack(pady=10, padx=20, fill="x")
        
        ttk.Button(main_frame, text="AE - America Energia", 
                  command=lambda: self.selecionar_tipo("AE")).pack(pady=10, padx=20, fill="x")
        
        # Iniciar loop
        self.root.mainloop()
    
    def selecionar_tipo(self, tipo):
        if tipo == "RE":
            self.empresas = self.empresas_re
            pasta_base = "RE"
        else:
            self.empresas = self.empresas_ae
            pasta_base = "AE"
        
        # Confirmar seleção
        msg = f"Selecionado: {tipo}\nTotal de empresas: {len(self.empresas)}\nPasta: {pasta_base}"
        if messagebox.askyesno("Confirmar", f"{msg}\n\nDeseja iniciar o processamento?"):
            self.root.destroy()
            self.executar()
        
    def executar(self):
        try:
            for empresa in self.empresas:
                self.processar_empresa(empresa)
                
            # Relatório final
            print("\n=== RELATÓRIO FINAL ===")
            print(f"Total de empresas processadas: {len(self.empresas)}")
            
            if self.empresas_com_erro:
                print("\nEmpresas com erro:")
                for empresa in self.empresas_com_erro:
                    print(f"- {empresa['pasta']} (ONS: {empresa['ons']})")
            else:
                print("\nTodas as empresas foram processadas com sucesso!")
                
        except Exception as e:
            print(f"Erro na execução: {str(e)}")
        finally:
            if hasattr(self, 'driver'):
                self.driver.quit()

    def processar_empresa(self, empresa, max_tentativas=5):
        pasta_base = os.path.join(r"C:\Users\Bruno\Downloads\LIGHT", 
                                 "AE" if empresa['ons'] in [str(x) for x in range(3859, 3865)] else "RE", 
                                 empresa["pasta"])
        os.makedirs(pasta_base, exist_ok=True)
        
        tentativa = 0
        sucesso = False
        
        while tentativa < max_tentativas and not sucesso:
            try:
                print(f"\nProcessando empresa: CNPJ {empresa['cnpj']} - ONS {empresa['ons']}")
                print(f"Tentativa {tentativa + 1} de {max_tentativas}")
                
                # Calcular delay progressivo
                delay = tentativa * 3
                if delay > 0:
                    print(f"Aguardando {delay} segundos antes de tentar novamente...")
                    time.sleep(delay)
                
                # Iniciar nova sessão do navegador
                if hasattr(self, 'driver'):
                    try:
                        self.driver.quit()
                    except:
                        pass
                
                print(f"\nIniciando nova sessão do navegador (tentativa {tentativa + 1})")
                self.inicializar_driver()
                
                # Configurar pasta de download
                self.driver.get("about:config")
                self.driver.find_element(By.ID, "warningButton").click()
                self.driver.execute_script("""
                    Services.prefs.setStringPref("browser.download.dir", arguments[0]);
                    Services.prefs.setIntPref("browser.download.folderList", 2);
                    Services.prefs.setBoolPref("browser.download.useDownloadDir", true);
                """, pasta_base)
                
                # Acessar site e baixar arquivos
                self.acessar_site(empresa)
                
                # Aguardar downloads e verificar
                time.sleep(2)  # Aguardar downloads
                if self.validar_downloads(pasta_base, empresa):
                    print(f"✓ Downloads corretos para {empresa['pasta']}")
                    sucesso = True
                else:
                    print(f"✗ Downloads incorretos para {empresa['pasta']}")
                    tentativa += 1
                
            except Exception as e:
                print(f"Erro ao processar empresa {empresa['cnpj']}: {str(e)}")
                tentativa += 1
        
        if not sucesso:
            print(f"Falha após {max_tentativas} tentativas para empresa {empresa['pasta']}")
            self.empresas_com_erro.append(empresa)

    def validar_downloads(self, pasta, empresa):
        """Valida se os arquivos baixados correspondem à empresa correta"""
        try:
            arquivos = os.listdir(pasta)
            
            # Padrões esperados nos nomes dos arquivos
            padrao_xml = f"0000{empresa['ons']}"
            padrao_pdf = f"EN01_0000{empresa['ons']}"
            
            # Encontrar arquivos correspondentes
            xml_correto = None
            pdf_correto = None
            
            for arquivo in arquivos:
                if arquivo.endswith('.xml') and padrao_xml in arquivo:
                    xml_correto = arquivo
                elif arquivo.endswith('.pdf') and padrao_pdf in arquivo:
                    pdf_correto = arquivo
            
            # Validar resultado
            if xml_correto and pdf_correto:
                print(f"\nArquivos encontrados para {empresa['pasta']}:")
                print(f"  XML: {xml_correto}")
                print(f"  PDF: {pdf_correto}")
                return True
            else:
                print(f"\nFaltam arquivos para {empresa['pasta']}:")
                print(f"  XML: {'Encontrado' if xml_correto else 'Faltando'}")
                print(f"  PDF: {'Encontrado' if pdf_correto else 'Faltando'}")
                return False
                
        except Exception as e:
            print(f"Erro ao validar downloads: {str(e)}")
            return False

    @staticmethod
    def processar_grupo_empresas(empresas):
        robo = LightRobot()  # Criar nova instância para cada processo
        robo.inicializar_driver()  # Inicializar o driver
        
        try:
            for empresa in empresas:
                robo.processar_empresa(empresa)
            return robo.empresas_com_erro
        finally:
            robo.driver.quit()  # Garantir que o driver seja fechado

    def acessar_site(self, empresa):
        try:
            print("\n1. Acessando o site...")
            self.driver.get("https://nfe.light.com.br/Web/wfmAutenticar.aspx")
            wait = WebDriverWait(self.driver, 5)  # Reduzido de 10 para 5 segundos
            
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
                    time.sleep(1)  # Reduzido de 3 para 1 segundo
                    
                    print("\n9. Selecionando filtros...")
                    select_ano = wait.until(EC.presence_of_element_located((By.ID, "ddlAno")))
                    select_ano.click()
                    time.sleep(0.5)  # Reduzido para 0.5 segundos
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
                    time.sleep(1)
                    
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
            wait = WebDriverWait(self.driver, 5)  # Reduzido de 10 para 5 segundos
            
            # Encontrar todos os links de download de uma vez
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
                    time.sleep(1)  # Reduzido de 3 para 1 segundo
                    
                    # Se for XML, verificar rapidamente
                    if tipo == "XML":
                        try:
                            # Verificar mensagem de erro
                            erro_element = wait.until(
                                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Download não verificado')]")),
                                timeout=2  # Timeout reduzido
                            )
                            
                            print(f"Erro no download do XML. Tentando novamente...")
                            # Fechar mensagem de erro se houver
                            fechar_btn = self.driver.find_element(By.CLASS_NAME, "close-button")
                            if fechar_btn:
                                fechar_btn.click()
                                time.sleep(1)
                                # Tentar novamente
                                self.driver.execute_script("arguments[0].click();", download_link)
                                time.sleep(1)
                                
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

    def inicializar_driver(self):
        # Configurar opções do Firefox
        firefox_options = webdriver.FirefoxOptions()
        
        # Configurar preferências de download
        firefox_options.set_preference("browser.download.folderList", 2)
        firefox_options.set_preference("browser.download.manager.showWhenStarting", False)
        firefox_options.set_preference("browser.download.manager.focusWhenStarting", False)
        firefox_options.set_preference("browser.download.useDownloadDir", True)
        firefox_options.set_preference("browser.helperApps.alwaysAsk.force", False)
        firefox_options.set_preference("browser.download.manager.alertOnEXEOpen", False)
        firefox_options.set_preference("browser.download.manager.closeWhenDone", True)
        firefox_options.set_preference("browser.download.manager.showAlertOnComplete", False)
        firefox_options.set_preference("browser.download.manager.useWindow", False)
        
        # Inicializar o Firefox com as opções
        self.driver = webdriver.Firefox(options=firefox_options)
        self.driver.set_page_load_timeout(30)
        self.driver.implicitly_wait(5)
        
        # Inicializar OCR
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)

if __name__ == "__main__":
    robo = LightRobot()
    robo.iniciar_interface()
