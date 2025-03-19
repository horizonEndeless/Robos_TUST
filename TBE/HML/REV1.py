from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import logging
 
def setup_logger():
    """Configura e retorna o logger"""
    # Configurar o logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)
 
# Criar logger global
logger = setup_logger()
 
def create_download_dir(base_dir, cnpj, empresa_nome):
    """Cria diretório específico para a empresa"""
    empresa_nome = empresa_nome.replace('/', '-').replace('\\', '-').strip()
    download_dir = os.path.join(base_dir, f"CNPJ_{cnpj}", empresa_nome)
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    return download_dir
 
def login_tbe():
    global logger
   
    # Diretório base para downloads
    base_download_dir = r"C:\Downloads\XML_TBE"
    if not os.path.exists(base_download_dir):
        os.makedirs(base_download_dir)
   
    # Configurar o driver do Chrome com opções para download automático
    chrome_options = webdriver.ChromeOptions()
    # Configurar diretório de download (ajuste para seu diretório desejado)
    prefs = {
        "download.default_directory": base_download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
   
    try:
        # Abrir o site
        driver.get("https://portalcliente.tbenergia.com.br/")
       
        # Aguardar elementos estarem presentes e interagíveis
        wait = WebDriverWait(driver, 10)
       
        # Login
        login_field = wait.until(EC.presence_of_element_located((By.NAME, "Login")))
        login_field.click()
        login_field.send_keys("carol1758")
       
        # Senha
        senha_field = wait.until(EC.presence_of_element_located((By.NAME, "Senha")))
        senha_field.click()
        senha_field.send_keys("c@rol1758")
       
        # Botão de login
        login_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit']")))
        login_button.click()
       
        # Aguardar a página de fechamento carregar
        wait.until(EC.url_to_be("https://portalcliente.tbenergia.com.br/Fechamento"))
       
        # Clicar no campo de seleção do Chosen
        chosen_field = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[@id='CNPJ_chosen']/a/span")))
        chosen_field.click()
       
        # Clicar no campo de busca do Chosen
        search_field = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//*[@id='CNPJ_chosen']/div/div/input")))
        search_field.click()
       
        # Selecionar a opção específica (4313)
        option = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[@id='CNPJ_chosen']/div/ul/li[contains(text(), '4313')]")))
        option.click()
 
        time.sleep(2)
       
        # Clicar no botão Filtrar
        filtrar_button = wait.until(EC.element_to_be_clickable(
            (By.ID, "BtnFiltrar")))
        filtrar_button.click()
       
        # Aguardar um momento para os dados carregarem
        time.sleep(3)
       
        # Aguardar a tabela de resultados carregar
        wait.until(EC.presence_of_element_located((By.ID, "NfRecentes")))
       
        # Inicializar contadores
        total_xmls = 0
        pagina_atual = 1  # Definindo a variável aqui
        empresas_processadas = set()
       
        logger.info("Iniciando processamento dos XMLs...")
       
        while True:
            logger.info(f"\nProcessando página {pagina_atual}")
           
            xml_links = wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, "//table[@id='NfRecentes']//a[contains(text(), 'XML')]")))
            rows = driver.find_elements(By.XPATH, "//table[@id='NfRecentes']/tbody/tr")
           
            logger.info(f"Encontrados {len(xml_links)} XMLs na página {pagina_atual}")
           
            for i, (row, link) in enumerate(zip(rows, xml_links), 1):
                try:
                    # Obter informações da linha atual com o mapeamento correto
                    competencia = row.find_element(By.XPATH, "./td[1]").text    # Competência
                    nf_numero = row.find_element(By.XPATH, "./td[2]").text      # Nro. NF
                    cnpj_atual = row.find_element(By.XPATH, "./td[5]").text     # CNPJ (coluna 5)
                    empresa_atual = row.find_element(By.XPATH, "./td[4]").text  # Empresa do Grupo
                    valor = row.find_element(By.XPATH, "./td[6]").text          # R$ Valor
                   
                    # Limpar o CNPJ (remover caracteres especiais)
                    cnpj_atual = ''.join(filter(str.isdigit, cnpj_atual))
                   
                    # Log detalhado do download
                    logger.info(f"\nBaixando XML {i}/{len(xml_links)} da página {pagina_atual}")
                    logger.info(f"Transmissora: {empresa_atual}")
                    logger.info(f"CNPJ: {cnpj_atual}")
                    logger.info(f"NF: {nf_numero}")
                    logger.info(f"Competência: {competencia}")
                    logger.info(f"Valor: {valor}")
                   
                    # Se for uma nova transmissora, criar diretório específico
                    if (cnpj_atual, empresa_atual) not in empresas_processadas:
                        download_dir = create_download_dir(base_download_dir, cnpj_atual, empresa_atual)
                        driver.execute_cdp_cmd('Page.setDownloadBehavior', {
                            'behavior': 'allow',
                            'downloadPath': download_dir
                        })
                        empresas_processadas.add((cnpj_atual, empresa_atual))
                        logger.info(f"Nova transmissora detectada: {empresa_atual}")
                        logger.info(f"CNPJ: {cnpj_atual}")
                        logger.info(f"Criado diretório: {download_dir}")
 
                    # Download do XML
                    driver.execute_script("arguments[0].scrollIntoView(true);", link)
                    time.sleep(1)
                    link.click()
                    total_xmls += 1
                    logger.info(f"✓ Download iniciado com sucesso")
                   
                except Exception as e:
                    logger.error(f"❌ Erro ao baixar XML na página {pagina_atual}: {str(e)}")
                    continue
           
            # Verificar se existe próxima página
            try:
                # Localizar o botão próximo
                next_button = wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#NfRecentes_next:not(.disabled)")))
               
                # Rolar até o final da página para garantir que o botão de próximo está visível
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
               
                # Verificar se o botão está habilitado
                if "disabled" in next_button.get_attribute("class"):
                    print("Chegou à última página")
                    break
               
                # Clicar no botão usando JavaScript
                driver.execute_script("arguments[0].click();", next_button)
               
                # Aguardar a tabela atualizar
                time.sleep(2)
               
            except Exception as e:
                print(f"Erro ao navegar para próxima página: {str(e)}")
                break
       
        # Aguardar downloads finalizarem
        time.sleep(5)
       
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")
       
    finally:
        # Você pode comentar esta linha se não quiser que o navegador feche automaticamente
        driver.quit()
 
if __name__ == "__main__":
    try:
        logger.info("Iniciando processo de download de XMLs")
        login_tbe()
        logger.info("Processo finalizado")
    except Exception as e:
        logger.error(f"Erro fatal: {str(e)}")