import requests
import json
from bs4 import BeautifulSoup
import os
from pathlib import Path

# Definição dos códigos ONS por tipo
CODIGOS_ONS = {
    'RE': [
        '4313', '4314', '3430', '3431', '3432', '4415', '4315', '4316',
        '3502', '3497', '3503', '3530', '3498', '3531', '3532', '3537',
        '3538', '3947', '3948', '3969', '3970', '3976', '3972'
    ],
    'AE': [
        '3859', '3860', '3861', '3862', '3863', '3864',
        '3740', '3741', '3750', '8011'
    ],
    'DE': ['3748']
}

def get_transmissora_data(agent_code):
    base_url = 'https://sys.sigetplus.com.br'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    
    endpoint = f'/cobranca/transmitter/1307/invoices'
    params = {'agent': agent_code}

    try:
        response = requests.get(
            f'{base_url}{endpoint}',
            headers=headers,
            params=params
        )
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer a requisição para o código {agent_code}: {e}")
        return None

def download_xml(xml_url, save_path):
    try:
        response = requests.get(xml_url)
        response.raise_for_status()
        
        os.makedirs(save_path, exist_ok=True)
        
        file_name = xml_url.split('/')[-1]
        full_path = os.path.join(save_path, file_name)
        
        with open(full_path, 'wb') as f:
            f.write(response.content)
            
        print(f"XML baixado com sucesso: {full_path}")
        return True
    except Exception as e:
        print(f"Erro ao baixar o XML: {e}")
        return False

def extract_xml_url(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        xml_link = soup.find('a', {'data-original-title': 'XML'})
        
        if xml_link and 'href' in xml_link.attrs:
            return xml_link['href']
        else:
            print("Link do XML não encontrado na página")
            return None
    except Exception as e:
        print(f"Erro ao extrair URL do XML: {e}")
        return None

def get_tipo_codigo(codigo):
    for tipo, codigos in CODIGOS_ONS.items():
        if codigo in codigos:
            return tipo
    return None

def process_agent(agent_code, base_path):
    print(f"\nProcessando código ONS: {agent_code}")
    
    # Determina o tipo (RE, AE, DE) baseado no código
    tipo = get_tipo_codigo(agent_code)
    if not tipo:
        print(f"Tipo não encontrado para o código {agent_code}")
        return
    
    # Cria o caminho da pasta específica para este código
    save_path = os.path.join(base_path, tipo, agent_code, 'XML')
    
    # Obtém os dados da página
    data = get_transmissora_data(agent_code)
    
    if data:
        # Extrai a URL do XML
        xml_url = extract_xml_url(data)
        
        if xml_url:
            # Faz o download do XML
            download_xml(xml_url, save_path)
        else:
            print(f"Não foi possível encontrar o URL do XML para o código {agent_code}")
    else:
        print(f"Não foi possível obter os dados da página para o código {agent_code}")

def main():
    # Diretório base
    base_path = r'C:\Users\Bruno\Downloads\TUST\ITAMARACA'
    
    # Processa todos os códigos
    for tipo, codigos in CODIGOS_ONS.items():
        print(f"\nProcessando {tipo}...")
        for codigo in codigos:
            process_agent(codigo, base_path)

if __name__ == "__main__":
    main()
