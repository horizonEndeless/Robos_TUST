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
import re

# Caminho para o executável do wkhtmltopdf
wkhtmltopdf_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

# Diretório base de download
base_download_directory = "C:\\Users\\Bruno\\Downloads\\ARGO\\RE\\"

def get_sigetplus_file_url(driver, url):
    """
    Trata URLs do SIGETPLUS que redirecionam para uma página de índice.
    Retorna a URL direta do arquivo PDF/XML.
    """
    try:
        # Tratamento específico para URLs do notas.sigetplus.com.br
        if "notas.sigetplus.com.br" in url:
            # Acessa a página índice
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_tag_name("body")
            )
            
            # Procura por links na página
            links = driver.find_elements(By.TAG_NAME, "a")
            for link in links:
                href = link.get_attribute("href")
                if not href or href == "/" or "Parent Directory" in link.text:
                    continue
                    
                # Para DANFE, procura arquivo PDF
                if "/DANFE/" in url and href.endswith(".pdf"):
                    return href
                # Para XML, procura arquivo XML
                elif "/XML/" in url and href.endswith(".xml"):
                    return href
                # Se encontrar apenas um link que não seja Parent Directory
                elif href != url and "Parent Directory" not in link.text:
                    # Acessa o link encontrado para pegar o arquivo final
                    driver.get(href)
                    return driver.current_url
            
            return None
        
        return url

    except Exception as e:
        print(f"Erro ao processar URL {url}: {e}")
        return None

def download_file(driver, url, save_path):
    """
    Baixa um arquivo da URL especificada e salva no caminho indicado.
    """
    try:
        # Obtém a URL final do arquivo
        final_url = get_sigetplus_file_url(driver, url)
        if not final_url:
            print(f"Não foi possível obter a URL final para {url}")
            return False

        # Usa os cookies do Selenium para a requisição
        selenium_cookies = driver.get_cookies()
        session = requests.Session()
        for cookie in selenium_cookies:
            session.cookies.set(cookie['name'], cookie['value'])
            
        response = session.get(final_url, stream=True)
        response.raise_for_status()
        
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        # Verifica se o arquivo foi baixado com sucesso
        if os.path.getsize(save_path) > 0:
            print(f"Arquivo baixado com sucesso: {save_path}")
            return True
        else:
            os.remove(save_path)
            print(f"Arquivo vazio removido: {save_path}")
            return False
            
    except Exception as e:
        print(f"Erro ao baixar arquivo {url}: {e}")
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
        link = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//a[contains(@href, '/invoices/{numero_fatura}') and text()='{tipo_documento}']")
        ))
        url = link.get_attribute('href')
        
        # Define extensão e nome do arquivo baseado no tipo
        if tipo_documento == "DANFE":
            ext = ".pdf"
            index_ext = ".pdf"
        elif tipo_documento == "XML":
            ext = ".xml"
            index_ext = ".xml"
        else:  # Boletos
            ext = ".pdf"
            index_ext = None
        
        nome_arquivo = f"{numero_fatura}_{tipo_documento}{ext}"
        caminho_arquivo = os.path.join(transmissora_directory, nome_arquivo)
        
        if not os.path.exists(caminho_arquivo):
            # Se for URL do notas.sigetplus.com.br, usa download especial
            if "notas.sigetplus.com.br" in url:
                if download_file_from_index(driver, url, index_ext, caminho_arquivo):
                    print(f"Arquivo {nome_arquivo} baixado com sucesso via página índice.")
                else:
                    print(f"Falha ao baixar {nome_arquivo} via página índice.")
            else:
                # Download normal para outros casos
                if download_file(driver, url, caminho_arquivo):
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

def baixar_faturas(driver, agent_directory):
    print("\nProcurando Rialma...")
    try:
        # Espera a tabela carregar
        table = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table-striped"))
        )
        
        # Encontra todas as linhas
        rows = table.find_elements(By.TAG_NAME, 'tr')
        
        for row in rows:
            try:
                if "RIALMA TRANSMISSORA DE ENERGIA IV" in row.text:
                    print("\nEncontrada linha da Rialma!")
                    processar_rialma(driver, row, agent_directory)
                    return  # Encerra após processar a Rialma
            except StaleElementReferenceException:
                continue
                
    except Exception as e:
        print(f"Erro ao procurar Rialma: {str(e)}")

def extrair_informacoes_fatura(row):
    """
    Extrai informações específicas da linha da tabela, com foco na Rialma
    """
    try:
        tds = row.find_elements(By.TAG_NAME, 'td')
        if len(tds) >= 10:  # Verifica se tem todas as colunas necessárias
            transmissora = tds[0].text.strip()
            
            # Verifica se é a Rialma
            if "RIALMA TRANSMISSORA DE ENERGIA IV" in transmissora:
                numero_fatura = tds[1].find_element(By.TAG_NAME, 'a').text.strip()
                
                # Pega os links de DANFE e XML
                danfe_link = tds[8].find_element(By.TAG_NAME, 'a').get_attribute('href')
                xml_link = tds[9].find_element(By.TAG_NAME, 'a').get_attribute('href')
                
                # Pega os links dos boletos (podem ser até 3)
                boleto_links = []
                for i in range(5, 8):  # Colunas 5, 6 e 7 são dos boletos
                    try:
                        boleto = tds[i].find_element(By.TAG_NAME, 'a')
                        if boleto:
                            boleto_links.append(boleto.get_attribute('href'))
                    except:
                        continue

                return {
                    'transmissora': transmissora,
                    'numero_fatura': numero_fatura,
                    'danfe_link': danfe_link,
                    'xml_link': xml_link,
                    'boleto_links': boleto_links
                }
    except Exception as e:
        print(f"Erro ao extrair informações da linha: {str(e)}")
    return None

def download_rialma_file(driver, index_url, save_path):
    """
    Função específica para baixar arquivos da Rialma usando apenas requests
    """
    try:
        # Headers padrão para simular um navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }
        
        # Primeiro, obtém a página índice
        print(f"Acessando página índice: {index_url}")
        response = requests.get(index_url, headers=headers)
        response.raise_for_status()
        
        # Usa BeautifulSoup para encontrar o link do arquivo
        soup = BeautifulSoup(response.text, 'html.parser')
        file_url = None
        
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and 'Parent Directory' not in link.text:
                if (('/DANFE/' in index_url and href.endswith('.pdf')) or 
                    ('/XML/' in index_url and href.endswith('.xml'))):
                    # Constrói a URL completa
                    file_url = urljoin(index_url, href)
                    print(f"Encontrado link do arquivo: {file_url}")
                    break
        
        if file_url:
            print(f"Baixando arquivo de: {file_url}")
            # Baixa o arquivo
            response = requests.get(file_url, headers=headers, stream=True)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            if os.path.getsize(save_path) > 0:
                print(f"Arquivo baixado com sucesso: {save_path}")
                return True
            else:
                os.remove(save_path)
                print(f"Arquivo vazio removido: {save_path}")
                return False
        else:
            print(f"Nenhum arquivo encontrado na página índice: {index_url}")
            return False
            
    except Exception as e:
        print(f"Erro ao baixar arquivo da Rialma: {str(e)}")
        return False

def processar_rialma(driver, row, agent_directory):
    """
    Processa especificamente a linha da Rialma
    """
    try:
        tds = row.find_elements(By.TAG_NAME, 'td')
        transmissora = tds[0].text.strip()
        numero_fatura = tds[1].find_element(By.TAG_NAME, 'a').text.strip()
        
        # Pega os links
        danfe_link = tds[8].find_element(By.TAG_NAME, 'a').get_attribute('href')
        xml_link = tds[9].find_element(By.TAG_NAME, 'a').get_attribute('href')
        
        # Cria diretório
        transmissora_directory = os.path.join(agent_directory, transmissora)
        os.makedirs(transmissora_directory, exist_ok=True)
        
        print(f"\nProcessando Rialma - Fatura: {numero_fatura}")
        
        # Baixa DANFE
        if danfe_link:
            print("\nBaixando DANFE...")
            danfe_path = os.path.join(transmissora_directory, f"{numero_fatura}_DANFE.pdf")
            download_rialma_file(driver, danfe_link, danfe_path)
        
        # Baixa XML
        if xml_link:
            print("\nBaixando XML...")
            xml_path = os.path.join(transmissora_directory, f"{numero_fatura}_XML.xml")
            download_rialma_file(driver, xml_link, xml_path)
        
        # Baixa Boletos
        for i in range(5, 8):  # Colunas 5, 6 e 7 são dos boletos
            try:
                boleto = tds[i].find_element(By.TAG_NAME, 'a')
                if boleto:
                    boleto_link = boleto.get_attribute('href')
                    boleto_path = os.path.join(transmissora_directory, f"{numero_fatura}_boleto_{i-4}.pdf")
                    baixar_boleto(driver, boleto_link, boleto_path)
            except:
                continue
        
        print(f"\nProcessado: {transmissora} (Fatura: {numero_fatura})")
        
    except Exception as e:
        print(f"Erro ao processar Rialma: {str(e)}")

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
    "3947": "SDBA",
    "3948": "SDBB",
    "3969": "SDBC",
    "3970": "SDBD",
    "3972": "SDBF",
    "3976": "SDBE",
    "4316": "CECF",
}

agentes_2 = {
    "3430": "CECA",
    "3431": "CECB",
    "3432": "CECC",
    "4315": "CECE",
    "4415": "CECD",
    "3497": "ITA2",
    "3498": "ITA5",
    "3502": "ITA1",
    "3503": "ITA3",
    "3530": "ITA4",
    "3531": "ITA6",
    "3532": "ITA7",
    "3537": "ITA8",
    "3538": "ITA9",
    "4313": "BRJA",
    "4314": "BRJB"
}

def analisar_linha_rialma(driver, row):
    """
    Analisa e exibe todos os links e informações da linha da Rialma
    """
    try:
        tds = row.find_elements(By.TAG_NAME, 'td')
        print("\n=== Análise da linha da Rialma ===")
        print(f"Número de colunas: {len(tds)}")
        
        for i, td in enumerate(tds):
            print(f"\nColuna {i}:")
            print(f"Texto: {td.text.strip()}")
            
            # Procura por links na coluna
            links = td.find_elements(By.TAG_NAME, 'a')
            for link in links:
                print(f"Link encontrado: {link.get_attribute('href')}")
                print(f"Texto do link: {link.text.strip()}")
                print(f"Classes do link: {link.get_attribute('class')}")
                
    except Exception as e:
        print(f"Erro ao analisar linha da Rialma: {str(e)}")

def download_file_from_index(driver, index_url, file_extension, save_path):
    """
    Baixa arquivo a partir de uma página índice.
    """
    try:
        # Acessa a página índice
        driver.get(index_url)
        time.sleep(2)  # Espera a página carregar
        
        # Procura por links que não sejam "Parent Directory"
        links = driver.find_elements(By.TAG_NAME, 'a')
        file_url = None
        
        for link in links:
            href = link.get_attribute('href')
            if href and not "Parent Directory" in link.text:
                if href.endswith(file_extension):
                    file_url = href
                    break
        
        if file_url:
            response = requests.get(file_url, stream=True)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            if os.path.getsize(save_path) > 0:
                print(f"Arquivo baixado com sucesso: {save_path}")
                return True
            else:
                os.remove(save_path)
                print(f"Arquivo vazio removido: {save_path}")
                return False
        else:
            print(f"Nenhum arquivo {file_extension} encontrado em {index_url}")
            return False
            
    except Exception as e:
        print(f"Erro ao baixar arquivo de {index_url}: {str(e)}")
        return False

try:
    # Primeiro login
    login_and_download('carolina.ferreira@pontalenergy.com', agentes_1)

    # Segundo login
    login_and_download('carolina@engenho.com', agentes_2)

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