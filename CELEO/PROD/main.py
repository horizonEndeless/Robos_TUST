import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import requests
from bs4 import BeautifulSoup
import os
import pdfkit
import tempfile
import xml.etree.ElementTree as ET
from datetime import datetime

URL_DEFAULT = "https://boleto.celeoredes.com.br"
URL_FATURAS = "https://boleto.celeoredes.com.br/read.asp"
POST_FATURAS = "txtNordem={0}"
POST_FATURASPERIODO = "txtNordem={0}&txtPeriodo={1}"

def get_transmissora_code(xml_content):
    try:
        # Parse o XML
        root = ET.fromstring(xml_content)
        
        # Encontra o namespace
        ns = {'nfe': root.tag.split('}')[0].strip('{')}
        
        # Busca o CNPJ e xFant da transmissora
        cnpj = root.find('.//nfe:emit/nfe:CNPJ', ns).text if root.find('.//nfe:emit/nfe:CNPJ', ns) is not None else ''
        xfant = root.find('.//nfe:emit/nfe:xFant', ns).text if root.find('.//nfe:emit/nfe:xFant', ns) is not None else ''
        xnome = root.find('.//nfe:emit/nfe:xNome', ns).text if root.find('.//nfe:emit/nfe:xNome', ns) is not None else ''
        
        # Mapeamento de CNPJs para códigos de transmissora
        cnpj_mapping = {
            '14832534000199': '1137',  # CAIUA/CATE
            # Adicione outros CNPJs conforme necessário
        }
        
        # Primeiro tenta pelo CNPJ
        if cnpj in cnpj_mapping:
            return cnpj_mapping[cnpj]
        
        # Se não encontrou pelo CNPJ, tenta pelo xFant
        transmissora = xfant.split('-')[0] if '-' in xfant else xfant
        
        # Mapeamento de transmissoras
        transmissoras = {
            "PTE": "1078",
            "CTE": "1068",
            "ENTE": "1101",
            "LTC": "1127",
            "IMTE": "1149",
            "CATE": "1137",
            "CANTE": "1198",
            "JTE": "1065",
            "VCTE": "1041",
            "LTT": "1058",
            "CPTE": "1031",
            "SITE": "1236",
            "BTE": "1082",
            "PATE": "1318",
            "CAIUA": "1137"  # Adicionando CAIUA como alternativa para CATE
        }
        
        # Se não encontrar pelo xFant, procura no nome completo
        if transmissora not in transmissoras and "CAIUA" in xnome:
            return "1137"
        
        return transmissoras.get(transmissora)
    except Exception as e:
        print(f"Erro ao processar XML: {e}")
        return None

def download_file(url, filename):
    print(f"Tentando baixar arquivo de {url} para {filename}")
    response = requests.get(url, verify=False)
    if response.ok:
        # Primeiro baixa o conteúdo
        content = response.content
        
        # Se for um XML, identifica a transmissora
        if filename.endswith('.xml'):
            try:
                transmissora_code = get_transmissora_code(content)
                if transmissora_code:
                    # Cria o novo caminho baseado na transmissora
                    base_dir = os.path.dirname(filename)
                    new_base_dir = os.path.join(base_dir, transmissora_code)
                    os.makedirs(new_base_dir, exist_ok=True)
                    
                    # Atualiza o nome do arquivo para incluir a pasta da transmissora
                    filename = os.path.join(new_base_dir, os.path.basename(filename))
            except Exception as e:
                print(f"Erro ao processar transmissora do XML: {e}")
        
        # Salva o arquivo no local correto
        with open(filename, 'wb') as file:
            file.write(content)
        print(f"Arquivo {filename} baixado com sucesso")
        
        return filename  # Retorna o nome do arquivo possivelmente modificado
    else:
        print(f"Erro ao baixar {filename} de {url}. Status: {response.status_code}")
        return None

def baixar_faturas(codigo_ons, empresa="AE"):
    print(f"Iniciando busca de faturas para o código ONS: {codigo_ons} - Empresa: {empresa}")
    
    # Adiciona código para obter o mês atual
    mes_atual = datetime.now().month
    
    # Cria o caminho base de acordo com a empresa (AE ou RE)
    caminho_base = os.path.join(r"C:\Users\Bruno\Downloads\TUST\CELEO", empresa, codigo_ons)
    os.makedirs(caminho_base, exist_ok=True)
    
    # Faz a requisição GET para a URL padrão
    response_default = requests.get(URL_DEFAULT, verify=False)
    print(f"Status da requisição inicial: {response_default.status_code}")
    
    if response_default.ok:
        # Prepara os dados para o POST incluindo o período
        post_data = {
            'txtNordem': codigo_ons,
            'txtPeriodo': str(mes_atual)  # Adiciona o mês atual
        }
        print(f"Dados do POST: {post_data}")
        
        # Adiciona headers mais completos
        headers = {
            'Referer': URL_DEFAULT,
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Faz a requisição POST para obter as faturas
        response_faturas = requests.post(
            URL_FATURAS, 
            data=post_data, 
            headers=headers, 
            verify=False
        )
        print(f"Status da requisição de faturas: {response_faturas.status_code}")
        print(f"Conteúdo da resposta: {response_faturas.text[:500]}")  # Primeiros 500 caracteres
        
        if response_faturas.ok:
            # Analisa o HTML retornado
            soup = BeautifulSoup(response_faturas.text, 'html.parser')
            rows = soup.select("table tr")
            print(f"Número de linhas encontradas na tabela: {len(rows)}")
            
            if rows:
                for row in rows[1:]:  # Ignora o cabeçalho
                    columns = row.find_all("td")
                    print(f"Número de colunas encontradas: {len(columns)}")
                    
                    if len(columns) >= 10:
                        try:
                            # Extrai os links para XML, DANFE e Boleto
                            link_xml = columns[4].find('a')['href']
                            link_danfe = columns[5].find('a')['href']
                            link_boleto = columns[6].find('a')['href'] if columns[6].find('a') else None
                            
                            print(f"Link XML: {link_xml}")
                            print(f"Link DANFE: {link_danfe}")
                            print(f"Link Boleto: {link_boleto}")
                            
                            # Corrige o formato dos links
                            link_xml = link_xml.replace('\\', '/')
                            link_danfe = link_danfe.replace('\\', '/')
                            
                            # Corrige o protocolo do link do boleto
                            if link_boleto:
                                link_boleto = link_boleto.replace('http://', 'https://')
                            
                            # Extrai os nomes dos arquivos dos links
                            nome_arquivo_xml = link_xml.split('/')[-1]
                            nome_arquivo_danfe = link_danfe.split('/')[-1]
                            
                            # Define o caminho de salvamento
                            caminho_base = os.path.join(r"C:\Users\Bruno\Downloads\TUST\CELEO", empresa, codigo_ons)
                            os.makedirs(caminho_base, exist_ok=True)
                            
                            # Baixa e salva o XML
                            if link_xml:
                                url_xml = f"{URL_DEFAULT}/{link_xml}"
                                caminho_xml = os.path.join(caminho_base, nome_arquivo_xml)
                                novo_caminho_xml = download_file(url_xml, caminho_xml)
                                
                                if novo_caminho_xml and link_danfe:
                                    # Usa o mesmo diretório do XML para o DANFE
                                    dir_transmissora = os.path.dirname(novo_caminho_xml)
                                    caminho_danfe = os.path.join(dir_transmissora, nome_arquivo_danfe)
                                    url_danfe = f"{URL_DEFAULT}/{link_danfe}"
                                    download_file(url_danfe, caminho_danfe)
                                    
                                    # Se tiver boleto, usa o mesmo diretório
                                    if link_boleto:
                                        nome_arquivo_boleto = nome_arquivo_danfe.replace('.pdf', '_boleto.pdf')
                                        caminho_boleto = os.path.join(dir_transmissora, nome_arquivo_boleto)
                                        download_boleto_as_pdf(link_boleto, caminho_boleto)
                                
                        except Exception as e:
                            print(f"Erro ao processar linha: {e}")
            else:
                print("Nenhuma linha encontrada na tabela")
        else:
            print("Falha ao obter faturas")
    else:
        print("Falha na requisição inicial")

def download_boleto_as_pdf(url, filename):
    print(f"Tentando baixar e converter boleto de {url} para {filename}")
    try:
        config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        
        # Opções otimizadas para garantir que o boleto seja exibido completamente
        options = {
            'page-size': 'A4',
            'encoding': 'utf-8',
            'custom-header': [
                ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0')
            ],
            'javascript-delay': 1000,
            'no-images': False,
            'enable-local-file-access': None,
            'print-media-type': True,
            'margin-top': '5mm',      # Reduzidas as margens
            'margin-right': '5mm',    # para maximizar área útil
            'margin-bottom': '5mm',
            'margin-left': '5mm',
            'orientation': 'Portrait',
            'dpi': 300,
            'zoom': 0.85,            # Zoom reduzido para garantir que todo conteúdo seja visível
            'disable-smart-shrinking': False  # Permite que o wkhtmltopdf ajuste o conteúdo
        }
        
        # Baixa o conteúdo HTML com headers específicos
        response = requests.get(url, verify=False, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Charset': 'utf-8',
            'Connection': 'keep-alive'
        })
        
        if response.ok:
            # Força UTF-8 e trata caracteres especiais
            response.encoding = 'utf-8'
            html_content = response.text
            
            # Adiciona meta tag para forçar encoding
            if '<head>' in html_content:
                html_content = html_content.replace('<head>', 
                    '<head><meta charset="utf-8"/>')
            
            # Salva em arquivo temporário
            with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as f:
                f.write(html_content)
                temp_path = f.name
            
            # Converte para PDF
            pdfkit.from_file(temp_path, filename, configuration=config, options=options)
            os.unlink(temp_path)
            
            print(f"Boleto convertido e salvo com sucesso em {filename}")
        else:
            print(f"Erro ao baixar boleto. Status: {response.status_code}")
    except Exception as e:
        print(f"Erro ao converter boleto para PDF: {e}")

if __name__ == "__main__":
    # Dicionário com códigos e nomes das subestações da AE
    codigos_ae = {
        "3859": "SJP1",
        "3860": "SJP2",
        "3861": "SJP3",
        "3862": "SJP4",
        "3863": "SJP5",
        "3864": "SJP6",
        "3740": "COR1",
        "3741": "COR2",
        "3750": "COR3",
        "8011": "LIBRA"
    }
    
    # Dicionário com códigos e nomes das subestações da RE
    codigos_re = {
        "4313": "BRJA",
        "4314": "BRJB",
        "3430": "CECA",
        "3431": "CECB",
        "3432": "CECC",
        "4415": "CECD",
        "4315": "CECE",
        "4316": "CECF",
        "3502": "ITA1",
        "3497": "ITA2",
        "3503": "ITA3",
        "3530": "ITA4",
        "3498": "ITA5",
        "3531": "ITA6",
        "3532": "ITA7",
        "3537": "ITA8",
        "3538": "ITA9",
        "3947": "SDBA",
        "3948": "SDBB",
        "3969": "SDBC",
        "3970": "SDBD",
        "3976": "SDBE",
        "3972": "SDBF"
    }
    
    # Dicionário com código da DE
    codigos_de = {
        "3748": "DE"
    }
    
    # Processa as subestações da AE
    print("\n=== Processando subestações AE ===")
    for codigo, nome in codigos_ae.items():
        print(f"\nBaixando faturas para AE - {nome} (Código ONS: {codigo})")
        baixar_faturas(codigo, "AE")
    
    # Processa as subestações da RE
    print("\n=== Processando subestações RE ===")
    for codigo, nome in codigos_re.items():
        print(f"\nBaixando faturas para RE - {nome} (Código ONS: {codigo})")
        baixar_faturas(codigo, "RE")
    
    # Processa a subestação da DE
    print("\n=== Processando subestação DE ===")
    for codigo, nome in codigos_de.items():
        print(f"\nBaixando faturas para DE - {nome} (Código ONS: {codigo})")
        baixar_faturas(codigo, "DE")
