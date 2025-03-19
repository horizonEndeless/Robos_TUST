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
DOWNLOAD_DIR = r"C:\Users\Bruno\Downloads\TUST\FURNAS"

class FurnasPortal:
    def __init__(self, headless=False):
        """Inicializa o portal Furnas"""
        self.driver = None
        self.headless = headless
        self.logged_in = False
        self.download_dir = DOWNLOAD_DIR
    
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
            return True
        except Exception as e:
            logger.error(f"Erro ao iniciar navegador: {str(e)}")
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
        """Salva um screenshot da página atual"""
        if not self.driver:
            logger.warning("Navegador não iniciado.")
            return False
        
        try:
            if not nome_arquivo:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nome_arquivo = f"furnas_screenshot_{timestamp}.png"
            
            # Criar diretório screenshots se não existir
            screenshots_dir = os.path.join(self.download_dir, "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            
            caminho_completo = os.path.join(screenshots_dir, nome_arquivo)
            self.driver.save_screenshot(caminho_completo)
            logger.info(f"Screenshot salvo em: {caminho_completo}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao salvar screenshot: {str(e)}")
            return False
    
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
            
            # Salvar screenshot após clicar na aba
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
    
    def baixar_xmls_da_tabela(self, transmissora):
        """Baixa os XMLs das faturas na tabela atual"""
        if not self.logged_in:
            logger.warning("É necessário fazer login primeiro.")
            return False
        
        try:
            logger.info(f"Baixando XMLs da tabela para transmissora: {transmissora}")
            
            # Criar diretório específico para a transmissora
            diretorio_transmissora = os.path.join(self.download_dir, transmissora.replace(" ", "_"))
            os.makedirs(diretorio_transmissora, exist_ok=True)
            
            # Fechar popups que possam estar bloqueando
            self.fechar_popups()
            
            # Salvar screenshot da tabela
            self.salvar_screenshot(f"tabela_{transmissora.replace(' ', '_')}.png")
            
            # Procurar pelos ícones de XML na coluna "XML NF-e"
            # Método 1: Procurar por imagens na coluna XML
            icones_xml = self.driver.find_elements(By.XPATH, "//td[contains(@id, 'XML') or contains(@headers, 'XML')]//img")
            
            # Método 2: Procurar por links com ícones
            if not icones_xml:
                icones_xml = self.driver.find_elements(By.CSS_SELECTOR, "img[src*='xml'], img[alt*='XML'], img[title*='XML']")
            
            # Método 3: Procurar por qualquer elemento na coluna XML
            if not icones_xml:
                # Tentar encontrar a coluna XML
                colunas = self.driver.find_elements(By.TAG_NAME, "th")
                coluna_xml_index = -1
                
                for i, coluna in enumerate(colunas):
                    if "XML" in coluna.text:
                        coluna_xml_index = i
                        break
                
                if coluna_xml_index >= 0:
                    # Encontrar todas as células nessa coluna
                    linhas = self.driver.find_elements(By.TAG_NAME, "tr")
                    for linha in linhas[1:]:  # Pular o cabeçalho
                        celulas = linha.find_elements(By.TAG_NAME, "td")
                        if len(celulas) > coluna_xml_index:
                            elementos_clicaveis = celulas[coluna_xml_index].find_elements(By.TAG_NAME, "img")
                            elementos_clicaveis.extend(celulas[coluna_xml_index].find_elements(By.TAG_NAME, "a"))
                            elementos_clicaveis.extend(celulas[coluna_xml_index].find_elements(By.TAG_NAME, "button"))
                            
                            if elementos_clicaveis:
                                icones_xml.extend(elementos_clicaveis)
            
            # Método 4: Baseado na imagem fornecida, procurar pelos ícones específicos
            if not icones_xml:
                icones_xml = self.driver.find_elements(By.CSS_SELECTOR, ".urImgIcon, .urImgRes, .urBtnStd")
            
            if not icones_xml:
                logger.warning(f"Nenhum ícone de XML encontrado na tabela para {transmissora}.")
                return False
            
            logger.info(f"Encontrados {len(icones_xml)} possíveis ícones de XML para {transmissora}.")
            
            # Clicar em cada ícone para baixar o XML
            downloads_realizados = 0
            
            # Verificar todos os arquivos XML no diretório de downloads antes de começar
            arquivos_xml_antes = set(glob.glob(os.path.join(self.download_dir, "*.xml")))
            
            for i, icone in enumerate(icones_xml):
                try:
                    # Verificar se o elemento está visível
                    if not icone.is_displayed():
                        continue
                    
                    logger.info(f"Tentando baixar XML {i+1} para {transmissora}...")
                    
                    # Fechar popups antes de cada clique
                    self.fechar_popups()
                    
                    # Rolar até o elemento
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", icone)
                    time.sleep(1)
                    
                    # Tentar clicar diretamente
                    try:
                        icone.click()
                    except:
                        # Se falhar, tentar com JavaScript
                        logger.info("Clique direto falhou. Tentando com JavaScript...")
                        self.driver.execute_script("arguments[0].click();", icone)
                    
                    # Aguardar download ou popup
                    time.sleep(2)
                    
                    # Verificar e aceitar diálogo de permissão para downloads múltiplos
                    self.aceitar_downloads_multiplos()
                    
                    # Aguardar mais tempo para o download
                    time.sleep(3)
                    
                    # Verificar se apareceu algum popup e fechar
                    self.fechar_popups()
                    
                    # Verificar se novos arquivos foram baixados
                    arquivos_xml_depois = set(glob.glob(os.path.join(self.download_dir, "*.xml")))
                    novos_arquivos = arquivos_xml_depois - arquivos_xml_antes
                    
                    if novos_arquivos:
                        # Mover os novos arquivos para o diretório da transmissora
                        for arquivo in novos_arquivos:
                            nome_arquivo = os.path.basename(arquivo)
                            destino = os.path.join(diretorio_transmissora, nome_arquivo)
                            shutil.move(arquivo, destino)
                            logger.info(f"Arquivo {nome_arquivo} movido para {diretorio_transmissora}")
                        
                        downloads_realizados += len(novos_arquivos)
                        logger.info(f"Download {i+1} concluído com sucesso para {transmissora}.")
                        
                        # Atualizar a lista de arquivos antes para a próxima iteração
                        arquivos_xml_antes = set(glob.glob(os.path.join(self.download_dir, "*.xml")))
                    else:
                        # Verificar se o arquivo foi baixado diretamente no diretório da transmissora
                        arquivos_transmissora_antes = set(os.listdir(diretorio_transmissora))
                        time.sleep(2)  # Aguardar um pouco mais
                        arquivos_transmissora_depois = set(os.listdir(diretorio_transmissora))
                        novos_arquivos_transmissora = arquivos_transmissora_depois - arquivos_transmissora_antes
                        
                        if novos_arquivos_transmissora:
                            downloads_realizados += len(novos_arquivos_transmissora)
                            logger.info(f"Download {i+1} concluído diretamente no diretório da transmissora.")
                        else:
                            logger.warning(f"Nenhum arquivo XML detectado após o clique {i+1} para {transmissora}.")
                    
                except Exception as e:
                    logger.error(f"Erro ao baixar XML {i+1} para {transmissora}: {str(e)}")
                
                # Recarregar os elementos após cada clique para evitar erros de "stale element"
                if i < len(icones_xml) - 1:  # Não recarregar após o último item
                    try:
                        # Buscar os elementos novamente
                        icones_xml_novos = self.driver.find_elements(By.XPATH, "//td[contains(@id, 'XML') or contains(@headers, 'XML')]//img")
                        if not icones_xml_novos:
                            icones_xml_novos = self.driver.find_elements(By.CSS_SELECTOR, "img[src*='xml'], img[alt*='XML'], img[title*='XML']")
                        if not icones_xml_novos:
                            icones_xml_novos = self.driver.find_elements(By.CSS_SELECTOR, ".urImgIcon, .urImgRes, .urBtnStd")
                        
                        if icones_xml_novos and len(icones_xml_novos) > i + 1:
                            # Substituir o elemento atual por um novo para evitar stale element
                            icones_xml = icones_xml_novos
                    except:
                        # Se falhar ao recarregar, continuar com os elementos existentes
                        pass
            
            logger.info(f"Download de {downloads_realizados} XMLs concluído para {transmissora}.")
            
            # Verificar se há arquivos no diretório da transmissora
            arquivos_transmissora = os.listdir(diretorio_transmissora)
            logger.info(f"Total de arquivos no diretório {diretorio_transmissora}: {len(arquivos_transmissora)}")
            
            return downloads_realizados > 0 or len(arquivos_transmissora) > 0
            
        except Exception as e:
            logger.error(f"Erro ao baixar XMLs da tabela para {transmissora}: {str(e)}")
            return False
    
    def processar_todas_transmissoras(self):
        """Processa todas as abas de transmissoras, baixando seus XMLs"""
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
                    # Baixar os XMLs da tabela
                    self.baixar_xmls_da_tabela(transmissora)
                else:
                    logger.warning(f"Não foi possível acessar a aba da transmissora: {transmissora}")
            
            # Verificar os resultados finais
            self.verificar_resultados_downloads()
            
            logger.info("Processamento de todas as transmissoras concluído.")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao processar todas as transmissoras: {str(e)}")
            return False
    
    def verificar_resultados_downloads(self):
        """Verifica e reporta os resultados dos downloads por transmissora"""
        try:
            logger.info("Verificando resultados dos downloads...")
            
            # Lista de transmissoras
            transmissoras = [
                "Transmissão_CHESF",
                "Geração_ENOR",
                "Transmissão_ENOR",
                "Geração_E.SUL",
                "Transmissão_E.SUL",
                "Transmissão_TMT1",
                "Transmissão_VSB1"
            ]
            
            total_arquivos = 0
            
            # Verificar cada diretório de transmissora
            for transmissora in transmissoras:
                diretorio = os.path.join(self.download_dir, transmissora)
                
                if os.path.exists(diretorio):
                    arquivos = os.listdir(diretorio)
                    num_arquivos = len(arquivos)
                    total_arquivos += num_arquivos
                    
                    logger.info(f"Transmissora {transmissora}: {num_arquivos} arquivos baixados")
                    
                    # Listar os primeiros 5 arquivos como exemplo
                    if arquivos:
                        logger.info(f"Exemplos de arquivos em {transmissora}:")
                        for i, arquivo in enumerate(arquivos[:5]):
                            logger.info(f"  {i+1}. {arquivo}")
                        
                        if len(arquivos) > 5:
                            logger.info(f"  ... e mais {len(arquivos) - 5} arquivo(s)")
                else:
                    logger.warning(f"Diretório para transmissora {transmissora} não encontrado")
            
            logger.info(f"Total geral: {total_arquivos} arquivos XML baixados")
            
            # Criar um relatório de resumo
            with open(os.path.join(self.download_dir, "relatorio_downloads.txt"), "w") as f:
                f.write(f"Relatório de Downloads - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*50 + "\n\n")
                
                for transmissora in transmissoras:
                    diretorio = os.path.join(self.download_dir, transmissora)
                    
                    if os.path.exists(diretorio):
                        arquivos = os.listdir(diretorio)
                        f.write(f"Transmissora: {transmissora}\n")
                        f.write(f"Arquivos baixados: {len(arquivos)}\n")
                        
                        if arquivos:
                            f.write("Exemplos de arquivos:\n")
                            for i, arquivo in enumerate(arquivos[:5]):
                                f.write(f"  {i+1}. {arquivo}\n")
                            
                            if len(arquivos) > 5:
                                f.write(f"  ... e mais {len(arquivos) - 5} arquivo(s)\n")
                        
                        f.write("\n")
                    else:
                        f.write(f"Transmissora: {transmissora}\n")
                        f.write("Diretório não encontrado\n\n")
                
                f.write("="*50 + "\n")
                f.write(f"Total geral: {total_arquivos} arquivos XML baixados\n")
            
            logger.info(f"Relatório de downloads salvo em {os.path.join(self.download_dir, 'relatorio_downloads.txt')}")
            
        except Exception as e:
            logger.error(f"Erro ao verificar resultados dos downloads: {str(e)}")

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
