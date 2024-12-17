from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import os
import pdfkit
import requests
from bs4 import BeautifulSoup

# Caminho para o executável do wkhtmltopdf
wkhtmltopdf_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

# Diretório base de download
base_download_directory = "C:\\Users\\Bruno\\Downloads\\ARGO"

# Diretório principal AE
ae_directory = os.path.join(base_download_directory, "SIGETPLUS_")
if not os.path.exists(ae_directory):
    os.makedirs(ae_directory)

# Dicionário de transmissoras e seus nomes
transmissoras = {
    
            "1320": "RIALMA",
            
}

def download_file(url, save_path):
    """Baixa um arquivo de uma URL e salva no caminho especificado."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()  # Levantar exceção para status HTTP de erro
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f'Arquivo baixado com sucesso: {save_path}')
        return True
    except requests.exceptions.RequestException as e:
        print(f'Erro ao baixar o arquivo: {e}')
        return False

def construir_url_xml(empresa, agente, ano, mes):
    """Constrói o URL do índice XML com base nos parâmetros fornecidos."""
    return f'http://notas.sigetplus.com.br/{empresa}/{agente}/{ano}/{mes}/XML/'

def download_xml_from_index(empresa, agente, ano, mes, save_path):
    """Baixa o XML a partir de um índice de diretório."""
    index_url = construir_url_xml(empresa, agente, ano, mes)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        # Obter o conteúdo do índice
        response = requests.get(index_url, headers=headers)
        response.raise_for_status()

        # Analisar o HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        link = soup.find('a', href=True, text=lambda x: x.endswith('.xml'))

        if link:
            xml_url = index_url + link['href']
            # Baixar o XML
            if download_file(xml_url, save_path):
                print(f'XML baixado com sucesso: {save_path}')
                # Verificar se o XML é válido
                with open(save_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    if not content.startswith('<?xml'):
                        print('Erro: XML não é válido.')
                        return False
                return True
            else:
                print('Falha ao baixar o XML.')
                return False
        else:
            print('Link do XML não encontrado no índice.')
            return False
    except requests.exceptions.RequestException as e:
        print(f'Erro ao acessar o índice: {e}')
        return False

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

        # Loop para percorrer todos os agentes
        for agente, agente_nome in agentes.items():
            # Criar diretório para o agente dentro da pasta AE
            agent_directory = os.path.join(ae_directory, agente_nome)
            if not os.path.exists(agent_directory):
                os.makedirs(agent_directory)

            # Loop para percorrer todas as transmissoras
            for target_code, transmissora_name in transmissoras.items():
                found = False
                page = 1
                print(f"Procurando pela transmissora com código {target_code} ({transmissora_name}) para o agente {agente_nome}...")

                # Criar diretório para a transmissora dentro do diretório do agente
                transmissora_directory = os.path.join(agent_directory, transmissora_name)
                if not os.path.exists(transmissora_directory):
                    os.makedirs(transmissora_directory)

                # Loop para percorrer todas as páginas
                while True:
                    # Ajustar a URL para o agente e a página atual
                    url = f'https://sys.sigetplus.com.br/portal?_=1720747296557&agent={agente}&page={page}'
                    driver.get(url)

                    # Esperar que o conteúdo da página carregue totalmente
                    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

                    # Procurar todas as linhas da tabela
                    rows = driver.find_elements(By.XPATH, '//tr')

                    # Verificar cada linha
                    for row in rows:
                        try:
                            td_elements = row.find_elements(By.TAG_NAME, 'td')
                            for td in td_elements:
                                if target_code in td.text:
                                    print(f'Transmissora com código {target_code} ({transmissora_name}) encontrada na página {page}')
                                    found = True

                                    # Procurar os links na mesma linha
                                    pdf_link = None
                                    xml_link = None
                                    danfe_link = None
                                    links = row.find_elements(By.TAG_NAME, 'a')
                                    for link in links:
                                        href = link.get_attribute('href')
                                        if 'billet' in href:
                                            pdf_link = href
                                            print(f'Link do PDF encontrado: {pdf_link}')
                                        elif 'xml' in link.text.lower():
                                            xml_link = href
                                            print(f'Link do XML encontrado: {xml_link}')
                                        elif 'danfe' in link.text.lower():
                                            danfe_link = href
                                            print(f'Link do DANFE encontrado: {danfe_link}')

                                    # Opções para o pdfkit
                                    pdf_options = {
                                        'no-stop-slow-scripts': None,
                                        'enable-local-file-access': None
                                    }

                                    # Baixar o PDF usando pdfkit
                                    if pdf_link:
                                        save_path_pdf = os.path.join(transmissora_directory, f"{target_code}.pdf")
                                        pdfkit.from_url(pdf_link, save_path_pdf, configuration=config, options=pdf_options)
                                        print(f'PDF baixado com sucesso: {save_path_pdf}')

                                    # Baixar o XML usando requests
                                    if xml_link:
                                        save_path_xml = os.path.join(transmissora_directory, f"{target_code}.xml")
                                        if download_file(xml_link, save_path_xml):
                                            print(f'XML baixado com sucesso: {save_path_xml}')
                                        else:
                                            print(f'Falha ao baixar o XML: {xml_link}')

                                    # Baixar o DANFE usando requests e nomear com o nome da transmissora
                                    if danfe_link:
                                        transmissora_name_clean = transmissora_name.replace(" ", "_").replace("/", "_").replace("\\", "_")
                                        save_path_danfe = os.path.join(transmissora_directory, f"{transmissora_name_clean}_DANFE.pdf")
                                        if download_file(danfe_link, save_path_danfe):
                                            print(f'DANFE baixado com sucesso: {save_path_danfe}')
                                        else:
                                            print(f'Falha ao baixar o DANFE: {danfe_link}')
                                    break

                        except StaleElementReferenceException:
                            print("Elemento obsoleto encontrado, tentando novamente...")
                            continue
                        except TimeoutException:
                            print("Tempo de espera excedido, tentando novamente...")
                            continue
                        except NoSuchElementException:
                            print("Elemento não encontrado, tentando novamente...")
                            continue

                        if found:
                            break

                    if found:
                        break

                    # Verificar se há um link para a próxima página (ou algum indicador de que a próxima página existe)
                    next_button = driver.find_elements(By.XPATH, '//*[contains(@class, "next")]')
                    if not next_button and not rows:
                        break  # Não há mais páginas ou não há mais resultados

                    page += 1

                if not found:
                    print(f'Transmissora com código {target_code} ({transmissora_name}) não encontrada em nenhuma página')
    finally:
        # Fechar o navegador
        driver.quit()

def baixar_xml_para_todos_os_agentes(agentes, empresa, ano, mes, base_directory):
    """Baixa o XML para todos os agentes fornecidos."""
    for agente, nome_agente in agentes.items():
        save_path = f'{base_directory}\\{nome_agente}\\RIALMA\\ONS{agente}.xml'
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))
        sucesso = download_xml_from_index(empresa, agente, ano, mes, save_path)
        if sucesso:
            print(f'XML para o agente {nome_agente} baixado com sucesso.')
        else:
            print(f'Falha ao baixar o XML para o agente {nome_agente}.')

# Exemplo de uso
empresa_re = '44857667000342'
empresa_ae = '44857667000342'  # Substitua pelo código correto se necessário
ano = '2024'
mes = '12'

# Agentes da Rio Energy
agentes_re_1 = {
    "3947": "SDBA",
    "3948": "SDBB",
    "3969": "SDBC",
    "3970": "SDBD",
    "3972": "SDBF",
    "3976": "SDBE",
    "4316": "CECF",
}

agentes_re_2 = {
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

# Agentes da América Energia
agentes_ae_1 = {
    "3859": "SJP I",
    "3860": "SJP II",
    "3861": "SJP III",
    "3862": "SJP IV",
    "3863": "SJP V",
    "3864": "SJP VI",
}

agentes_ae_2 = {
    "8011": "LIBRA",
}

agentes_ae_3 = {
    "3740": "COREMA I",
    "3741": "COREMA II",
    "3750": "COREMA III",
}

print("\nBaixando XML para agentes da Rio Energy (Grupo 1)...")
baixar_xml_para_todos_os_agentes(agentes_re_1, empresa_re, ano, mes, 'C:\\Users\\Bruno\\Downloads\\ARGO\\RE')

print("\nBaixando XML para agentes da Rio Energy (Grupo 2)...")
baixar_xml_para_todos_os_agentes(agentes_re_2, empresa_re, ano, mes, 'C:\\Users\\Bruno\\Downloads\\ARGO\\RE')

print("\nBaixando XML para agentes da América Energia (Grupo 1)...")
baixar_xml_para_todos_os_agentes(agentes_ae_1, empresa_ae, ano, mes, 'C:\\Users\\Bruno\\Downloads\\ARGO\\AE')

print("\nBaixando XML para agentes da América Energia (Grupo 2)...")
baixar_xml_para_todos_os_agentes(agentes_ae_2, empresa_ae, ano, mes, 'C:\\Users\\Bruno\\Downloads\\ARGO\\AE')

print("\nBaixando XML para agentes da América Energia (Grupo 3)...")
baixar_xml_para_todos_os_agentes(agentes_ae_3, empresa_ae, ano, mes, 'C:\\Users\\Bruno\\Downloads\\ARGO\\AE')
