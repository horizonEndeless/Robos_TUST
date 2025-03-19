import requests
from bs4 import BeautifulSoup
import re
import logging
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import pandas as pd
from datetime import datetime
import glob
import shutil

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# URL do portal
url_base = "https://portaldocliente.furnas.com.br/sap/bc/webdynpro/sap/zwda_portalclientes"
login_url = f"{url_base}?sap-client=130&sap-theme=sap_bluecrystal&login=true"

# Credenciais de login
USERNAME = "backoffice@deltaenergia.com.br"
PASSWORD = "1234backoffice"

# Diretório de download
DOWNLOAD_DIR = r"C:\Users\Bruno\Downloads\TUST\FURNAS\DE"

class FurnasPortal:
    def __init__(self, headless=False):
        """Inicializa o portal Furnas"""
        self.driver = None
        self.headless = headless
        self.logged_in = False
        self.download_dir = DOWNLOAD_DIR
        self.arquivos_baixados = set()  # Conjunto para rastrear arquivos já baixados
    
    def iniciar_navegador(self):
        """Inicia o navegador Chrome"""
        try:
            logger.info("Iniciando navegador Chrome...")
            
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920x1080")
            chrome_options.add_argument("--start-maximized")
            
            # Configurar pasta de download
            prefs = {
                "download.default_directory": self.download_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            # Criar diretório de download se não existir
            os.makedirs(self.download_dir, exist_ok=True)
            
            self.driver = webdriver.Chrome(options=chrome_options)
            
            # Inicializar o conjunto de arquivos já baixados
            self.carregar_arquivos_existentes()
            
            return True
        except Exception as e:
            logger.error(f"Erro ao iniciar navegador: {str(e)}")
            return False
    
    def carregar_arquivos_existentes(self):
        """Carrega todos os arquivos XML existentes para evitar downloads duplicados"""
        try:
            logger.info("Carregando lista de arquivos XML existentes...")
            
            # Verificar todos os diretórios de transmissoras
            transmissoras = [
                "Transmissão_CHESF",
                "Geração_ENOR",
                "Transmissão_ENOR",
                "Geração_E.SUL",
                "Transmissão_E.SUL",
                "Transmissão_TMT1",
                "Transmissão_VSB1"
            ]
            
            # Limpar o conjunto de arquivos baixados
            self.arquivos_baixados = set()
            
            # Verificar arquivos no diretório principal
            for arquivo in glob.glob(os.path.join(self.download_dir, "*.xml")):
                nome_arquivo = os.path.basename(arquivo)
                self.arquivos_baixados.add(nome_arquivo)
            
            # Verificar arquivos em cada diretório de transmissora
            for transmissora in transmissoras:
                diretorio = os.path.join(self.download_dir, transmissora)
                if os.path.exists(diretorio):
                    for arquivo in glob.glob(os.path.join(diretorio, "*.xml")):
                        nome_arquivo = os.path.basename(arquivo)
                        self.arquivos_baixados.add(nome_arquivo)
            
            logger.info(f"Total de {len(self.arquivos_baixados)} arquivos XML já existentes.")
            
            # Extrair números de nota fiscal dos nomes de arquivo
            numeros_nf = []
            for arquivo in self.arquivos_baixados:
                # Tentar extrair o número da NF do nome do arquivo
                match = re.search(r'(\d+)', arquivo)
                if match:
                    numeros_nf.append(match.group(1))
            
            if numeros_nf:
                logger.info(f"Exemplos de números de NF já baixados: {numeros_nf[:5]}")
            
            return True
        except Exception as e:
            logger.error(f"Erro ao carregar arquivos existentes: {str(e)}")
            return False
    
    def verificar_arquivo_ja_existe(self, nome_arquivo):
        """Verifica se um arquivo já existe com base no nome (número da NF)"""
        try:
            # Verificar se o nome exato já existe
            if nome_arquivo in self.arquivos_baixados:
                return True
            
            # Extrair o número da NF do nome do arquivo
            match_novo = re.search(r'(\d+)', nome_arquivo)
            if not match_novo:
                return False
            
            numero_nf_novo = match_novo.group(1)
            
            # Verificar se algum arquivo existente contém o mesmo número de NF
            for arquivo_existente in self.arquivos_baixados:
                match_existente = re.search(r'(\d+)', arquivo_existente)
                if match_existente and match_existente.group(1) == numero_nf_novo:
                    logger.info(f"Arquivo com NF {numero_nf_novo} já existe como {arquivo_existente}")
                    return True
            
            return False
        except Exception as e:
            logger.error(f"Erro ao verificar se arquivo já existe: {str(e)}")
            return False
    
    def aceitar_downloads_multiplos(self):
        """Aceita o diálogo de permissão para baixar múltiplos arquivos"""
        try:
            logger.info("Verificando diálogo de permissão para downloads múltiplos...")
            
            # Método 1: Procurar pelo botão "Permitir" no diálogo
            botoes_permitir = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Permitir')]")
            if not botoes_permitir:
                botoes_permitir = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Permitir')]/ancestor::button")
            
            if botoes_permitir and len(botoes_permitir) > 0:
                logger.info("Diálogo de permissão para downloads múltiplos encontrado. Clicando em 'Permitir'...")
                try:
                    botoes_permitir[0].click()
                    logger.info("Permissão para downloads múltiplos concedida.")
                    time.sleep(1)
                    return True
                except:
                    # Se falhar, tentar com JavaScript
                    logger.info("Clique direto falhou. Tentando com JavaScript...")
                    self.driver.execute_script("arguments[0].click();", botoes_permitir[0])
                    logger.info("Permissão para downloads múltiplos concedida via JavaScript.")
                    time.sleep(1)
                    return True
            
            # Método 2: Verificar se há algum diálogo de download aberto
            dialogo_download = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'download de vários arquivos')]")
            if dialogo_download:
                # Tentar encontrar o botão Permitir dentro do diálogo
                botoes = self.driver.find_elements(By.TAG_NAME, "button")
                for botao in botoes:
                    if "permitir" in botao.text.lower():
                        logger.info("Botão 'Permitir' encontrado no diálogo de download.")
                        botao.click()
                        logger.info("Permissão para downloads múltiplos concedida.")
                        time.sleep(1)
                        return True
            
            logger.info("Nenhum diálogo de permissão para downloads múltiplos encontrado.")
            return False
            
        except Exception as e:
            logger.error(f"Erro ao aceitar downloads múltiplos: {str(e)}")
            return False
    
    def realizar_login(self):
        """Realiza login no portal Furnas"""
        if not self.driver:
            if not self.iniciar_navegador():
                return False
        
        try:
            logger.info(f"Acessando URL de login: {login_url}")
            self.driver.get(login_url)
            
            # Aguardar carregamento da página
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "input"))
            )
            
            # Encontrar campos de login
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            username_field = None
            password_field = None
            
            for inp in inputs:
                input_type = inp.get_attribute("type")
                if input_type == "text" or input_type == "email":
                    username_field = inp
                elif input_type == "password":
                    password_field = inp
            
            if not username_field or not password_field:
                logger.info("Campos de login não encontrados diretamente. Tentando método alternativo...")
                
                # Clicar no elemento SAP para revelar campos de login
                sap_element = self.driver.find_element(By.ID, "sapwd_main_window_root_")
                logger.info("Clicando no elemento SAP para revelar campos de login...")
                sap_element.click()
                
                # Aguardar aparecimento dos campos
                time.sleep(3)
                
                # Procurar novamente pelos campos
                inputs = self.driver.find_elements(By.TAG_NAME, "input")
                for inp in inputs:
                    input_type = inp.get_attribute("type")
                    if input_type == "text" or input_type == "email":
                        username_field = inp
                    elif input_type == "password":
                        password_field = inp
            
            # Verificar se encontrou os campos
            if not username_field or not password_field:
                logger.error("Não foi possível encontrar os campos de login.")
                return False
            
            # Preencher credenciais
            logger.info("Preenchendo credenciais...")
            username_field.clear()
            username_field.send_keys(USERNAME)
            
            password_field.clear()
            password_field.send_keys(PASSWORD)
            
            # Enviar formulário
            logger.info("Enviando formulário de login...")
            password_field.send_keys(Keys.RETURN)
            
            # Aguardar processamento do login
            time.sleep(5)
            
            # Verificar e aceitar diálogo de permissão para downloads múltiplos
            self.aceitar_downloads_multiplos()
            
            # Verificar se o login foi bem-sucedido
            page_source = self.driver.page_source.lower()
            if "logout" in page_source or "bem-vindo" in page_source or "dashboard" in page_source:
                logger.info("Login realizado com sucesso!")
                self.logged_in = True
                return True
            else:
                logger.error("Falha no login. Verifique as credenciais ou se houve alterações no portal.")
                return False
            
        except Exception as e:
            logger.error(f"Erro durante o login: {str(e)}")
            return False
    
    def fechar_popups(self):
        """Fecha popups ou overlays que possam estar bloqueando a interação"""
        try:
            logger.info("Verificando e fechando popups...")
            
            # Método 1: Procurar pelo overlay específico que está bloqueando
            overlay = self.driver.find_elements(By.ID, "urPopupWindowBlockLayer")
            if overlay and len(overlay) > 0 and overlay[0].is_displayed():
                logger.info("Overlay de popup encontrado. Tentando fechar...")
                
                # Tentar clicar no botão de fechar do popup
                close_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".urPopWinCloseIcon, .urPwCl, [title='Fechar'], [title='Close']")
                if close_buttons:
                    for btn in close_buttons:
                        try:
                            if btn.is_displayed():
                                logger.info("Clicando no botão de fechar popup...")
                                btn.click()
                                time.sleep(1)
                                break
                        except:
                            pass
                
                # Se não conseguiu fechar com o botão, tentar com JavaScript
                if self.driver.find_elements(By.ID, "urPopupWindowBlockLayer"):
                    logger.info("Tentando remover overlay com JavaScript...")
                    self.driver.execute_script("arguments[0].remove();", overlay[0])
                    time.sleep(1)
            
            # Método 2: Tentar fechar qualquer popup visível
            popup_elements = self.driver.find_elements(By.CSS_SELECTOR, ".urPopup, .urPopWin, .sapPopup")
            for popup in popup_elements:
                if popup.is_displayed():
                    logger.info("Popup encontrado. Tentando fechar...")
                    try:
                        # Tentar encontrar o botão de fechar dentro do popup
                        close_btn = popup.find_elements(By.CSS_SELECTOR, ".urPopWinCloseIcon, .urPwCl, [title='Fechar'], [title='Close']")
                        if close_btn:
                            close_btn[0].click()
                        else:
                            # Tentar pressionar ESC para fechar
                            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                    except:
                        pass
                    time.sleep(1)
            
            # Método 3: Pressionar ESC para tentar fechar qualquer diálogo
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(1)
            
            return True
        except Exception as e:
            logger.error(f"Erro ao tentar fechar popups: {str(e)}")
            return False
    
    def navegar_para_secao(self, secao):
        """Navega para uma seção específica do portal"""
        if not self.logged_in:
            logger.warning("É necessário fazer login primeiro.")
            return False
        
        try:
            logger.info(f"Navegando para a seção: {secao}")
            
            # Fechar popups que possam estar bloqueando
            self.fechar_popups()
            
            # Procurar por links ou botões com o texto da seção
            elementos = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{secao}')]")
            
            if not elementos:
                logger.warning(f"Seção '{secao}' não encontrada.")
                return False
            
            # Tentar clicar no primeiro elemento encontrado
            try:
                elementos[0].click()
                logger.info(f"Clique na seção '{secao}' realizado.")
            except:
                # Se falhar, tentar com JavaScript
                logger.info("Clique direto falhou. Tentando com JavaScript...")
                self.driver.execute_script("arguments[0].click();", elementos[0])
                logger.info(f"Clique via JavaScript na seção '{secao}' realizado.")
            
            # Aguardar carregamento
            time.sleep(3)
            return True
            
        except Exception as e:
            logger.error(f"Erro ao navegar para a seção '{secao}': {str(e)}")
            return False
    
    def salvar_screenshot(self, nome_arquivo=None):
        """Função vazia - screenshots desativados"""
        return True
    
    def fechar(self):
        """Fecha o navegador"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Navegador fechado.")
                self.driver = None
                self.logged_in = False
            except Exception as e:
                logger.error(f"Erro ao fechar navegador: {str(e)}")
    
    def acessar_aba_transmissora(self, transmissora):
        """Acessa a aba de uma transmissora específica"""
        if not self.logged_in:
            logger.warning("É necessário fazer login primeiro.")
            return False
        
        try:
            logger.info(f"Tentando acessar aba da transmissora: {transmissora}")
            
            # Fechar popups que possam estar bloqueando
            self.fechar_popups()
            
            # Procurar pela aba da transmissora usando diferentes seletores
            # Método 1: Procurar por elementos role="tab" com o texto da transmissora
            abas = self.driver.find_elements(By.XPATH, f"//span[@role='tab'][contains(text(), '{transmissora}')]")
            
            # Método 2: Procurar por qualquer elemento com o texto da transmissora
            if not abas:
                abas = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{transmissora}')]")
            
            # Método 3: Procurar por elementos que contenham parte do texto da transmissora
            if not abas:
                # Extrair a parte principal do nome da transmissora (ex: "CHESF", "ENOR", "E.SUL")
                partes = transmissora.split()
                if len(partes) > 1:
                    parte_principal = partes[-1]  # Pegar o último elemento (CHESF, ENOR, etc.)
                    abas = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{parte_principal}')]")
            
            if not abas:
                logger.warning(f"Aba da transmissora '{transmissora}' não encontrada. Tentando localizar todas as abas disponíveis...")
                
                # Listar todas as abas disponíveis para diagnóstico
                todas_abas = self.driver.find_elements(By.XPATH, "//span[@role='tab']")
                if todas_abas:
                    logger.info(f"Abas disponíveis encontradas: {len(todas_abas)}")
                    for i, aba in enumerate(todas_abas):
                        try:
                            texto_aba = aba.text
                            logger.info(f"Aba {i+1}: '{texto_aba}'")
                            
                            # Tentar encontrar correspondência parcial
                            if any(parte in texto_aba for parte in ["CHESF", "ENOR", "E.SUL", "TMT1", "VSB1"]):
                                if transmissora.split()[-1] in texto_aba:
                                    logger.info(f"Correspondência parcial encontrada: '{texto_aba}'")
                                    abas = [aba]
                                    break
                        except:
                            logger.warning(f"Não foi possível ler o texto da aba {i+1}")
                else:
                    logger.warning("Nenhuma aba encontrada na página")
                    
                    # Tentar encontrar qualquer elemento clicável que possa ser uma aba
                    elementos_clicaveis = self.driver.find_elements(By.CSS_SELECTOR, ".urTbsLbl, .urTbsTxt, .urBtnStd")
                    if elementos_clicaveis:
                        logger.info(f"Encontrados {len(elementos_clicaveis)} possíveis elementos de aba")
                        abas = [elementos_clicaveis[0]]  # Tentar o primeiro elemento
            
            if not abas:
                # Criar diretório para a transmissora mesmo se não encontrar a aba
                diretorio_transmissora = os.path.join(self.download_dir, transmissora.replace(" ", "_"))
                os.makedirs(diretorio_transmissora, exist_ok=True)
                logger.warning(f"Aba da transmissora '{transmissora}' não encontrada, mas o diretório foi criado.")
                return False
            
            # Tentar clicar na aba
            try:
                logger.info(f"Clicando na aba: {transmissora}")
                abas[0].click()
            except:
                # Se falhar, tentar com JavaScript
                logger.info("Clique direto falhou. Tentando com JavaScript...")
                self.driver.execute_script("arguments[0].click();", abas[0])
            
            # Aguardar carregamento da tabela
            time.sleep(3)
            
            # Manter a chamada para salvar_screenshot, mas agora é uma função vazia
            self.salvar_screenshot(f"aba_{transmissora.replace(' ', '_')}.png")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao acessar aba da transmissora '{transmissora}': {str(e)}")
            # Criar diretório para a transmissora mesmo em caso de erro
            diretorio_transmissora = os.path.join(self.download_dir, transmissora.replace(" ", "_"))
            os.makedirs(diretorio_transmissora, exist_ok=True)
            return False
    
    def verificar_arquivos_baixados(self, diretorio, tempo_espera=10):
        """Verifica se novos arquivos foram baixados no diretório especificado"""
        try:
            logger.info(f"Verificando downloads no diretório: {diretorio}")
            
            # Listar arquivos antes do download
            arquivos_antes = set(os.listdir(diretorio))
            
            # Aguardar o tempo especificado para o download
            time.sleep(tempo_espera)
            
            # Listar arquivos após o download
            arquivos_depois = set(os.listdir(diretorio))
            
            # Encontrar novos arquivos
            novos_arquivos = arquivos_depois - arquivos_antes
            
            if novos_arquivos:
                logger.info(f"Novos arquivos baixados: {novos_arquivos}")
                return list(novos_arquivos)
            else:
                logger.warning("Nenhum novo arquivo detectado após o download.")
                return []
                
        except Exception as e:
            logger.error(f"Erro ao verificar arquivos baixados: {str(e)}")
            return []
    
    def baixar_xmls_da_tabela(self, transmissora):
        """Baixa os XMLs e PDFs das faturas na tabela atual"""
        if not self.logged_in:
            logger.warning("É necessário fazer login primeiro.")
            return False
        
        try:
            logger.info(f"Baixando XMLs e PDFs da tabela para transmissora: {transmissora}")
            
            # Extrair informações da tabela antes de baixar os arquivos
            informacoes = self.extrair_informacoes_tabela(transmissora)
            
            # Criar diretório específico para a transmissora
            diretorio_transmissora = os.path.join(self.download_dir, transmissora.replace(" ", "_"))
            os.makedirs(diretorio_transmissora, exist_ok=True)
            
            # Fechar popups que possam estar bloqueando
            self.fechar_popups()
            
            # Verificar todos os arquivos XML e PDF no diretório de downloads antes de começar
            arquivos_xml_antes = set(glob.glob(os.path.join(self.download_dir, "*.xml")))
            arquivos_pdf_antes = set(glob.glob(os.path.join(self.download_dir, "*.pdf")))
            
            # Contadores para estatísticas
            downloads_realizados_xml = 0
            downloads_realizados_pdf = 0
            downloads_ignorados = 0
            
            # Processar cada fatura encontrada
            for fatura in informacoes.get("faturas", []):
                try:
                    # Baixar XML se disponível
                    if fatura.get('tem_xml') and fatura.get('id_botao_xml'):
                        logger.info(f"Baixando XML para fatura {fatura.get('numero_documento', 'N/A')}")
                        
                        # Clicar no botão de XML
                        self.clicar_botao_por_id(fatura['id_botao_xml'])
                        
                        # Aguardar download - 20 segundos
                        time.sleep(20)
                        
                        # Verificar e aceitar diálogo de permissão para downloads múltiplos
                        self.aceitar_downloads_multiplos()
                        
                        # Verificar se novos arquivos foram baixados
                        arquivos_xml_depois = set(glob.glob(os.path.join(self.download_dir, "*.xml")))
                        novos_arquivos = arquivos_xml_depois - arquivos_xml_antes
                        
                        if novos_arquivos:
                            # Mover os arquivos para o diretório da transmissora
                            for arquivo in novos_arquivos:
                                nome_arquivo = os.path.basename(arquivo)
                                destino = os.path.join(diretorio_transmissora, nome_arquivo)
                                shutil.move(arquivo, destino)
                                logger.info(f"Arquivo XML {nome_arquivo} movido para {diretorio_transmissora}")
                                self.arquivos_baixados.add(nome_arquivo)
                            
                            downloads_realizados_xml += len(novos_arquivos)
                            
                            # Atualizar a lista de arquivos antes para a próxima iteração
                            arquivos_xml_antes = set(glob.glob(os.path.join(self.download_dir, "*.xml")))
                    
                    # Baixar boleto se disponível
                    if fatura.get('tem_boleto') and fatura.get('id_botao_boleto'):
                        logger.info(f"Baixando boleto para fatura {fatura.get('numero_documento', 'N/A')}")
                        
                        # Clicar no botão de boleto
                        self.clicar_botao_por_id(fatura['id_botao_boleto'])
                        
                        # Aguardar download - 20 segundos
                        time.sleep(20)
                        
                        # Verificar e aceitar diálogo de permissão para downloads múltiplos
                        self.aceitar_downloads_multiplos()
                        
                        # Verificar se novos arquivos foram baixados
                        arquivos_pdf_depois = set(glob.glob(os.path.join(self.download_dir, "*.pdf")))
                        novos_arquivos = arquivos_pdf_depois - arquivos_pdf_antes
                        
                        if novos_arquivos:
                            # Mover os arquivos para o diretório da transmissora
                            for arquivo in novos_arquivos:
                                nome_arquivo = os.path.basename(arquivo)
                                destino = os.path.join(diretorio_transmissora, nome_arquivo)
                                shutil.move(arquivo, destino)
                                logger.info(f"Arquivo PDF (boleto) {nome_arquivo} movido para {diretorio_transmissora}")
                            
                            downloads_realizados_pdf += len(novos_arquivos)
                            
                            # Atualizar a lista de arquivos antes para a próxima iteração
                            arquivos_pdf_antes = set(glob.glob(os.path.join(self.download_dir, "*.pdf")))
                    
                    # Baixar NF-e (DANFE) se disponível
                    if fatura.get('tem_nfe') and fatura.get('id_botao_nfe'):
                        logger.info(f"Baixando DANFE para fatura {fatura.get('numero_documento', 'N/A')}")
                        
                        # Clicar no botão de NF-e
                        self.clicar_botao_por_id(fatura['id_botao_nfe'])
                        
                        # Aguardar download - 20 segundos
                        time.sleep(20)
                        
                        # Verificar e aceitar diálogo de permissão para downloads múltiplos
                        self.aceitar_downloads_multiplos()
                        
                        # Verificar se novos arquivos foram baixados
                        arquivos_pdf_depois = set(glob.glob(os.path.join(self.download_dir, "*.pdf")))
                        novos_arquivos = arquivos_pdf_depois - arquivos_pdf_antes
                        
                        if novos_arquivos:
                            # Mover os arquivos para o diretório da transmissora
                            for arquivo in novos_arquivos:
                                nome_arquivo = os.path.basename(arquivo)
                                destino = os.path.join(diretorio_transmissora, nome_arquivo)
                                shutil.move(arquivo, destino)
                                logger.info(f"Arquivo PDF (DANFE) {nome_arquivo} movido para {diretorio_transmissora}")
                            
                            downloads_realizados_pdf += len(novos_arquivos)
                            
                            # Atualizar a lista de arquivos antes para a próxima iteração
                            arquivos_pdf_antes = set(glob.glob(os.path.join(self.download_dir, "*.pdf")))
                    
                    # Baixar fatura PDF se disponível
                    if fatura.get('tem_fatura') and fatura.get('id_botao_fatura'):
                        logger.info(f"Baixando fatura PDF para fatura {fatura.get('numero_documento', 'N/A')}")
                        
                        # Clicar no botão de fatura
                        self.clicar_botao_por_id(fatura['id_botao_fatura'])
                        
                        # Aguardar download - 20 segundos
                        time.sleep(20)
                        
                        # Verificar e aceitar diálogo de permissão para downloads múltiplos
                        self.aceitar_downloads_multiplos()
                        
                        # Verificar se novos arquivos foram baixados
                        arquivos_pdf_depois = set(glob.glob(os.path.join(self.download_dir, "*.pdf")))
                        novos_arquivos = arquivos_pdf_depois - arquivos_pdf_antes
                        
                        if novos_arquivos:
                            # Mover os arquivos para o diretório da transmissora
                            for arquivo in novos_arquivos:
                                nome_arquivo = os.path.basename(arquivo)
                                destino = os.path.join(diretorio_transmissora, nome_arquivo)
                                shutil.move(arquivo, destino)
                                logger.info(f"Arquivo PDF (fatura) {nome_arquivo} movido para {diretorio_transmissora}")
                            
                            downloads_realizados_pdf += len(novos_arquivos)
                            
                            # Atualizar a lista de arquivos antes para a próxima iteração
                            arquivos_pdf_antes = set(glob.glob(os.path.join(self.download_dir, "*.pdf")))
                
                except Exception as e:
                    logger.error(f"Erro ao processar downloads para fatura {fatura.get('numero_documento', 'N/A')}: {str(e)}")
            
            logger.info(f"Download concluído para {transmissora}: {downloads_realizados_xml} XMLs, {downloads_realizados_pdf} PDFs")
            
            # Verificar e garantir o salvamento correto dos arquivos
            self.verificar_e_garantir_salvamento(transmissora)
            
            return downloads_realizados_xml > 0 or downloads_realizados_pdf > 0
            
        except Exception as e:
            logger.error(f"Erro ao baixar XMLs e PDFs da tabela para {transmissora}: {str(e)}")
            return False
    
    def clicar_botao_por_id(self, botao_id):
        """Clica em um botão pelo seu ID"""
        try:
            # Tentar encontrar o elemento pelo ID
            elemento = self.driver.find_element(By.ID, botao_id)
            
            # Rolar até o elemento
            self.driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
            time.sleep(1)
            
            # Fechar popups antes de clicar
            self.fechar_popups()
            
            # Tentar clicar diretamente
            try:
                elemento.click()
                logger.info(f"Clique no botão ID={botao_id} realizado com sucesso")
            except:
                # Se falhar, tentar com JavaScript
                logger.info(f"Clique direto falhou. Tentando com JavaScript para botão ID={botao_id}")
                self.driver.execute_script("arguments[0].click();", elemento)
            
            return True
        except Exception as e:
            logger.error(f"Erro ao clicar no botão ID={botao_id}: {str(e)}")
            return False
    
    def extrair_informacoes_tabela(self, transmissora):
        """Extrai informações detalhadas da tabela de faturas para a transmissora atual"""
        try:
            logger.info(f"Extraindo informações da tabela para transmissora: {transmissora}")
            
            # Dicionário para armazenar as informações extraídas
            informacoes = {
                "transmissora": transmissora,
                "faturas": []
            }
            
            # Identificar os cabeçalhos da tabela - similar ao método GetTabColumns do código C#
            colunas_indices = self.obter_indices_colunas()
            logger.info(f"Índices de colunas encontrados: {colunas_indices}")
            
            # Encontrar todas as linhas da tabela (excluindo o cabeçalho)
            linhas = self.driver.find_elements(By.XPATH, "//tr[@sst='0']")
            
            # Extrair dados de cada linha
            for i, linha in enumerate(linhas):
                try:
                    # Obter todas as células da linha
                    celulas = linha.find_elements(By.TAG_NAME, "td")
                    
                    # Pular linhas sem células suficientes
                    if len(celulas) < 3:
                        continue
                    
                    # Criar um dicionário para a fatura atual
                    fatura = {}
                    
                    # Extrair informações específicas baseadas nos índices das colunas
                    if colunas_indices.get('vencimento') is not None and colunas_indices['vencimento'] < len(celulas):
                        fatura['vencimento'] = celulas[colunas_indices['vencimento']].text.strip()
                    
                    if colunas_indices.get('numero_documento') is not None and colunas_indices['numero_documento'] < len(celulas):
                        fatura['numero_documento'] = celulas[colunas_indices['numero_documento']].text.strip()
                    
                    if colunas_indices.get('cliente') is not None and colunas_indices['cliente'] < len(celulas):
                        fatura['cliente'] = celulas[colunas_indices['cliente']].text.strip()
                    
                    if colunas_indices.get('atribuicao') is not None and colunas_indices['atribuicao'] < len(celulas):
                        fatura['atribuicao'] = celulas[colunas_indices['atribuicao']].text.strip()
                    
                    if colunas_indices.get('data_documento') is not None and colunas_indices['data_documento'] < len(celulas):
                        fatura['data_documento'] = celulas[colunas_indices['data_documento']].text.strip()
                    
                    if colunas_indices.get('montante') is not None and colunas_indices['montante'] < len(celulas):
                        fatura['montante'] = celulas[colunas_indices['montante']].text.strip()
                    
                    if colunas_indices.get('nome') is not None and colunas_indices['nome'] < len(celulas):
                        fatura['nome'] = celulas[colunas_indices['nome']].text.strip()
                    
                    if colunas_indices.get('nota_fiscal') is not None and colunas_indices['nota_fiscal'] < len(celulas):
                        fatura['nota_fiscal'] = celulas[colunas_indices['nota_fiscal']].text.strip()
                    
                    if colunas_indices.get('codigo_ons') is not None and colunas_indices['codigo_ons'] < len(celulas):
                        fatura['codigo_ons'] = celulas[colunas_indices['codigo_ons']].text.strip()
                    
                    # Extrair IDs dos botões para download (similar ao código C#)
                    if colunas_indices.get('nfe') is not None and colunas_indices['nfe'] < len(celulas):
                        fatura['id_botao_nfe'] = self.extrair_id_botao(celulas[colunas_indices['nfe']])
                        fatura['tem_nfe'] = not "urBtnStdDsbl" in celulas[colunas_indices['nfe']].get_attribute("innerHTML")
                    
                    if colunas_indices.get('fatura') is not None and colunas_indices['fatura'] < len(celulas):
                        fatura['id_botao_fatura'] = self.extrair_id_botao(celulas[colunas_indices['fatura']])
                        fatura['tem_fatura'] = not "urBtnStdDsbl" in celulas[colunas_indices['fatura']].get_attribute("innerHTML")
                    
                    if colunas_indices.get('boleto') is not None and colunas_indices['boleto'] < len(celulas):
                        fatura['id_botao_boleto'] = self.extrair_id_botao(celulas[colunas_indices['boleto']])
                        fatura['tem_boleto'] = not "urBtnStdDsbl" in celulas[colunas_indices['boleto']].get_attribute("innerHTML")
                    
                    if colunas_indices.get('xml_nfe') is not None and colunas_indices['xml_nfe'] < len(celulas):
                        fatura['id_botao_xml'] = self.extrair_id_botao(celulas[colunas_indices['xml_nfe']])
                        fatura['tem_xml'] = not "urBtnStdDsbl" in celulas[colunas_indices['xml_nfe']].get_attribute("innerHTML")
                    
                    # Adicionar a fatura à lista apenas se tiver informações relevantes
                    if self.eh_fatura_valida(fatura):
                        informacoes["faturas"].append(fatura)
                    
                except Exception as e:
                    logger.error(f"Erro ao processar linha {i+1}: {str(e)}")
            
            # Salvar as informações em um arquivo JSON
            diretorio_transmissora = os.path.join(self.download_dir, transmissora.replace(" ", "_"))
            os.makedirs(diretorio_transmissora, exist_ok=True)
            
            arquivo_json = os.path.join(diretorio_transmissora, "informacoes_faturas.json")
            with open(arquivo_json, 'w', encoding='utf-8') as f:
                json.dump(informacoes, f, ensure_ascii=False, indent=4)
            
            logger.info(f"Informações da tabela salvas em {arquivo_json}")
            logger.info(f"Total de faturas encontradas: {len(informacoes['faturas'])}")
            
            # Criar um arquivo CSV também para facilitar a análise
            arquivo_csv = os.path.join(diretorio_transmissora, "informacoes_faturas.csv")
            
            if informacoes["faturas"]:
                # Criar DataFrame e salvar como CSV
                df = pd.DataFrame(informacoes["faturas"])
                df.to_csv(arquivo_csv, index=False, encoding='utf-8')
                logger.info(f"Informações da tabela salvas em formato CSV: {arquivo_csv}")
            
            return informacoes
            
        except Exception as e:
            logger.error(f"Erro ao extrair informações da tabela para {transmissora}: {str(e)}")
            return {"transmissora": transmissora, "faturas": [], "erro": str(e)}
    
    def obter_indices_colunas(self):
        """Obtém os índices das colunas da tabela (similar ao método GetTabColumns do código C#)"""
        indices_colunas = {}
        try:
            # Encontrar os cabeçalhos da tabela
            colunas = self.driver.find_elements(By.XPATH, "//tr[@role='rowheader']/th")
            
            for i, coluna in enumerate(colunas):
                texto_coluna = coluna.text.strip().lower()
                
                if "nf-e" == texto_coluna:
                    indices_colunas['nfe'] = i
                elif "fatura" == texto_coluna:
                    indices_colunas['fatura'] = i
                elif "boleto" == texto_coluna:
                    indices_colunas['boleto'] = i
                elif "vencimento" == texto_coluna or "data" == texto_coluna:
                    indices_colunas['vencimento'] = i
                elif "documento" in texto_coluna and "nº" in texto_coluna:
                    indices_colunas['numero_documento'] = i
                elif "cliente" == texto_coluna:
                    indices_colunas['cliente'] = i
                elif "atribuição" == texto_coluna:
                    indices_colunas['atribuicao'] = i
                elif "data documento" == texto_coluna:
                    indices_colunas['data_documento'] = i
                elif "montante" == texto_coluna:
                    indices_colunas['montante'] = i
                elif "nome" == texto_coluna:
                    indices_colunas['nome'] = i
                elif "nota fiscal" == texto_coluna:
                    indices_colunas['nota_fiscal'] = i
                elif "xml nf-e" == texto_coluna:
                    indices_colunas['xml_nfe'] = i
                elif "cod. ons" == texto_coluna:
                    indices_colunas['codigo_ons'] = i
            
            logger.info(f"Índices de colunas identificados: {indices_colunas}")
            
        except Exception as e:
            logger.error(f"Erro ao obter índices das colunas: {str(e)}")
        
        return indices_colunas
    
    def extrair_id_botao(self, celula):
        """Extrai o ID do botão de uma célula (similar ao método GetHtmlValueDadosFatura do código C#)"""
        try:
            # Procurar por elementos <a> ou <img> dentro da célula
            botoes = celula.find_elements(By.TAG_NAME, "a")
            if botoes:
                return botoes[0].get_attribute("id")
            
            # Se não encontrou botões, procurar por imagens clicáveis
            imagens = celula.find_elements(By.TAG_NAME, "img")
            if imagens:
                # Tentar obter o ID da imagem ou do elemento pai
                for img in imagens:
                    img_id = img.get_attribute("id")
                    if img_id:
                        return img_id
                    
                    # Verificar o elemento pai
                    parent = img.find_element(By.XPATH, "..")
                    parent_id = parent.get_attribute("id")
                    if parent_id:
                        return parent_id
            
            return None
        except Exception as e:
            logger.error(f"Erro ao extrair ID do botão: {str(e)}")
            return None
    
    def eh_fatura_valida(self, fatura):
        """Verifica se a fatura contém informações válidas e relevantes"""
        # Verificar se tem pelo menos um campo com valor real
        campos_importantes = ['vencimento', 'numero_documento', 'montante', 'nota_fiscal']
        for campo in campos_importantes:
            if campo in fatura and fatura[campo] and len(fatura[campo]) > 0:
                return True
        
        # Verificar se tem botões de download disponíveis
        if fatura.get('tem_xml') or fatura.get('tem_boleto') or fatura.get('tem_nfe') or fatura.get('tem_fatura'):
            return True
        
        return False
    
    def verificar_e_garantir_salvamento(self, transmissora):
        """Implementa quatro tratativas para garantir o salvamento correto dos arquivos XML"""
        try:
            logger.info(f"Verificando e garantindo o salvamento correto dos XMLs para {transmissora}...")
            
            diretorio_transmissora = os.path.join(self.download_dir, transmissora.replace(" ", "_"))
            
            # Tratativa 1: Verificar se há arquivos XML no diretório principal e mover para a pasta correta
            logger.info("Tratativa 1: Verificando XMLs no diretório principal...")
            xmls_diretorio_principal = glob.glob(os.path.join(self.download_dir, "*.xml"))
            
            if xmls_diretorio_principal:
                logger.info(f"Encontrados {len(xmls_diretorio_principal)} XMLs no diretório principal.")
                
                # Obter informações da tabela atual para identificar números de NF
                numeros_nf_tabela = self.extrair_numeros_nf_da_tabela()
                
                for xml_path in xmls_diretorio_principal:
                    nome_arquivo = os.path.basename(xml_path)
                    
                    # Verificar se o arquivo pertence à transmissora atual
                    pertence_a_transmissora = False
                    
                    # Método 1: Verificar se o nome do arquivo contém o nome da transmissora
                    if transmissora.replace(" ", "").lower() in nome_arquivo.lower():
                        pertence_a_transmissora = True
                    
                    # Método 2: Verificar se o número da NF está na tabela atual
                    if not pertence_a_transmissora and numeros_nf_tabela:
                        match = re.search(r'(\d+)', nome_arquivo)
                        if match and match.group(1) in numeros_nf_tabela:
                            pertence_a_transmissora = True
                    
                    # Método 3: Se estamos processando a transmissora atual, assumir que os XMLs são dela
                    if not pertence_a_transmissora:
                        # Verificar a data de modificação do arquivo
                        tempo_modificacao = os.path.getmtime(xml_path)
                        tempo_atual = time.time()
                        
                        # Se o arquivo foi modificado nos últimos 5 minutos, provavelmente é da transmissora atual
                        if tempo_atual - tempo_modificacao < 300:  # 5 minutos em segundos
                            pertence_a_transmissora = True
                    
                    if pertence_a_transmissora:
                        # Verificar se o arquivo já existe no diretório da transmissora
                        destino = os.path.join(diretorio_transmissora, nome_arquivo)
                        if os.path.exists(destino):
                            logger.info(f"Arquivo {nome_arquivo} já existe no diretório da transmissora. Removendo duplicata.")
                            os.remove(xml_path)
                        else:
                            # Mover o arquivo para o diretório da transmissora
                            shutil.move(xml_path, destino)
                            logger.info(f"Arquivo {nome_arquivo} movido para o diretório da transmissora.")
                            
                            # Adicionar ao conjunto de arquivos baixados
                            self.arquivos_baixados.add(nome_arquivo)
            
            # Tratativa 2: Verificar se há arquivos XML em outras pastas de transmissoras que deveriam estar nesta
            logger.info("Tratativa 2: Verificando XMLs em outras pastas de transmissoras...")
            
            # Lista de todas as transmissoras
            todas_transmissoras = [
                "Transmissão_CHESF",
                "Geração_ENOR",
                "Transmissão_ENOR",
                "Geração_E.SUL",
                "Transmissão_E.SUL",
                "Transmissão_TMT1",
                "Transmissão_VSB1"
            ]
            
            # Obter números de NF da tabela atual
            numeros_nf_tabela = self.extrair_numeros_nf_da_tabela() if not numeros_nf_tabela else numeros_nf_tabela
            
            # Verificar cada diretório de transmissora (exceto o atual)
            for outra_transmissora in todas_transmissoras:
                if outra_transmissora == transmissora.replace(" ", "_"):
                    continue
                
                diretorio_outra = os.path.join(self.download_dir, outra_transmissora)
                if not os.path.exists(diretorio_outra):
                    continue
                
                xmls_outra_transmissora = glob.glob(os.path.join(diretorio_outra, "*.xml"))
                
                for xml_path in xmls_outra_transmissora:
                    nome_arquivo = os.path.basename(xml_path)
                    
                    # Verificar se o arquivo pertence à transmissora atual
                    pertence_a_transmissora = False
                    
                    # Método 1: Verificar se o nome do arquivo contém o nome da transmissora atual
                    if transmissora.replace(" ", "").lower() in nome_arquivo.lower():
                        pertence_a_transmissora = True
                    
                    # Método 2: Verificar se o número da NF está na tabela atual
                    if not pertence_a_transmissora and numeros_nf_tabela:
                        match = re.search(r'(\d+)', nome_arquivo)
                        if match and match.group(1) in numeros_nf_tabela:
                            pertence_a_transmissora = True
                    
                    if pertence_a_transmissora:
                        # Verificar se o arquivo já existe no diretório da transmissora atual
                        destino = os.path.join(diretorio_transmissora, nome_arquivo)
                        if not os.path.exists(destino):
                            # Copiar o arquivo para o diretório da transmissora atual
                            shutil.copy2(xml_path, destino)
                            logger.info(f"Arquivo {nome_arquivo} copiado de {outra_transmissora} para {transmissora.replace(' ', '_')}.")
                            
                            # Adicionar ao conjunto de arquivos baixados
                            self.arquivos_baixados.add(nome_arquivo)
            
            # Tratativa 3: Verificar se há arquivos XML com nomes incorretos ou incompletos
            logger.info("Tratativa 3: Verificando XMLs com nomes incorretos ou incompletos...")
            
            # Verificar arquivos no diretório da transmissora
            xmls_transmissora = glob.glob(os.path.join(diretorio_transmissora, "*.xml"))
            
            for xml_path in xmls_transmissora:
                nome_arquivo = os.path.basename(xml_path)
                
                # Verificar se o nome do arquivo segue o padrão esperado (contém números)
                if not re.search(r'\d+', nome_arquivo):
                    logger.warning(f"Arquivo {nome_arquivo} não segue o padrão esperado (sem números).")
                    
                    # Tentar extrair o número da NF do conteúdo do arquivo
                    try:
                        with open(xml_path, 'r', encoding='utf-8', errors='ignore') as f:
                            conteudo = f.read()
                            
                            # Procurar por padrões de número de NF no conteúdo
                            match_nf = re.search(r'<nNF>(\d+)</nNF>', conteudo)
                            if match_nf:
                                numero_nf = match_nf.group(1)
                                novo_nome = f"NF_{numero_nf}.xml"
                                novo_path = os.path.join(diretorio_transmissora, novo_nome)
                                
                                # Renomear o arquivo
                                if not os.path.exists(novo_path):
                                    os.rename(xml_path, novo_path)
                                    logger.info(f"Arquivo {nome_arquivo} renomeado para {novo_nome}.")
                                    
                                    # Atualizar no conjunto de arquivos baixados
                                    if nome_arquivo in self.arquivos_baixados:
                                        self.arquivos_baixados.remove(nome_arquivo)
                                    self.arquivos_baixados.add(novo_nome)
                    except Exception as e:
                        logger.error(f"Erro ao tentar corrigir o nome do arquivo {nome_arquivo}: {str(e)}")
            
            # Tratativa 4: Verificar a integridade dos arquivos XML
            logger.info("Tratativa 4: Verificando a integridade dos arquivos XML...")
            
            # Atualizar a lista de XMLs após as modificações anteriores
            xmls_transmissora = glob.glob(os.path.join(diretorio_transmissora, "*.xml"))
            
            arquivos_corrompidos = []
            
            for xml_path in xmls_transmissora:
                nome_arquivo = os.path.basename(xml_path)
                
                # Verificar se o arquivo é um XML válido
                try:
                    with open(xml_path, 'r', encoding='utf-8', errors='ignore') as f:
                        conteudo = f.read()
                        
                        # Verificar se o conteúdo parece ser um XML válido
                        if not ('<' in conteudo and '>' in conteudo):
                            logger.warning(f"Arquivo {nome_arquivo} não parece ser um XML válido.")
                            arquivos_corrompidos.append(xml_path)
                            continue
                        
                        # Verificar se o arquivo contém as tags esperadas de uma NF-e
                        if not ('<nNF>' in conteudo or '<NFe>' in conteudo or '<infNFe>' in conteudo):
                            logger.warning(f"Arquivo {nome_arquivo} não contém as tags esperadas de uma NF-e.")
                            arquivos_corrompidos.append(xml_path)
                except Exception as e:
                    logger.error(f"Erro ao verificar a integridade do arquivo {nome_arquivo}: {str(e)}")
                    arquivos_corrompidos.append(xml_path)
            
            # Mover arquivos corrompidos para uma pasta de problemas
            if arquivos_corrompidos:
                diretorio_problemas = os.path.join(self.download_dir, "problemas")
                os.makedirs(diretorio_problemas, exist_ok=True)
                
                for arquivo_corrompido in arquivos_corrompidos:
                    nome_arquivo = os.path.basename(arquivo_corrompido)
                    destino = os.path.join(diretorio_problemas, nome_arquivo)
                    
                    # Adicionar timestamp para evitar sobrescrever
                    if os.path.exists(destino):
                        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                        nome_base, extensao = os.path.splitext(nome_arquivo)
                        destino = os.path.join(diretorio_problemas, f"{nome_base}_{timestamp}{extensao}")
                    
                    # Mover o arquivo
                    shutil.move(arquivo_corrompido, destino)
                    logger.warning(f"Arquivo corrompido {nome_arquivo} movido para a pasta de problemas.")
                    
                    # Remover do conjunto de arquivos baixados
                    if nome_arquivo in self.arquivos_baixados:
                        self.arquivos_baixados.remove(nome_arquivo)
            
            # Contar arquivos válidos após todas as verificações
            xmls_validos = glob.glob(os.path.join(diretorio_transmissora, "*.xml"))
            logger.info(f"Total de {len(xmls_validos)} arquivos XML válidos para {transmissora}.")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao verificar e garantir o salvamento dos XMLs para {transmissora}: {str(e)}")
            return False

    def processar_todas_transmissoras(self):
        """Processa todas as abas de transmissoras, baixando seus XMLs e PDFs"""
        if not self.logged_in:
            logger.warning("É necessário fazer login primeiro.")
            return False
        
        try:
            # Primeiro, navegar para a seção de faturas (sem clicar em Faturas Compensadas)
            logger.info("Navegando para a seção de faturas...")
            if not self.navegar_para_secao("Faturas"):
                logger.error("Não foi possível acessar a seção de faturas.")
                return False
            
            # Salvar screenshot da página de faturas
            self.salvar_screenshot("pagina_faturas_inicial.png")
            
            # Lista de transmissoras baseada na imagem fornecida
            transmissoras = [
                "Transmissão CHESF",
                "Geração ENOR",
                "Transmissão ENOR",
                "Geração E.SUL",
                "Transmissão E.SUL",
                "Transmissão TMT1",
                "Transmissão VSB1"
            ]
            
            # Processar cada transmissora
            for transmissora in transmissoras:
                logger.info(f"Processando transmissora: {transmissora}")
                
                # Criar diretório para a transmissora independentemente de encontrar a aba
                diretorio_transmissora = os.path.join(self.download_dir, transmissora.replace(" ", "_"))
                os.makedirs(diretorio_transmissora, exist_ok=True)
                
                # Acessar a aba da transmissora
                if self.acessar_aba_transmissora(transmissora):
                    # Baixar os XMLs e PDFs da tabela
                    self.baixar_xmls_da_tabela(transmissora)
                else:
                    logger.warning(f"Não foi possível acessar a aba da transmissora: {transmissora}")
            
            # Verificação final para garantir que todos os arquivos estão nas pastas corretas
            logger.info("Realizando verificação final de todos os arquivos...")
            for transmissora in transmissoras:
                self.verificar_e_garantir_salvamento(transmissora)
            
            # Verificar os resultados finais
            self.verificar_resultados_downloads()
            
            logger.info("Processamento de todas as transmissoras concluído.")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao processar todas as transmissoras: {str(e)}")
            return False

def main():
    """Função principal para demonstração"""
    logger.info("Iniciando automação do Portal Furnas...")
    
    # Criar instância do portal (True para modo headless, False para ver o navegador)
    portal = FurnasPortal(headless=False)
    
    try:
        # Realizar login
        if not portal.realizar_login():
            logger.error("Não foi possível realizar o login. Encerrando.")
            portal.fechar()
            return
        
        # Salvar screenshot da página após login
        portal.salvar_screenshot("apos_login.png")
        
        # Processar todas as transmissoras
        portal.processar_todas_transmissoras()
        
        logger.info("Automação concluída com sucesso!")
        
    finally:
        # Garantir que o navegador seja fechado mesmo em caso de erro
        portal.fechar()

if __name__ == "__main__":
    main()
