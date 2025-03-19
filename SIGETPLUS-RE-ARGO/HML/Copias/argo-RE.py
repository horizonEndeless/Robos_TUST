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

# Caminho para o executável do wkhtmltopdf
wkhtmltopdf_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

# Diretório base de download
base_download_directory = "C:\\Users\\Bruno\\Downloads\\ARGO"

# Diretório principal para a empresa RE
re_directory = os.path.join(base_download_directory, "RE")
if not os.path.exists(re_directory):
    os.makedirs(re_directory)

# Dicionário de transmissoras e seus nomes
transmissoras = {
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
            # "1034": "TAESA-ETAU",
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
            
            "1304 - FS TRANSMISSORA DE ENERGIA ELETRICA S.A": "FS Transmissora",
            "1320 - RIALMA TRANSMISSORA DE ENERGIA IV": "RIALMA IV",
            "1228 - MARIANA TRANSMISSORA DE ENERGIA ELETRICA": "TAESA-MARIANA",
            "1133 - SÃO GOTARDO TRANSMISSORA DE ENERGIA": "1133 - TAESA-SGT",
            "1015 - TRANSMISSORA ALIANÇA DE ENERGIA": "TAESA-ETEO",
            # Adicione outros códigos e nomes de transmissoras aqui conforme necessário
}

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
            # Criar diretório para o agente dentro da pasta RE
            agent_directory = os.path.join(re_directory, agente_nome)
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

try:
    # Primeiro login
    login_and_download('carolina.ferreira@pontalenergy.com', agentes_1)

    # Segundo login
    login_and_download('carolina@engenho.com', agentes_2)

finally:
    # Listar arquivos no diretório de download
    print("Arquivos no diretório de download:")
    for agent_dir in os.listdir(re_directory):
        agent_path = os.path.join(re_directory, agent_dir)
        if os.path.isdir(agent_path):
            print(f"Arquivos para o agente {agent_dir}:")
            for transmissora_dir in os.listdir(agent_path):
                transmissora_path = os.path.join(agent_path, transmissora_dir)
                if os.path.isdir(transmissora_path):
                    print(f" - {transmissora_dir}:")
                    for filename in os.listdir(transmissora_path):
                        print(f"   - {filename}")