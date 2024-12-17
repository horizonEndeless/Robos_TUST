from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import os
import pdfkit
import requests
import time
from bs4 import BeautifulSoup
import concurrent.futures
from urllib.parse import urljoin, urlparse, unquote
import io
from PyPDF2 import PdfReader, PdfWriter

# Caminho para o executável do wkhtmltopdf
wkhtmltopdf_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

# Diretório base de download
base_download_directory = "C:\\Users\\Bruno\\Downloads\\ARGO\\"

def download_file(url, save_path):
    """Baixa um arquivo de uma URL e salva no caminho especificado."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Levantar exceção para status HTTP de erro
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f'Arquivo baixado com sucesso: {save_path}')
        return True
    except requests.exceptions.RequestException as e:
        print(f'Erro ao baixar o arquivo: {e}')
        return False

def arquivo_ja_existe(diretorio, tipos_arquivo):
    """Verifica se algum arquivo dos tipos especificados já existe no diretório."""
    for arquivo in os.listdir(diretorio):
        if any(arquivo.lower().endswith(tipo) for tipo in tipos_arquivo):
            return True
    return False

def extrair_codigo_ons(nome_transmissora):
    """Extrai o código ONS do nome da transmissora."""
    partes = nome_transmissora.split('-', 1)
    if len(partes) > 1:
        return partes[0].strip()
    return None

def baixar_fatura(driver, transmissora_directory, numero_fatura, tipo_documento):
    try:
        wait = WebDriverWait(driver, 30)
        link = wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[contains(@href, '/invoices/{numero_fatura}') and text()='{tipo_documento}']")))
        url = link.get_attribute('href')
        nome_arquivo = f"{numero_fatura}_{tipo_documento}.pdf"
        caminho_arquivo = os.path.join(transmissora_directory, nome_arquivo)
        
        if not os.path.exists(caminho_arquivo):
            if download_file(url, caminho_arquivo):
                print(f"Arquivo {nome_arquivo} baixado com sucesso.")
            else:
                print(f"Falha ao baixar {nome_arquivo}.")
        else:
            print(f"Arquivo {nome_arquivo} já existe. Pulando download.")
    except Exception as e:
        print(f"Erro ao baixar {tipo_documento} para fatura {numero_fatura}: {str(e)}")

def processar_transmissora(driver, row, agent_directory):
    td_elements = row.find_elements(By.TAG_NAME, 'td')
    if len(td_elements) >= 2:
        transmissora_name = td_elements[0].text.strip()
        numero_fatura = td_elements[1].text.strip()
        
        codigo_ons = extrair_codigo_ons(transmissora_name)
        if codigo_ons:
            transmissora_directory = os.path.join(agent_directory, f"{codigo_ons} - {transmissora_name}")
            if not os.path.exists(transmissora_directory):
                os.makedirs(transmissora_directory)

            try:
                click_with_retry(driver, row)
                time.sleep(2)  # Espera para a página carregar

                baixar_fatura(driver, transmissora_directory, numero_fatura, "DANFE")
                baixar_fatura(driver, transmissora_directory, numero_fatura, "XML")
                
                for i in range(1, 4):
                    baixar_fatura(driver, transmissora_directory, numero_fatura, f"Boleto #{i}")

                print(f"Processado: {transmissora_name} (Código ONS: {codigo_ons})")
            except Exception as e:
                print(f"Erro ao processar {transmissora_name}: {str(e)}")
            finally:
                driver.back()  # Volta para a página da lista de transmissoras
                time.sleep(2)  # Espera para a página carregar
        else:
            print(f"Não foi possível extrair o código ONS de {transmissora_name}")

def wait_for_element(driver, by, value, timeout=20):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

def click_with_retry(driver, element, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            element.click()
            return True
        except StaleElementReferenceException:
            if attempt == max_attempts - 1:
                raise
            time.sleep(1)
    return False

def get_filename_from_url(url):
    """Extrai o nome do arquivo da URL."""
    path = urlparse(url).path
    filename = unquote(os.path.basename(path))
    # Garante que o arquivo tenha a extensão .pdf para DANFEs e boletos
    if 'danfe' in url.lower() or 'billet' in url.lower():
        if not filename.lower().endswith('.pdf'):
            filename = f"{filename.split('.')[0]}.pdf"
    return filename

def baixar_danfe(driver, url, caminho_destino):
    print(f"Tentando baixar DANFE de: {url}")
    try:
        response = requests.get(url, stream=True, allow_redirects=True)
        response.raise_for_status()
        
        with open(caminho_destino, 'wb') as arquivo:
            for chunk in response.iter_content(chunk_size=8192):
                arquivo.write(chunk)
        
        if os.path.getsize(caminho_destino) == 0:
            os.remove(caminho_destino)
            print(f"Arquivo vazio removido: {caminho_destino}")
        else:
            print(f"DANFE baixada com sucesso: {caminho_destino}")
    except Exception as e:
        print(f"Erro ao baixar DANFE: {str(e)}")

def baixar_arquivo_rapido(url, caminho_destino):
    if os.path.exists(caminho_destino):
        print(f"Arquivo já existe: {caminho_destino}")
        return
    try:
        response = requests.get(url, stream=True, allow_redirects=True)
        response.raise_for_status()
        
        with open(caminho_destino, 'wb') as arquivo:
            for chunk in response.iter_content(chunk_size=8192):
                arquivo.write(chunk)
        
        if os.path.getsize(caminho_destino) == 0:
            os.remove(caminho_destino)
            print(f"Arquivo vazio removido: {caminho_destino}")
        else:
            print(f"Arquivo baixado: {caminho_destino}")
    except Exception as e:
        print(f"Erro ao baixar {url}: {str(e)}")

def baixar_boleto(driver, url, caminho_destino):
    print(f"Tentando baixar boleto de: {url}")
    original_window = driver.current_window_handle
    
    try:
        # Abre uma nova aba
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        
        # Navega para a URL do boleto
        driver.get(url)
        
        # Espera até que o conteúdo seja carregado
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Captura o HTML da página
        html_content = driver.page_source
        
        # Usa pdfkit para converter o HTML em PDF
        pdfkit.from_string(html_content, caminho_destino, configuration=config)
        
        print(f"Boleto salvo como PDF: {caminho_destino}")
    except Exception as e:
        print(f"Erro ao baixar boleto: {str(e)}")
        # Se falhar, tenta salvar uma captura de tela
        driver.save_screenshot(caminho_destino.replace('.pdf', '.png'))
        print(f"Captura de tela salva: {caminho_destino.replace('.pdf', '.png')}")
    finally:
        # Volta para a aba original e fecha a nova aba
        driver.close()
        driver.switch_to.window(original_window)

def baixar_faturas(driver, agent_directory, max_retries=3, page_timeout=20):
    page = 1
    while True:
        print(f"Processando página {page}")
        try:
            WebDriverWait(driver, page_timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "table-striped")))
        except TimeoutException:
            print(f"Timeout ao carregar a página {page}. Finalizando.")
            break

        rows = driver.find_elements(By.XPATH, '//table[@class="table table-striped table-bordered"]/tbody/tr')
        print(f"Total de linhas na página {page}: {len(rows)}")
        
        for row in rows:
            info = extrair_informacoes_fatura(row)
            if info:
                transmissora_directory = os.path.join(agent_directory, info['transmissora'])
                os.makedirs(transmissora_directory, exist_ok=True)
                
                if info['danfe_link']:
                    danfe_filename = get_filename_from_url(info['danfe_link'])
                    danfe_path = os.path.join(transmissora_directory, danfe_filename)
                    baixar_danfe(driver, info['danfe_link'], danfe_path)
                if info['xml_link']:
                    xml_filename = get_filename_from_url(info['xml_link'])
                    xml_path = os.path.join(transmissora_directory, xml_filename)
                    baixar_arquivo_rapido(info['xml_link'], xml_path)
                for link in info['boleto_links']:
                    boleto_filename = get_filename_from_url(link)
                    boleto_path = os.path.join(transmissora_directory, boleto_filename)
                    baixar_boleto(driver, link, boleto_path)
                
                print(f"Processado: {info['transmissora']} (Fatura: {info['numero_fatura']})")
        
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//a[@rel="next"]'))
            )
            next_url = next_button.get_attribute('href')
            driver.get(next_url)
            page += 1
            time.sleep(2)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Erro ao navegar para a próxima página: {str(e)}")
            print("Chegamos à última página ou houve um problema. Finalizando.")
            break

def extrair_informacoes_fatura(row):
    """Extrai informações de uma linha da tabela de faturas."""
    colunas = row.find_elements(By.TAG_NAME, 'td')
    if len(colunas) >= 10:
        transmissora = colunas[0].text.strip()
        numero_fatura = colunas[1].find_element(By.TAG_NAME, 'a').text.strip()
        danfe_link = colunas[8].find_element(By.TAG_NAME, 'a').get_attribute('href') if colunas[8].find_elements(By.TAG_NAME, 'a') else None
        xml_link = colunas[9].find_element(By.TAG_NAME, 'a').get_attribute('href') if colunas[9].find_elements(By.TAG_NAME, 'a') else None
        boleto_links = []
        for col in colunas[5:8]:
            links = col.find_elements(By.TAG_NAME, 'a')
            if links and 'billet' in links[0].get_attribute('href'):
                boleto_links.append(links[0].get_attribute('href'))
        return {
            'transmissora': transmissora,
            'numero_fatura': numero_fatura,
            'danfe_link': danfe_link,
            'xml_link': xml_link,
            'boleto_links': boleto_links
        }
    return None

def login_and_download(email, agentes):
    # Configurar o WebDriver usando o WebDriver Manager
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Executar em modo headless para evitar abrir a GUI do navegador
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Abrir o site
        driver.get('https://sys.sigetplus.com.br/portal/login')

        # Espera explícita para o campo de email
        wait = WebDriverWait(driver, 20)
        email_field = wait.until(EC.presence_of_element_located((By.ID, 'email')))

        # Digitar o email
        email_field.send_keys(email)

        # Espera explícita para o botão de login
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div[2]/form/div/div/div/button')))

        # Clicar no botão de login
        login_button.click()

        # Espera explícita após o login para o carregamento da página principal
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # Dicionário de transmissoras e seus nomes
        transmissoras = {
            
            # "1304 - FS TRANSMISSORA DE ENERGIA ELETRICA S.A": "FS Transmissora"
            
            # "1337": "DUNAS",
            # "1224": "ARGO",
            # "1273": "ARGO II",
            # "1241": "ARGO III",
            # "1272": "ARGO IV",
            # "1181": "ARGO V",
            # "1184": "ARGO VI",
            # #"1261": "ARGO",
            # "1244": "MANTIQUEIRA",
            # "1275": "CHIMARRAO",
            # "1322": "PAMPA",
            # "1217": "ARCOVERDE",
            # "1327": "AGUA VERMELHA",
            # "1311": "ETTM",
            # "1307": "ITAMARACA",
            # "1235": "LEST",
            # "1131": "TPAE",
            # "1229": "VINEYARDS",
            # "1183": "LAT",
            # "1299": "LINHA VERDE II",
            # "1216": "SANTA LUCIA",
            # "1054": "INTESA",
            # "1206": "SANTA MARIA",
            # "1330": "LINHA VERDE I",
            # "1173": "PTE",
            # "1199": "TJMME",
            # "1227": "GSTE",
            # "1320": "RIALMA IV",
            # "1163": "TP NORTE (MATRINCHA)",
            # "1182": "TP SUL (GUARACIABA)",
            # "1195": "BMTE",
            # "1015": "TAESA-ETEO",
            # "1021": "TAESA-NVT",
            # "1022": "TAESA-TSN",
            # "1023": "TAESA-GTESA",
            # "1025": "TAESA-NTE",
            # "1026": "TAESA-STE",
            # "1029": "TAESA-PATESA",
            # "1034": "TAESA-SGT",
            # "1036": "TAESA-ATE",
            # "1037": "TAESA-MUNIRAH",
            # "1046": "TAESA-ATE II",
            # "1052": "TAESA-ATE III",
            # "1066": "TAESA-BRASNORTE",
            # "1133": "TAESA-SGT",
            # "1180": "SJTE",
            # "1189": "SPT",
            # "1212": "RIALMA I",
            # "1267": "SERTANEJA",
            # "1143": "LNT",
            # "1329": "SILVANIA",
            # "1208": "PRTE",
            # "1200": "CANARANA",
            # "1222": "XRTE",
            # "1060": "RPTE",
            # "1102": "ARARAQUARA",
            # "1096": "CATXERE",
            # "1045": "ITE",
            # "1059": "SPTE",
            # "1051": "SMTE",
            # "1027": "ETIM",
            # "1079": "IRACEMA",
            # "1061": "PCTE",
            # "1089": "ITATIM",
            # "1117": "MONTES CLAROS",
            # "1042": "PPTE",
            # "1017": "EXPANSION",
            # "1124": "ATLANTICO",
            # "1179": "MRTE",
            # "1226": "TAESA-MIRACEMA",
            # "1228": "TAESA-MARIANA",
            # "1276": "JANAUBA",
            # "1288": "SANTANA",
            # "1289": "IE AIMORES",
            # "1298": "IE PARAGUACU",
            # "1316": "SAIRA",
            # "1243": "ARTEON Z1",
            # "1281": "ARTEON Z3",
            # "1291": "SIMOES",
            # "1304": "FS Transmissora",
            # "1268": "COLINAS",
            # "1242": "ARTEON Z2"
            
            

            
            # Adicione outras transmissoras se necessário
        }
        
        # Dicionário para armazenar a contagem de transmissoras por agente
        transmissoras_por_agente = {}

        # Loop para percorrer todos os agentes
        for agente, agente_nome in agentes.items():
            # Criar diretório para o agente
            agent_directory = os.path.join(base_download_directory, agente_nome)
            if not os.path.exists(agent_directory):
                os.makedirs(agent_directory)

            url = f'https://sys.sigetplus.com.br/portal?_=1728654874046&agent={agente}'
            driver.get(url)
            time.sleep(2)

            baixar_faturas(driver, agent_directory)

    finally:
        driver.quit()

# Dicionário de agentes e suas respectivas pastas
agentes_1 = {
    "3748": "DE",
    
}

try:
    # Primeiro login
    login_and_download('services.easytust@diamanteenergia.com.br', agentes_1)

finally:
    # Listar arquivos no diretório de download
    print("Arquivos no diretório de download:")
    for agent_dir in os.listdir(base_download_directory):
        agent_path = os.path.join(base_download_directory, agent_dir)
        if os.path.isdir(agent_path):
            print(f"Arquivos para o agente {agent_dir}:")
            for transmissora_dir in os.listdir(agent_path):
                transmissora_path = os.path.join(agent_path, transmissora_dir)
                if os.path.isdir(transmissora_path):
                    print(f" - {transmissora_dir}:")
                    for filename in os.listdir(transmissora_path):
                        print(f"   - {filename}")