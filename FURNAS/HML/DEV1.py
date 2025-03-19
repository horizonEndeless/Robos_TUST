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

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# URL do portal
url_base = "https://portaldocliente.furnas.com.br/sap/bc/webdynpro/sap/zwda_portalclientes"
login_url = f"{url_base}?sap-client=130&sap-theme=sap_bluecrystal&login=true"

# Credenciais de login
USERNAME = "backoffice@deltaenergia.com.br"
PASSWORD = "1234backoffice"

class FurnasPortal:
    def __init__(self, headless=False):
        """Inicializa o portal Furnas"""
        self.driver = None
        self.headless = headless
        self.logged_in = False
    
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
                "download.default_directory": os.path.abspath("downloads"),
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
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
            os.makedirs("screenshots", exist_ok=True)
            
            caminho_completo = os.path.join("screenshots", nome_arquivo)
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
            
            if not abas:
                logger.warning(f"Aba da transmissora '{transmissora}' não encontrada.")
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
            return False
    
    def baixar_xmls_da_tabela(self, diretorio_destino="downloads/xmls"):
        """Baixa os XMLs das faturas na tabela atual"""
        if not self.logged_in:
            logger.warning("É necessário fazer login primeiro.")
            return False
        
        try:
            logger.info("Baixando XMLs da tabela atual...")
            
            # Criar diretório de destino se não existir
            os.makedirs(diretorio_destino, exist_ok=True)
            
            # Fechar popups que possam estar bloqueando
            self.fechar_popups()
            
            # Salvar screenshot da tabela
            self.salvar_screenshot("tabela_faturas.png")
            
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
                logger.warning("Nenhum ícone de XML encontrado na tabela.")
                return False
            
            logger.info(f"Encontrados {len(icones_xml)} possíveis ícones de XML.")
            
            # Clicar em cada ícone para baixar o XML
            downloads_realizados = 0
            for i, icone in enumerate(icones_xml):
                try:
                    # Verificar se o elemento está visível
                    if not icone.is_displayed():
                        continue
                    
                    logger.info(f"Tentando baixar XML {i+1}...")
                    
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
                    time.sleep(3)
                    
                    # Verificar se apareceu algum popup e fechar
                    self.fechar_popups()
                    
                    downloads_realizados += 1
                    logger.info(f"Download {i+1} iniciado.")
                    
                except Exception as e:
                    logger.error(f"Erro ao baixar XML {i+1}: {str(e)}")
            
            logger.info(f"Tentativa de download de {downloads_realizados} XMLs concluída.")
            return downloads_realizados > 0
            
        except Exception as e:
            logger.error(f"Erro ao baixar XMLs da tabela: {str(e)}")
            return False
    
    def processar_todas_transmissoras(self):
        """Processa todas as abas de transmissoras, baixando seus XMLs"""
        if not self.logged_in:
            logger.warning("É necessário fazer login primeiro.")
            return False
        
        try:
            # Primeiro, navegar para a seção de faturas
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
                
                # Criar diretório específico para a transmissora
                diretorio_transmissora = os.path.join("downloads", "xmls", transmissora.replace(" ", "_"))
                os.makedirs(diretorio_transmissora, exist_ok=True)
                
                # Acessar a aba da transmissora
                if self.acessar_aba_transmissora(transmissora):
                    # Baixar os XMLs da tabela
                    self.baixar_xmls_da_tabela(diretorio_transmissora)
                else:
                    logger.warning(f"Não foi possível acessar a aba da transmissora: {transmissora}")
            
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
