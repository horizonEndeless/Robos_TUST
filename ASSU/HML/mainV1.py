import requests
import json
from datetime import datetime
import os
from bs4 import BeautifulSoup
import re

# Dicionário com todas as ONS e suas respectivas empresas
ONS_EMPRESAS = {
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

def obter_dados_nota_recente(session, base_url, cod_ons, headers):
    """Obtém os dados da nota fiscal mais recente"""
    response = session.get(f"{base_url}/Home/Notas?iCodEmp=18&iCodOns={cod_ons}", headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Procura a tabela com classe 'tableGrid'
        tabela = soup.find('table', {'class': 'tableGrid'})
        if tabela:
            # Pega todas as linhas da tabela exceto o cabeçalho
            linhas = tabela.find_all('tr', {'class': 'dif'})
            if linhas:
                # A última linha é a nota mais recente
                ultima_linha = linhas[-1]
                dados = {}
                # Extrai os dados da linha
                colunas = ultima_linha.find_all('td')
                dados['numero_nf'] = colunas[0].text.strip()
                dados['data_emissao'] = colunas[1].text.strip()
                dados['valor'] = colunas[2].text.strip()
                dados['chave_nfe'] = colunas[3].text.strip()
                
                # Extrai a chave NFe do link do XML
                link_xml = ultima_linha.find('a', href=True, text='Xml')
                if link_xml:
                    href = link_xml['href']
                    chave = href.split('sChvDoe=')[1]
                    dados['chave_nfe'] = chave
                
                print(f"Dados da nota mais recente para ONS {cod_ons}:")
                print(json.dumps(dados, indent=2))
                return dados
    return None

def obter_dados_boleto_recente(session, base_url, cod_ons, headers):
    """Obtém os dados do boleto mais recente"""
    response = session.get(f"{base_url}/Home/Boletos?iCodEmp=18&iCodOns={cod_ons}", headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Procura a tabela com classe 'tableGrid'
        tabela = soup.find('table', {'class': 'tableGrid'})
        if tabela:
            # Pega a primeira linha após o cabeçalho (boleto mais recente)
            linha = tabela.find('tr', {'class': 'dif'})
            if linha:
                # Extrai todos os inputs hidden da linha
                inputs = linha.find_all('input', {'type': 'hidden'})
                dados = {}
                for input_field in inputs:
                    dados[input_field['name']] = input_field['value']
                
                print(f"Dados do boleto mais recente para ONS {cod_ons}:")
                print(json.dumps(dados, indent=2))
                return dados
    return None

def baixar_titulo_assu(cod_ons, empresa):
    print(f"\nProcessando ONS {cod_ons} - {empresa}")
    
    base_url = "https://faturamentoassu.cesbe.com.br"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "content-type": "application/x-www-form-urlencoded",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1"
    }

    session = requests.Session()
    response = session.post(f"{base_url}/", data={"CodOns": cod_ons, "CodEmp": "18"}, headers=headers)
    
    if response.status_code == 200:
        base_path = os.path.join(r"C:\Users\Bruno\Downloads\ASSU\RE", cod_ons)
        os.makedirs(base_path, exist_ok=True)

        # Obtém dados da nota fiscal mais recente
        dados_nota = obter_dados_nota_recente(session, base_url, cod_ons, headers)
        if dados_nota:
            # Download do XML
            params_xml = {
                "sCodEmp": "18",
                "sChvDoe": dados_nota['chave_nfe']
            }
            
            response_xml = session.get(
                f"{base_url}/Home/WsDownloadXml",
                params=params_xml,
                headers={**headers, "referer": f"{base_url}/Home/Notas?iCodEmp=18&iCodOns={cod_ons}"}
            )
            
            if response_xml.status_code == 200:
                xml_path = os.path.join(base_path, f"NFe_{empresa}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml")
                with open(xml_path, 'wb') as f:
                    f.write(response_xml.content)
                print(f"XML baixado com sucesso: {xml_path}")

            # Download da DANFE
            response_danfe = session.get(
                f"{base_url}/Home/WsDownloadDanfe",
                params=params_xml,  # Usa os mesmos parâmetros do XML
                headers={**headers, "referer": f"{base_url}/Home/Notas?iCodEmp=18&iCodOns={cod_ons}"}
            )
            
            if response_danfe.status_code == 200:
                danfe_path = os.path.join(base_path, f"DANFE_{empresa}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
                with open(danfe_path, 'wb') as f:
                    f.write(response_danfe.content)
                print(f"DANFE baixada com sucesso: {danfe_path}")

        # Obtém dados do boleto mais recente
        dados_boleto = obter_dados_boleto_recente(session, base_url, cod_ons, headers)
        if dados_boleto:
            response_download = session.get(
                f"{base_url}/Home/DownloadBoleto",
                params=dados_boleto,
                headers=headers
            )
            
            if response_download.status_code == 200:
                boleto_path = os.path.join(base_path, f"Boleto_{empresa}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
                with open(boleto_path, 'wb') as f:
                    f.write(response_download.content)
                print(f"Boleto baixado com sucesso: {boleto_path}")
                return True

    else:
        print(f"Erro na autenticação para ONS {cod_ons}: {response.status_code}")
    return False

def processar_todas_ons():
    for cod_ons, empresa in ONS_EMPRESAS.items():
        try:
            baixar_titulo_assu(cod_ons, empresa)
        except Exception as e:
            print(f"Erro ao processar ONS {cod_ons} - {empresa}: {str(e)}")
        print("-" * 50)

if __name__ == "__main__":
    processar_todas_ons()
