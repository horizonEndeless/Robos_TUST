import requests
import json
import os
import shutil
from urllib.parse import urlparse
from pathlib import Path

# URL da API
url = "https://ms-site.cap-tropicalia.cust.app.br/site/usuaria"

# Headers da requisição
headers = {
    "accept": "*/*",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "access-control-allow-origin": "*",
    "content-type": "application/json",
    "origin": "https://nf-tropicalia-transmissora.cust.app.br",
    "referer": "https://nf-tropicalia-transmissora.cust.app.br/",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

# Diretório de download
download_dir = Path(r"C:\Users\Bruno\Downloads\TUST\TROPICALIA")

# Pasta Rio Energy
re_dir = download_dir / "RE"

# Pasta AE
ae_dir = download_dir / "AE"

# Pasta DE
de_dir = download_dir / "DE"

# Dicionário de empresas
empresas = {
    "RE": {
        "3947": "SDBA", "3948": "SDBB", "3969": "SDBC", "3970": "SDBD", "3972": "SDBF",
        "3976": "SDBE", "4316": "CECF", "3430": "CECA", "3431": "CECB", "3432": "CECC",
        "4315": "CECE", "4415": "CECD", "3497": "ITA2", "3498": "ITA5", "3502": "ITA1",
        "3503": "ITA3", "3530": "ITA4", "3531": "ITA6", "3532": "ITA7", "3537": "ITA8",
        "3538": "ITA9", "4314": "BRJB", "4313": "BRJA"
    },
    "AE": {
        "3859": "SJP I", "3860": "SJP II", "3861": "SJP III", "3862": "SJP IV",
        "3863": "SJP V", "3864": "SJP VI", "8011": "LIBRA", "3740": "COREMA I",
        "3741": "COREMA II", "3750": "COREMA III"
    },
    "DE": {
        "3748": "DIAMANTE"
    }

}

# Função para baixar um arquivo
def download_file(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Arquivo baixado: {filename}")
    else:
        print(f"Erro ao baixar {filename}: {response.status_code}")

# Função para processar uma empresa
def processar_empresa(numero_ons, nome_pasta, pasta_principal):
    params = {"numeroOns": numero_ons}
    empresa_dir = pasta_principal / nome_pasta
    empresa_dir.mkdir(exist_ok=True)

    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nProcessando empresa: {nome_pasta}")
        
        for item in data:
            if item['periodoContabil'] == "NOVEMBRO-2024":
                periodo = item['periodoContabil'].replace('/', '-')
                
                # Baixando DANFE
                danfe_url = item['linkDanfe']
                danfe_filename = empresa_dir / f"DANFE_{periodo}.pdf"
                download_file(danfe_url, danfe_filename)
                
                # Baixando XML
                xml_url = item['linkXml']
                xml_filename = empresa_dir / f"XML_{periodo}.xml"
                download_file(xml_url, xml_filename)
                
                # Baixando Boleto
                boleto_url = item['linkBoleto']
                boleto_filename = empresa_dir / f"BOLETO_{periodo}.pdf"
                download_file(boleto_url, boleto_filename)
                
                print(f"Arquivos baixados para {nome_pasta} - {periodo}")
                return True
        
        print(f"Não foram encontrados dados para agosto de 2024 para {nome_pasta}")
        return False
    else:
        print(f"Erro na requisição para {nome_pasta}: {response.status_code}")
        return False

try:
    # Criando o diretório principal se não existir
    download_dir.mkdir(parents=True, exist_ok=True)

    # Criando as pastas RE, AE e DE
    re_dir.mkdir(exist_ok=True)
    ae_dir.mkdir(exist_ok=True)
    de_dir.mkdir(exist_ok=True)

    # Processando cada empresa
    for grupo, grupo_empresas in empresas.items():
        if grupo == "RE":
            pasta_principal = re_dir
        elif grupo == "AE":
            pasta_principal = ae_dir
        else:  # grupo == "DE"
            pasta_principal = de_dir
        
        for numero_ons, nome_pasta in grupo_empresas.items():
            processar_empresa(numero_ons, nome_pasta, pasta_principal)

except Exception as e:
    print(f"Ocorreu um erro: {str(e)}")
