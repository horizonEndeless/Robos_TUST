from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import requests
from bs4 import BeautifulSoup
import re
import json
import datetime
from urllib.parse import urljoin
import shutil
import pdfkit
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("faturas_download.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Lista de códigos ONS e empresas
EMPRESAS = [
    {"codigo": "4313", "nome": "BRJA"},
    {"codigo": "4314", "nome": "BRJB"},
    {"codigo": "3430", "nome": "CECA"},
    {"codigo": "3431", "nome": "CECB"},
    {"codigo": "3432", "nome": "CECC"},
    {"codigo": "4415", "nome": "CECD"},
    {"codigo": "4315", "nome": "CECE"},
    {"codigo": "4316", "nome": "CECF"},
    {"codigo": "3502", "nome": "ITA1"},
    {"codigo": "3497", "nome": "ITA2"},
    {"codigo": "3503", "nome": "ITA3"},
    {"codigo": "3530", "nome": "ITA4"},
    {"codigo": "3498", "nome": "ITA5"},
    {"codigo": "3531", "nome": "ITA6"},
    {"codigo": "3532", "nome": "ITA7"},
    {"codigo": "3537", "nome": "ITA8"},
    {"codigo": "3538", "nome": "ITA9"},
    {"codigo": "3947", "nome": "SDBA"},
    {"codigo": "3948", "nome": "SDBB"},
    {"codigo": "3969", "nome": "SDBC"},
    {"codigo": "3970", "nome": "SDBD"},
    {"codigo": "3976", "nome": "SDBE"},
    {"codigo": "3972", "nome": "SDBF"}
]

def analisar_site_tecp():
    # Configurar o Chrome
    chrome_options = Options()
    # Descomente a linha abaixo se quiser executar em modo headless (sem interface gráfica)
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Inicializar o driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # Acessar o site
        print("Acessando o site da TECP Energia...")
        driver.get("https://tecpenergia.com.br/")
        time.sleep(3)  # Aguardar carregamento da página
        
        # Verificar se há área de login
        print("Procurando área de login...")
        login_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Login')]")
        
        if login_elements:
            print("Área de login encontrada!")
            # Clicar no botão de login
            login_elements[0].click()
            time.sleep(2)
            
            # Verificar campos de login
            username_field = driver.find_elements(By.ID, "user_login")
            password_field = driver.find_elements(By.ID, "user_pass")
            
            if username_field and password_field:
                print("Campos de login encontrados:")
                print("- Campo de usuário: Presente")
                print("- Campo de senha: Presente")
                
                # Verificar se há informações sobre faturas
                print("\nProcurando informações sobre faturas...")
                fatura_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Fatura')]")
                
                if fatura_elements:
                    print("Informações sobre faturas encontradas!")
                    for elem in fatura_elements:
                        print(f"- {elem.text}")
                else:
                    print("Não foram encontradas informações específicas sobre faturas na página de login.")
                
                print("\nPara acessar a fatura 4313, provavelmente será necessário:")
                print("1. Fazer login com credenciais válidas")
                print("2. Navegar até a seção de faturas")
                print("3. Buscar pela fatura específica (4313)")
            else:
                print("Não foi possível identificar os campos de login.")
        else:
            print("Não foi encontrada uma área de login explícita.")
            
            # Procurar por links relacionados a faturas
            print("\nProcurando links relacionados a faturas...")
            fatura_links = driver.find_elements(By.XPATH, "//a[contains(text(), 'Fatura') or contains(@href, 'fatura')]")
            
            if fatura_links:
                print("Links relacionados a faturas encontrados:")
                for link in fatura_links:
                    print(f"- {link.text}: {link.get_attribute('href')}")
            else:
                print("Não foram encontrados links diretos para faturas.")
        
        # Capturar screenshot para análise visual
        screenshot_path = os.path.join(os.getcwd(), "tecp_site.png")
        driver.save_screenshot(screenshot_path)
        print(f"\nCaptura de tela salva em: {screenshot_path}")
        
    except Exception as e:
        print(f"Ocorreu um erro durante a análise: {str(e)}")
    
    finally:
        # Fechar o navegador
        driver.quit()
        print("\nAnálise concluída!")

def analisar_site_tecp_requests():
    # Headers para simular um navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    
    # Criar uma sessão para manter cookies
    session = requests.Session()
    
    try:
        # Acessar o site principal
        print("Acessando o site da TECP Energia via requests...")
        response = session.get("https://tecpenergia.com.br/", headers=headers)
        response.raise_for_status()  # Verificar se a requisição foi bem-sucedida
        
        # Analisar o HTML da página
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Procurar por formulário de login
        login_form = soup.find('form', {'id': 'loginform'}) or soup.find('form', {'action': re.compile(r'login|wp-login')})
        
        if login_form:
            print("Formulário de login encontrado!")
            
            # Identificar campos de login
            login_fields = login_form.find_all('input')
            login_info = {}
            
            for field in login_fields:
                field_name = field.get('name')
                if field_name:
                    login_info[field_name] = field.get('id', '')
            
            print("Campos do formulário de login:")
            for name, id_value in login_info.items():
                print(f"- Campo '{name}' (ID: '{id_value}')")
            
            # Identificar URL de login
            login_url = login_form.get('action', '')
            if login_url:
                print(f"URL de login: {login_url}")
            else:
                print("URL de login não encontrada explicitamente no formulário.")
        else:
            print("Formulário de login não encontrado diretamente na página inicial.")
            
            # Procurar por links de login
            login_links = soup.find_all('a', href=re.compile(r'login|wp-login'))
            if login_links:
                print("Links de login encontrados:")
                for link in login_links:
                    print(f"- {link.text.strip()}: {link.get('href')}")
                    
                    # Tentar acessar a página de login
                    login_url = link.get('href')
                    if login_url and not login_url.startswith(('http://', 'https://')):
                        if login_url.startswith('/'):
                            login_url = f"https://tecpenergia.com.br{login_url}"
                        else:
                            login_url = f"https://tecpenergia.com.br/{login_url}"
                    
                    print(f"Tentando acessar a página de login: {login_url}")
                    login_response = session.get(login_url, headers=headers)
                    if login_response.status_code == 200:
                        login_soup = BeautifulSoup(login_response.text, 'html.parser')
                        login_form = login_soup.find('form', {'id': 'loginform'}) or login_soup.find('form', {'action': re.compile(r'login|wp-login')})
                        if login_form:
                            print("Formulário de login encontrado na página de login!")
            else:
                print("Nenhum link de login encontrado.")
        
        # Procurar por links relacionados a faturas
        print("\nProcurando links relacionados a faturas...")
        fatura_links = soup.find_all('a', text=re.compile(r'[Ff]atura'))
        fatura_links.extend(soup.find_all('a', href=re.compile(r'fatura')))
        
        if fatura_links:
            print("Links relacionados a faturas encontrados:")
            for link in fatura_links:
                print(f"- {link.text.strip()}: {link.get('href')}")
        else:
            print("Não foram encontrados links diretos para faturas.")
        
        # Procurar por menções a faturas no texto
        fatura_mentions = soup.find_all(text=re.compile(r'[Ff]atura'))
        if fatura_mentions:
            print("\nMenções a faturas encontradas no texto:")
            for mention in fatura_mentions:
                parent = mention.parent
                context = parent.get_text().strip()
                if len(context) > 200:
                    context = context[:200] + "..."
                print(f"- {context}")
        
        # Procurar pelo ícone de cadeado mencionado no site
        print("\nProcurando pelo ícone de cadeado mencionado...")
        cadeado_elements = soup.find_all(text=re.compile(r'[Cc]adeado'))
        if cadeado_elements:
            print("Menções ao cadeado encontradas:")
            for element in cadeado_elements:
                parent = element.parent
                context = parent.get_text().strip()
                if len(context) > 200:
                    context = context[:200] + "..."
                print(f"- {context}")
        
        print("\nPara acessar a fatura 4313, provavelmente será necessário:")
        print("1. Fazer login com credenciais válidas (usuário e senha)")
        print("2. Procurar pelo ícone de cadeado no canto superior direito")
        print("3. Registrar o código de usuário 'ONS' para download da NF")
        print("4. Buscar pela fatura específica (4313)")
        
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição HTTP: {str(e)}")
    except Exception as e:
        print(f"Ocorreu um erro durante a análise: {str(e)}")
    
    print("\nAnálise via requests concluída!")

def tentar_acessar_fatura_requests():
    # Headers para simular um navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    
    # Criar uma sessão para manter cookies
    session = requests.Session()
    
    try:
        # Acessar o site principal
        print("Acessando o site da TECP Energia...")
        response = session.get("https://tecpenergia.com.br/", headers=headers)
        response.raise_for_status()
        
        # Salvar o HTML para análise
        with open("tecp_homepage.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("HTML da página inicial salvo em 'tecp_homepage.html'")
        
        # Analisar o HTML da página
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Procurar por todos os links na página
        print("\nAnalisando todos os links da página...")
        all_links = soup.find_all('a', href=True)
        
        for link in all_links:
            href = link.get('href')
            text = link.get_text().strip()
            print(f"Link: '{text}' -> {href}")
            
            # Verificar se o link pode estar relacionado a login ou faturas
            if any(keyword in href.lower() or keyword in text.lower() for keyword in ['login', 'fatura', 'conta', 'acesso']):
                print(f"Link potencialmente relevante encontrado: '{text}' -> {href}")
                
                # Tentar acessar o link
                link_url = href
                if not link_url.startswith(('http://', 'https://')):
                    if link_url.startswith('/'):
                        link_url = f"https://tecpenergia.com.br{link_url}"
                    else:
                        link_url = f"https://tecpenergia.com.br/{link_url}"
                
                try:
                    print(f"Tentando acessar: {link_url}")
                    link_response = session.get(link_url, headers=headers, timeout=10)
                    
                    if link_response.status_code == 200:
                        # Salvar o HTML para análise
                        with open(f"tecp_link_{text.replace(' ', '_')}.html", "w", encoding="utf-8") as f:
                            f.write(link_response.text)
                        print(f"HTML da página '{text}' salvo")
                        
                        # Verificar se há formulário de login ou menção a faturas
                        link_soup = BeautifulSoup(link_response.text, 'html.parser')
                        login_form = link_soup.find('form')
                        if login_form:
                            print(f"Formulário encontrado na página '{text}':")
                            print(f"Action: {login_form.get('action')}")
                            print(f"Method: {login_form.get('method')}")
                            
                            # Listar campos do formulário
                            form_inputs = login_form.find_all('input')
                            for input_field in form_inputs:
                                print(f"- Campo: {input_field.get('name')} (Tipo: {input_field.get('type')})")
                except Exception as e:
                    print(f"Erro ao acessar {link_url}: {str(e)}")
        
        # Procurar por elementos que possam conter o ícone de cadeado
        print("\nProcurando por possíveis ícones de cadeado...")
        icon_elements = soup.find_all(['i', 'span', 'div'], class_=re.compile(r'icon|lock|cadeado|fa-lock'))
        
        if icon_elements:
            print("Possíveis ícones de cadeado encontrados:")
            for icon in icon_elements:
                print(f"- Classe: {icon.get('class')}, Texto: {icon.get_text().strip()}")
                
                # Verificar se o ícone está dentro de um link
                parent_link = icon.find_parent('a')
                if parent_link and parent_link.has_attr('href'):
                    print(f"  Link associado: {parent_link.get('href')}")
        
        # Procurar por elementos relacionados a faturas
        print("\nProcurando por elementos relacionados a faturas...")
        fatura_elements = soup.find_all(string=lambda text: 'fatura' in text.lower() if text else False)
        
        if fatura_elements:
            print("Elementos relacionados a faturas encontrados:")
            for element in fatura_elements:
                parent = element.parent
                print(f"- Texto: {element}")
                
                # Verificar se está dentro de um link
                parent_link = parent.find_parent('a')
                if parent_link and parent_link.has_attr('href'):
                    print(f"  Link associado: {parent_link.get('href')}")
        
        # Tentar encontrar informações sobre a fatura específica
        print("\nProcurando por informações sobre a fatura 4313...")
        fatura_4313 = soup.find(string=lambda text: '4313' in text if text else False)
        
        if fatura_4313:
            print(f"Menção à fatura 4313 encontrada: {fatura_4313}")
            parent = fatura_4313.parent
            print(f"Contexto: {parent.get_text().strip()}")
        else:
            print("Nenhuma menção específica à fatura 4313 encontrada na página inicial.")
            
        # Verificar se há alguma API ou endpoint para acesso a faturas
        print("\nVerificando possíveis endpoints de API...")
        scripts = soup.find_all('script')
        api_patterns = re.compile(r'(api|endpoint|fatura|invoice|bill).*?(url|endpoint|path)')
        
        for script in scripts:
            if script.string and api_patterns.search(script.string):
                print(f"Possível referência a API encontrada: {api_patterns.search(script.string).group(0)}")
                
        # Verificar se há alguma menção ao código ONS
        print("\nVerificando menções ao código ONS...")
        ons_elements = soup.find_all(string=lambda text: 'ons' in text.lower() if text else False)
        
        if ons_elements:
            print("Menções ao código ONS encontradas:")
            for element in ons_elements:
                parent = element.parent
                context = parent.get_text().strip()
                if len(context) > 200:
                    context = context[:200] + "..."
                print(f"- {context}")
        
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição HTTP: {str(e)}")
    except Exception as e:
        print(f"Ocorreu um erro durante a análise: {str(e)}")
    
    print("\nAnálise detalhada concluída!")

import requests
from bs4 import BeautifulSoup
import re
import os
import datetime
from urllib.parse import urljoin
import shutil

def baixar_fatura_mais_recente():
    # Caminho para salvar os arquivos
    pasta_destino = r"C:\Users\Bruno\Downloads\TUST\TECP"
    
    # Criar a pasta de destino se não existir
    os.makedirs(pasta_destino, exist_ok=True)
    
    # Headers para simular um navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://tecpenergia.com.br/',
    }
    
    # Criar uma sessão para manter cookies
    session = requests.Session()
    
    try:
        # Acessar o site principal para obter cookies
        print("Acessando o site da TECP Energia...")
        response = session.get("https://tecpenergia.com.br/", headers=headers)
        response.raise_for_status()
        
        # URL do endpoint de emissão de faturas
        fatura_url = "https://faturas.alupar.com.br:8090/Fatura/Emissao/56"
        
        # Dados do formulário
        form_data = {
            'Codigo': '4313',  # Código da fatura
            'btnEntrar': 'Entrar'
        }
        
        # Enviar requisição POST para o endpoint de faturas
        print(f"Acessando a área de faturas com o código 4313...")
        fatura_response = session.post(fatura_url, data=form_data, headers=headers)
        
        # Verificar se a requisição foi bem-sucedida
        if fatura_response.status_code == 200:
            print("Acesso bem-sucedido! Código de status: 200")
            
            # Analisar a resposta
            soup = BeautifulSoup(fatura_response.text, 'html.parser')
            
            # Encontrar a tabela de faturas
            tabelas = soup.find_all('table')
            if tabelas:
                print("\nTabela de faturas encontrada!")
                tabela = tabelas[0]
                
                # Extrair informações das faturas
                faturas = []
                rows = tabela.find_all('tr')
                
                # Pular a primeira linha (cabeçalho)
                for i, row in enumerate(rows[1:], 1):
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 8:  # Verificar se há células suficientes
                        empresa = cells[1].get_text().strip()
                        codigo = cells[2].get_text().strip()
                        cliente = cells[3].get_text().strip()
                        cnpj = cells[4].get_text().strip()
                        num_documento = cells[5].get_text().strip()
                        
                        # Extrair e converter a data de emissão
                        data_emissao_str = cells[6].get_text().strip()
                        try:
                            # Converter string de data para objeto datetime
                            data_emissao = datetime.datetime.strptime(data_emissao_str, "%d/%m/%Y")
                        except ValueError:
                            # Se não conseguir converter, usar uma data antiga
                            data_emissao = datetime.datetime(1900, 1, 1)
                        
                        valor = cells[7].get_text().strip()
                        
                        # Encontrar links na coluna de ação
                        links = cells[8].find_all('a', href=True)
                        
                        fatura_info = {
                            'empresa': empresa,
                            'codigo': codigo,
                            'cliente': cliente,
                            'cnpj': cnpj,
                            'num_documento': num_documento,
                            'data_emissao': data_emissao,
                            'data_emissao_str': data_emissao_str,
                            'valor': valor,
                            'links': []
                        }
                        
                        # Extrair informações dos links
                        for link in links:
                            href = link.get('href')
                            onclick = link.get('onclick', '')
                            title = link.get('title', '')
                            
                            fatura_info['links'].append({
                                'href': href,
                                'onclick': onclick,
                                'title': title
                            })
                        
                        faturas.append(fatura_info)
                
                if faturas:
                    # Ordenar faturas por data de emissão (mais recente primeiro)
                    faturas.sort(key=lambda x: x['data_emissao'], reverse=True)
                    
                    # Pegar a fatura mais recente
                    fatura_recente = faturas[0]
                    
                    print(f"\nFatura mais recente encontrada:")
                    print(f"- Empresa: {fatura_recente['empresa']}")
                    print(f"- Código ONS: {fatura_recente['codigo']}")
                    print(f"- Cliente: {fatura_recente['cliente']}")
                    print(f"- CNPJ: {fatura_recente['cnpj']}")
                    print(f"- Nº Documento: {fatura_recente['num_documento']}")
                    print(f"- Data de Emissão: {fatura_recente['data_emissao_str']}")
                    print(f"- Valor: {fatura_recente['valor']}")
                    
                    # Criar nome de arquivo baseado na data e número do documento
                    mes_ano = fatura_recente['data_emissao'].strftime("%m%Y")
                    base_filename = f"TECP_4313_{mes_ano}"
                    
                    # Baixar os arquivos da fatura mais recente
                    print("\nBaixando arquivos da fatura mais recente...")
                    
                    # Contador de arquivos baixados
                    arquivos_baixados = 0
                    
                    # Processar cada link da fatura
                    for link in fatura_recente['links']:
                        onclick = link['onclick']
                        title = link['title']
                        
                        # Extrair URL do onclick
                        url_match = re.search(r"window\.open\('([^']+)'", onclick)
                        if url_match:
                            url_path = url_match.group(1)
                            url_completa = urljoin("https://faturas.alupar.com.br:8090", url_path)
                            
                            print(f"Baixando {title} de: {url_completa}")
                            
                            try:
                                # Fazer requisição para baixar o arquivo
                                download_response = session.get(url_completa, headers=headers)
                                
                                if download_response.status_code == 200:
                                    # Determinar extensão do arquivo baseado no título
                                    if "XML" in title:
                                        extension = ".xml"
                                    elif "DANFE" in title or "NF" in title:
                                        extension = ".pdf"
                                    else:
                                        # Verificar pelo Content-Type
                                        content_type = download_response.headers.get('Content-Type', '')
                                        if 'xml' in content_type.lower():
                                            extension = ".xml"
                                        elif 'pdf' in content_type.lower():
                                            extension = ".pdf"
                                        else:
                                            extension = ".bin"
                                    
                                    # Nome do arquivo final
                                    filename = f"{base_filename}_{title.replace(' ', '_')}{extension}"
                                    filepath = os.path.join(pasta_destino, filename)
                                    
                                    # Salvar o arquivo
                                    with open(filepath, "wb") as f:
                                        f.write(download_response.content)
                                    
                                    print(f"Arquivo salvo como: {filepath}")
                                    arquivos_baixados += 1
                                else:
                                    print(f"Falha ao baixar {title}. Status: {download_response.status_code}")
                            except Exception as e:
                                print(f"Erro ao baixar {title}: {str(e)}")
                    
                    # Tentar exportar para Excel
                    print("\nTentando exportar para Excel...")
                    excel_url = "https://faturas.alupar.com.br:8090/Fatura/ExportarExcel/56"
                    
                    try:
                        excel_response = session.get(excel_url, headers=headers)
                        
                        if excel_response.status_code == 200:
                            # Verificar o tipo de conteúdo
                            content_type = excel_response.headers.get('Content-Type', '')
                            
                            # Se for um arquivo Excel
                            if 'application/vnd.ms-excel' in content_type.lower() or 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in content_type.lower():
                                extension = '.xlsx' if 'openxmlformats' in content_type.lower() else '.xls'
                                excel_filename = f"{base_filename}_relatorio{extension}"
                                excel_filepath = os.path.join(pasta_destino, excel_filename)
                                
                                # Salvar o arquivo
                                with open(excel_filepath, "wb") as f:
                                    f.write(excel_response.content)
                                print(f"Arquivo Excel salvo como: {excel_filepath}")
                                arquivos_baixados += 1
                            else:
                                print(f"A resposta não é um arquivo Excel. Content-Type: {content_type}")
                    except Exception as e:
                        print(f"Erro ao exportar para Excel: {str(e)}")
                    
                    print(f"\nTotal de arquivos baixados: {arquivos_baixados}")
                    
                    if arquivos_baixados > 0:
                        print(f"\nTodos os arquivos foram salvos em: {pasta_destino}")
                        return True
                    else:
                        print("\nNenhum arquivo foi baixado.")
                        return False
                else:
                    print("Nenhuma fatura encontrada.")
                    return False
            else:
                print("Nenhuma tabela de faturas encontrada na resposta.")
                return False
        else:
            print(f"Falha na requisição. Código de status: {fatura_response.status_code}")
            return False
        
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição HTTP: {str(e)}")
        return False
    except Exception as e:
        print(f"Ocorreu um erro durante o acesso: {str(e)}")
        return False
    
    print("\nProcesso de download de faturas concluído!")
    return True

if __name__ == "__main__":
    baixar_fatura_mais_recente()

def baixar_fatura_empresa(empresa, pasta_base):
    """Baixa a fatura mais recente para uma empresa específica"""
    codigo_ons = empresa["codigo"]
    nome_empresa = empresa["nome"]
    
    # Criar pasta específica para a empresa
    pasta_destino = os.path.join(pasta_base, nome_empresa)
    os.makedirs(pasta_destino, exist_ok=True)
    
    logger.info(f"Iniciando download para empresa {nome_empresa} (Código ONS: {codigo_ons})")
    
    # Headers para simular um navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://tecpenergia.com.br/',
    }
    
    # Criar uma sessão para manter cookies
    session = requests.Session()
    
    try:
        # Acessar o site principal para obter cookies
        response = session.get("https://tecpenergia.com.br/", headers=headers, timeout=30)
        response.raise_for_status()
        
        # URL do endpoint de emissão de faturas
        fatura_url = "https://faturas.alupar.com.br:8090/Fatura/Emissao/56"
        
        # Dados do formulário
        form_data = {
            'Codigo': codigo_ons,
            'btnEntrar': 'Entrar'
        }
        
        # Enviar requisição POST para o endpoint de faturas
        logger.info(f"Acessando a área de faturas com o código {codigo_ons}...")
        fatura_response = session.post(fatura_url, data=form_data, headers=headers, timeout=30)
        
        # Verificar se a requisição foi bem-sucedida
        if fatura_response.status_code == 200:
            logger.info(f"Acesso bem-sucedido para {nome_empresa}!")
            
            # Analisar a resposta
            soup = BeautifulSoup(fatura_response.text, 'html.parser')
            
            # Encontrar a tabela de faturas
            tabelas = soup.find_all('table')
            if not tabelas:
                logger.warning(f"Nenhuma tabela de faturas encontrada para {nome_empresa}")
                return False
                
            tabela = tabelas[0]
            
            # Extrair informações das faturas
            faturas = []
            rows = tabela.find_all('tr')
            
            # Pular a primeira linha (cabeçalho)
            for row in rows[1:]:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 8:  # Verificar se há células suficientes
                    empresa_nome = cells[1].get_text().strip()
                    codigo = cells[2].get_text().strip()
                    cliente = cells[3].get_text().strip()
                    cnpj = cells[4].get_text().strip()
                    num_documento = cells[5].get_text().strip()
                    
                    # Extrair e converter a data de emissão
                    data_emissao_str = cells[6].get_text().strip()
                    try:
                        # Converter string de data para objeto datetime
                        data_emissao = datetime.datetime.strptime(data_emissao_str, "%d/%m/%Y")
                    except ValueError:
                        # Se não conseguir converter, usar uma data antiga
                        data_emissao = datetime.datetime(1900, 1, 1)
                        logger.warning(f"Erro ao converter data '{data_emissao_str}' para {nome_empresa}")
                    
                    valor = cells[7].get_text().strip()
                    
                    # Encontrar links na coluna de ação
                    links = cells[8].find_all('a', href=True)
                    
                    fatura_info = {
                        'empresa': empresa_nome,
                        'codigo': codigo,
                        'cliente': cliente,
                        'cnpj': cnpj,
                        'num_documento': num_documento,
                        'data_emissao': data_emissao,
                        'data_emissao_str': data_emissao_str,
                        'valor': valor,
                        'links': []
                    }
                    
                    # Extrair informações dos links
                    for link in links:
                        href = link.get('href')
                        onclick = link.get('onclick', '')
                        title = link.get('title', '')
                        
                        fatura_info['links'].append({
                            'href': href,
                            'onclick': onclick,
                            'title': title
                        })
                    
                    faturas.append(fatura_info)
            
            if not faturas:
                logger.warning(f"Nenhuma fatura encontrada para {nome_empresa}")
                return False
                
            # Ordenar faturas por data de emissão (mais recente primeiro)
            faturas.sort(key=lambda x: x['data_emissao'], reverse=True)
            
            # Pegar a fatura mais recente
            fatura_recente = faturas[0]
            
            logger.info(f"Fatura mais recente para {nome_empresa}:")
            logger.info(f"- Nº Documento: {fatura_recente['num_documento']}")
            logger.info(f"- Data de Emissão: {fatura_recente['data_emissao_str']}")
            logger.info(f"- Valor: {fatura_recente['valor']}")
            
            # Criar nome de arquivo baseado na data e número do documento
            mes_ano = fatura_recente['data_emissao'].strftime("%m%Y")
            base_filename = f"{nome_empresa}_{codigo_ons}_{mes_ano}"
            
            # Baixar os arquivos da fatura mais recente
            logger.info(f"Baixando arquivos da fatura mais recente para {nome_empresa}...")
            
            # Contador de arquivos baixados
            arquivos_baixados = 0
            
            # Processar cada link da fatura
            for link in fatura_recente['links']:
                onclick = link['onclick']
                title = link['title']
                
                # Extrair URL do onclick
                url_match = re.search(r"window\.open\('([^']+)'", onclick)
                if url_match:
                    url_path = url_match.group(1)
                    url_completa = urljoin("https://faturas.alupar.com.br:8090", url_path)
                    
                    logger.info(f"Baixando {title} de: {url_completa}")
                    
                    try:
                        # Fazer requisição para baixar o arquivo
                        download_response = session.get(url_completa, headers=headers, timeout=30)
                        
                        if download_response.status_code == 200:
                            # Determinar extensão do arquivo baseado no título
                            if "XML" in title:
                                extension = ".xml"
                            elif "DANFE" in title or "NF" in title:
                                extension = ".pdf"
                            else:
                                # Verificar pelo Content-Type
                                content_type = download_response.headers.get('Content-Type', '')
                                if 'xml' in content_type.lower():
                                    extension = ".xml"
                                elif 'pdf' in content_type.lower():
                                    extension = ".pdf"
                                else:
                                    extension = ".bin"
                            
                            # Nome do arquivo final
                            filename = f"{base_filename}_{title.replace(' ', '_')}{extension}"
                            filepath = os.path.join(pasta_destino, filename)
                            
                            # Salvar o arquivo
                            with open(filepath, "wb") as f:
                                f.write(download_response.content)
                            
                            logger.info(f"Arquivo salvo como: {filepath}")
                            arquivos_baixados += 1
                        else:
                            logger.warning(f"Falha ao baixar {title} para {nome_empresa}. Status: {download_response.status_code}")
                    except Exception as e:
                        logger.error(f"Erro ao baixar {title} para {nome_empresa}: {str(e)}")
            
            # Tentar exportar para Excel
            logger.info(f"Tentando exportar relatório Excel para {nome_empresa}...")
            excel_url = "https://faturas.alupar.com.br:8090/Fatura/ExportarExcel/56"
            
            try:
                excel_response = session.get(excel_url, headers=headers, timeout=30)
                
                if excel_response.status_code == 200:
                    # Verificar o tipo de conteúdo
                    content_type = excel_response.headers.get('Content-Type', '')
                    
                    # Se for um arquivo Excel
                    if 'application/vnd.ms-excel' in content_type.lower() or 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in content_type.lower():
                        extension = '.xlsx' if 'openxmlformats' in content_type.lower() else '.xls'
                        excel_filename = f"{base_filename}_relatorio{extension}"
                        excel_filepath = os.path.join(pasta_destino, excel_filename)
                        
                        # Salvar o arquivo
                        with open(excel_filepath, "wb") as f:
                            f.write(excel_response.content)
                        logger.info(f"Arquivo Excel salvo como: {excel_filepath}")
                        arquivos_baixados += 1
                    else:
                        logger.warning(f"A resposta não é um arquivo Excel para {nome_empresa}. Content-Type: {content_type}")
            except Exception as e:
                logger.error(f"Erro ao exportar Excel para {nome_empresa}: {str(e)}")
            
            logger.info(f"Total de arquivos baixados para {nome_empresa}: {arquivos_baixados}")
            
            if arquivos_baixados > 0:
                logger.info(f"Todos os arquivos para {nome_empresa} foram salvos em: {pasta_destino}")
                return True
            else:
                logger.warning(f"Nenhum arquivo foi baixado para {nome_empresa}.")
                return False
        else:
            logger.error(f"Falha na requisição para {nome_empresa}. Código de status: {fatura_response.status_code}")
            return False
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na requisição HTTP para {nome_empresa}: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Ocorreu um erro durante o acesso para {nome_empresa}: {str(e)}")
        return False

def baixar_todas_faturas():
    """Baixa as faturas mais recentes para todas as empresas"""
    # Caminho base para salvar os arquivos
    pasta_base = r"C:\Users\Bruno\Downloads\TUST\TECP"
    
    # Criar a pasta base se não existir
    os.makedirs(pasta_base, exist_ok=True)
    
    logger.info(f"Iniciando download de faturas para {len(EMPRESAS)} empresas")
    logger.info(f"Arquivos serão salvos em: {pasta_base}")
    
    # Contador de sucessos e falhas
    sucessos = 0
    falhas = 0
    
    # Lista para armazenar resultados
    resultados = []
    
    # Usar ThreadPoolExecutor para processar múltiplas empresas em paralelo
    # Reduzir para 2 workers para evitar sobrecarga no servidor
    with ThreadPoolExecutor(max_workers=2) as executor:
        # Submeter tarefas para cada empresa
        future_to_empresa = {executor.submit(baixar_fatura_empresa, empresa, pasta_base): empresa for empresa in EMPRESAS}
        
        # Processar resultados à medida que são concluídos
        for future in as_completed(future_to_empresa):
            empresa = future_to_empresa[future]
            try:
                resultado = future.result()
                if resultado:
                    sucessos += 1
                    resultados.append({"empresa": empresa["nome"], "codigo": empresa["codigo"], "status": "Sucesso"})
                else:
                    # Tentar novamente uma vez em caso de falha
                    logger.warning(f"Primeira tentativa falhou para {empresa['nome']}. Tentando novamente...")
                    time.sleep(5)  # Esperar 5 segundos antes de tentar novamente
                    
                    # Segunda tentativa
                    resultado = baixar_fatura_empresa(empresa, pasta_base)
                    if resultado:
                        sucessos += 1
                        resultados.append({"empresa": empresa["nome"], "codigo": empresa["codigo"], "status": "Sucesso (segunda tentativa)"})
                    else:
                        falhas += 1
                        resultados.append({"empresa": empresa["nome"], "codigo": empresa["codigo"], "status": "Falha após retry"})
            except Exception as e:
                logger.error(f"Erro ao processar empresa {empresa['nome']}: {str(e)}")
                falhas += 1
                resultados.append({"empresa": empresa["nome"], "codigo": empresa["codigo"], "status": f"Erro: {str(e)}"})
    
    # Gerar relatório de resultados
    logger.info("\n" + "="*50)
    logger.info("RELATÓRIO DE DOWNLOAD DE FATURAS")
    logger.info("="*50)
    logger.info(f"Total de empresas processadas: {len(EMPRESAS)}")
    logger.info(f"Downloads com sucesso: {sucessos}")
    logger.info(f"Downloads com falha: {falhas}")
    logger.info("="*50)
    logger.info("Detalhes por empresa:")
    
    for resultado in resultados:
        logger.info(f"- {resultado['empresa']} (Código: {resultado['codigo']}): {resultado['status']}")
    
    logger.info("="*50)
    
    # Salvar relatório em arquivo de texto
    relatorio_path = os.path.join(pasta_base, f"relatorio_download_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    with open(relatorio_path, "w", encoding="utf-8") as f:
        f.write("="*50 + "\n")
        f.write("RELATÓRIO DE DOWNLOAD DE FATURAS\n")
        f.write("="*50 + "\n")
        f.write(f"Data e hora: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"Total de empresas processadas: {len(EMPRESAS)}\n")
        f.write(f"Downloads com sucesso: {sucessos}\n")
        f.write(f"Downloads com falha: {falhas}\n")
        f.write("="*50 + "\n")
        f.write("Detalhes por empresa:\n")
        
        for resultado in resultados:
            f.write(f"- {resultado['empresa']} (Código: {resultado['codigo']}): {resultado['status']}\n")
        
        f.write("="*50 + "\n")
    
    logger.info(f"Relatório salvo em: {relatorio_path}")
    
    return sucessos, falhas, relatorio_path

if __name__ == "__main__":
    start_time = time.time()
    sucessos, falhas, relatorio_path = baixar_todas_faturas()
    end_time = time.time()
    
    tempo_total = end_time - start_time
    logger.info(f"Processo concluído em {tempo_total:.2f} segundos")
    
    if falhas == 0:
        logger.info("Todas as faturas foram baixadas com sucesso!")
    else:
        logger.warning(f"Processo concluído com {falhas} falhas. Verifique o relatório para detalhes.")
