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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os
import base64

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# URL do portal
url_base = "https://portaldocliente.furnas.com.br/sap/bc/webdynpro/sap/zwda_portalclientes"
params = {
    "sap-client": "130",
    "sap-theme": "sap_bluecrystal"
}

# Credenciais de login
USERNAME = "backoffice@deltaenergia.com.br"
PASSWORD = "1234backoffice"

def login_interativo():
    """Tenta realizar login de forma interativa, explorando a página"""
    try:
        logger.info("Iniciando tentativa de login interativo...")
        
        # Criar diretório para salvar capturas de tela
        os.makedirs("furnas_screenshots", exist_ok=True)
        
        # Configurar o Selenium para navegação interativa
        chrome_options = Options()
        # Comentar a linha abaixo para ver o navegador em ação
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--start-maximized")
        
        # Iniciar o navegador
        logger.info("Iniciando navegador para login interativo...")
        driver = webdriver.Chrome(options=chrome_options)
        
        # Acessar a página
        full_url = f"{url_base}?sap-client=130&sap-theme=sap_bluecrystal"
        logger.info(f"Acessando URL: {full_url}")
        driver.get(full_url)
        
        # Aguardar carregamento da página
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Capturar screenshot da página inicial
        driver.save_screenshot("furnas_screenshots/01_pagina_inicial.png")
        logger.info("Screenshot da página inicial salvo")
        
        # Explorar a página para encontrar elementos clicáveis
        logger.info("Explorando elementos clicáveis na página...")
        
        # Método 1: Procurar por links ou botões que possam levar à página de login
        clickable_elements = []
        
        # Procurar por links
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            try:
                text = link.text.strip()
                href = link.get_attribute("href")
                if text and (
                    "login" in text.lower() or 
                    "entrar" in text.lower() or 
                    "acessar" in text.lower() or 
                    "acesso" in text.lower()
                ):
                    logger.info(f"Link de possível login encontrado: '{text}', href: {href}")
                    clickable_elements.append((link, f"Link: {text}"))
            except:
                pass
        
        # Procurar por botões
        buttons = driver.find_elements(By.TAG_NAME, "button")
        buttons.extend(driver.find_elements(By.CSS_SELECTOR, "[role='button']"))
        buttons.extend(driver.find_elements(By.CSS_SELECTOR, ".button, .btn"))
        
        for button in buttons:
            try:
                text = button.text.strip()
                if text and (
                    "login" in text.lower() or 
                    "entrar" in text.lower() or 
                    "acessar" in text.lower() or 
                    "acesso" in text.lower()
                ):
                    logger.info(f"Botão de possível login encontrado: '{text}'")
                    clickable_elements.append((button, f"Botão: {text}"))
            except:
                pass
        
        # Procurar por elementos com ID ou classe que sugerem login
        login_elements = driver.find_elements(By.CSS_SELECTOR, "[id*='login'], [id*='Login'], [class*='login'], [class*='Login']")
        for elem in login_elements:
            try:
                text = elem.text.strip()
                tag = elem.tag_name
                logger.info(f"Elemento relacionado a login encontrado: Tag: {tag}, Texto: '{text}'")
                clickable_elements.append((elem, f"Elemento login: {tag}"))
            except:
                pass
        
        # Método 2: Procurar por elementos SAP específicos
        sap_elements = driver.find_elements(By.CSS_SELECTOR, "[id*='sap'], [class*='sap']")
        for elem in sap_elements:
            try:
                if elem.is_displayed() and elem.is_enabled():
                    tag = elem.tag_name
                    id_attr = elem.get_attribute("id")
                    class_attr = elem.get_attribute("class")
                    logger.info(f"Elemento SAP encontrado: Tag: {tag}, ID: {id_attr}, Class: {class_attr}")
                    clickable_elements.append((elem, f"Elemento SAP: {tag}"))
            except:
                pass
        
        # Método 3: Procurar por elementos com texto que sugere interação
        text_elements = driver.find_elements(By.XPATH, "//*[text()='Login' or text()='Entrar' or text()='Acessar' or text()='Acesso']")
        for elem in text_elements:
            try:
                if elem.is_displayed():
                    tag = elem.tag_name
                    text = elem.text
                    logger.info(f"Elemento com texto de login encontrado: Tag: {tag}, Texto: '{text}'")
                    clickable_elements.append((elem, f"Texto: {text}"))
            except:
                pass
        
        # Tentar interagir com os elementos encontrados
        if clickable_elements:
            logger.info(f"Encontrados {len(clickable_elements)} elementos para interação")
            
            for i, (element, desc) in enumerate(clickable_elements):
                try:
                    logger.info(f"Tentando interagir com elemento {i+1}: {desc}")
                    
                    # Rolar até o elemento
                    driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    time.sleep(1)
                    
                    # Capturar screenshot antes de clicar
                    driver.save_screenshot(f"furnas_screenshots/02_antes_clique_{i+1}.png")
                    
                    # Clicar no elemento
                    element.click()
                    logger.info(f"Clique realizado no elemento {i+1}")
                    
                    # Aguardar possível carregamento
                    time.sleep(3)
                    
                    # Capturar screenshot após o clique
                    driver.save_screenshot(f"furnas_screenshots/03_apos_clique_{i+1}.png")
                    
                    # Verificar se apareceram campos de login
                    inputs = driver.find_elements(By.TAG_NAME, "input")
                    username_field = None
                    password_field = None
                    
                    for inp in inputs:
                        input_type = inp.get_attribute("type")
                        if input_type == "text" or input_type == "email":
                            username_field = inp
                        elif input_type == "password":
                            password_field = inp
                    
                    if username_field and password_field:
                        logger.info("Campos de login encontrados após interação!")
                        
                        # Tentar realizar login
                        username_field.clear()
                        username_field.send_keys(USERNAME)
                        logger.info("Usuário inserido")
                        
                        password_field.clear()
                        password_field.send_keys(PASSWORD)
                        logger.info("Senha inserida")
                        
                        # Capturar screenshot com credenciais preenchidas
                        driver.save_screenshot("furnas_screenshots/04_credenciais_preenchidas.png")
                        
                        # Procurar botão de login
                        login_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Login') or contains(text(), 'Entrar') or contains(text(), 'Acessar')]")
                        if login_buttons:
                            login_buttons[0].click()
                            logger.info("Botão de login clicado")
                        else:
                            # Tentar enviar o formulário com Enter
                            password_field.send_keys(Keys.RETURN)
                            logger.info("Tecla Enter pressionada para enviar formulário")
                        
                        # Aguardar processamento do login
                        time.sleep(5)
                        
                        # Capturar screenshot após tentativa de login
                        driver.save_screenshot("furnas_screenshots/05_apos_login.png")
                        
                        # Verificar se o login foi bem-sucedido
                        page_source = driver.page_source.lower()
                        if "logout" in page_source or "bem-vindo" in page_source or "dashboard" in page_source:
                            logger.info("Login realizado com sucesso!")
                            
                            # Salvar cookies da sessão autenticada
                            cookies = driver.get_cookies()
                            with open("furnas_screenshots/cookies_autenticados.json", "w", encoding="utf-8") as f:
                                json.dump(cookies, f, indent=4)
                            logger.info("Cookies da sessão autenticada salvos")
                            
                            # Salvar HTML da página autenticada
                            with open("furnas_screenshots/pagina_autenticada.html", "w", encoding="utf-8") as f:
                                f.write(driver.page_source)
                            logger.info("HTML da página autenticada salvo")
                            
                            break
                        else:
                            logger.warning("Login pode ter falhado. Continuando exploração...")
                            driver.back()
                            time.sleep(2)
                    else:
                        logger.info("Campos de login não encontrados após interação. Voltando...")
                        driver.back()
                        time.sleep(2)
                
                except Exception as e:
                    logger.error(f"Erro ao interagir com elemento {i+1}: {str(e)}")
                    try:
                        driver.back()
                        time.sleep(2)
                    except:
                        pass
        else:
            logger.warning("Nenhum elemento clicável relacionado a login encontrado")
        
        # Método 4: Tentar injetar JavaScript para encontrar campos ocultos
        logger.info("Tentando injetar JavaScript para encontrar campos ocultos...")
        
        # Capturar screenshot antes da injeção
        driver.save_screenshot("furnas_screenshots/06_antes_injecao_js.png")
        
        # Injetar JavaScript para tentar revelar campos ocultos
        js_script = """
        // Tentar encontrar campos de login ocultos
        var inputs = document.querySelectorAll('input');
        var loginFields = [];
        
        for (var i = 0; i < inputs.length; i++) {
            var input = inputs[i];
            // Tentar tornar visível
            if (input.type === 'hidden') {
                if (input.id.toLowerCase().includes('user') || 
                    input.id.toLowerCase().includes('login') || 
                    input.id.toLowerCase().includes('email')) {
                    input.type = 'text';
                    loginFields.push(input);
                }
                if (input.id.toLowerCase().includes('pass') || 
                    input.id.toLowerCase().includes('senha')) {
                    input.type = 'password';
                    loginFields.push(input);
                }
            }
        }
        
        // Verificar se há divs ou spans que possam conter campos de login
        var elements = document.querySelectorAll('div, span');
        for (var i = 0; i < elements.length; i++) {
            var elem = elements[i];
            if (elem.id && (
                elem.id.toLowerCase().includes('login') || 
                elem.id.toLowerCase().includes('user') || 
                elem.id.toLowerCase().includes('pass')
            )) {
                elem.style.display = 'block';
                elem.style.visibility = 'visible';
            }
        }
        
        return loginFields.length;
        """
        
        result = driver.execute_script(js_script)
        logger.info(f"JavaScript executado. Campos potencialmente revelados: {result}")
        
        # Capturar screenshot após injeção
        driver.save_screenshot("furnas_screenshots/07_apos_injecao_js.png")
        
        # Método 5: Tentar acessar diretamente uma possível página de login
        logger.info("Tentando acessar diretamente possíveis páginas de login...")
        
        # Lista de possíveis caminhos de login para SAP
        login_paths = [
            "/sap/bc/webdynpro/sap/zwda_portalclientes?sap-client=130&sap-theme=sap_bluecrystal&login=true",
            "/sap/bc/gui/sap/its/webgui?sap-client=130&sap-language=PT",
            "/sap/bc/webdynpro/sap/hrrcf_a_startpage_ext_cust",
            "/sap/bc/ui5_ui5/ui2/ushell/shells/abap/FioriLaunchpad.html",
            "/sap/bc/bsp/sap/it00/login.html",
            "/sap/bc/webdynpro/sap/hrrcf_a_act_cntr"
        ]
        
        base_url = "https://portaldocliente.furnas.com.br"
        
        for i, path in enumerate(login_paths):
            try:
                full_path = base_url + path
                logger.info(f"Tentando acessar: {full_path}")
                
                driver.get(full_path)
                time.sleep(3)
                
                # Capturar screenshot
                driver.save_screenshot(f"furnas_screenshots/08_pagina_login_direta_{i+1}.png")
                
                # Verificar se há campos de login
                inputs = driver.find_elements(By.TAG_NAME, "input")
                username_field = None
                password_field = None
                
                for inp in inputs:
                    input_type = inp.get_attribute("type")
                    if input_type == "text" or input_type == "email":
                        username_field = inp
                    elif input_type == "password":
                        password_field = inp
                
                if username_field and password_field:
                    logger.info(f"Campos de login encontrados na página direta {i+1}!")
                    
                    # Tentar realizar login
                    username_field.clear()
                    username_field.send_keys(USERNAME)
                    logger.info("Usuário inserido")
                    
                    password_field.clear()
                    password_field.send_keys(PASSWORD)
                    logger.info("Senha inserida")
                    
                    # Capturar screenshot com credenciais preenchidas
                    driver.save_screenshot(f"furnas_screenshots/09_credenciais_pagina_direta_{i+1}.png")
                    
                    # Procurar botão de login
                    login_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Login') or contains(text(), 'Entrar') or contains(text(), 'Acessar')]")
                    if login_buttons:
                        login_buttons[0].click()
                        logger.info("Botão de login clicado")
                    else:
                        # Tentar enviar o formulário com Enter
                        password_field.send_keys(Keys.RETURN)
                        logger.info("Tecla Enter pressionada para enviar formulário")
                    
                    # Aguardar processamento do login
                    time.sleep(5)
                    
                    # Capturar screenshot após tentativa de login
                    driver.save_screenshot(f"furnas_screenshots/10_apos_login_pagina_direta_{i+1}.png")
                    
                    # Verificar se o login foi bem-sucedido
                    page_source = driver.page_source.lower()
                    if "logout" in page_source or "bem-vindo" in page_source or "dashboard" in page_source:
                        logger.info("Login realizado com sucesso!")
                        
                        # Salvar cookies da sessão autenticada
                        cookies = driver.get_cookies()
                        with open("furnas_screenshots/cookies_autenticados.json", "w", encoding="utf-8") as f:
                            json.dump(cookies, f, indent=4)
                        logger.info("Cookies da sessão autenticada salvos")
                        
                        # Salvar HTML da página autenticada
                        with open("furnas_screenshots/pagina_autenticada.html", "w", encoding="utf-8") as f:
                            f.write(driver.page_source)
                        logger.info("HTML da página autenticada salvo")
                        
                        break
                    else:
                        logger.warning(f"Login na página direta {i+1} pode ter falhado. Tentando próxima...")
                else:
                    logger.info(f"Campos de login não encontrados na página direta {i+1}")
            
            except Exception as e:
                logger.error(f"Erro ao acessar página direta {i+1}: {str(e)}")
        
        # Fechar o navegador
        driver.quit()
        logger.info("Análise interativa concluída")
        
    except Exception as e:
        logger.error(f"Erro na análise interativa: {str(e)}")

if __name__ == "__main__":
    logger.info("Iniciando análise interativa do portal do cliente Furnas...")
    
    # Tentar login interativo
    login_interativo()
    
    logger.info("Análise interativa concluída.")
