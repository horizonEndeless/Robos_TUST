import requests
import json
from datetime import datetime
import os
from bs4 import BeautifulSoup
import re

# Dicionário com todas as empresas e suas ONS
EMPRESAS = {
    "RE": {  # Comentado pois já está funcionando
        "base_url": "https://faturamentoassu.cesbe.com.br",
        "ons": {
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
    },
    "AE": {
        "base_url": "https://faturamentoassu.cesbe.com.br",
        "ons": {
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
    },
    "DE": {
        "base_url": "https://faturamentoassu.cesbe.com.br",
        "ons": {
            "3748": "DE"
        }
    }
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
        tabela = soup.find('table', {'class': 'tableGrid'})
        if tabela:
            linha = tabela.find('tr', {'class': 'dif'})
            if linha:
                # Encontra o link de download do boleto
                link_download = linha.find('a', href=True)
                if link_download:
                    # Extrai os parâmetros do link
                    href = link_download['href']
                    params = {}
                    for param in href.split('?')[1].split('&'):
                        if '=' in param:
                            key, value = param.split('=')
                            params[key] = value.replace('%20', ' ').replace('%2F', '/').replace('%3A', ':')
                    
                    # Extrai apenas os parâmetros necessários
                    dados_boleto = {
                        "CodEmp": params.get('CodEmp', '18'),
                        "CodFil": params.get('CodFil', '2'),
                        "NumTit": params.get('NumTit', ''),
                        "CodTpt": params.get('CodTpt', 'DP'),
                        "VlrAbe": params.get('VlrAbe', ''),
                        "CodPor": params.get('CodPor', '341'),
                        "CodCrt": params.get('CodCrt', 'SI'),
                        "TitBan": params.get('TitBan', ''),
                        "CgcCpf": params.get('CgcCpf', '33485728000100'),
                        "CodPar": params.get('CodPar', '1'),
                        "CodOns": cod_ons,
                        "CodSel": params.get('CodSel', '1'),
                        "RecUnn": params.get('RecUnn', ''),
                        "ModBlo": params.get('ModBlo', 'FRCR223.BLO'),
                        "NomBan": params.get('NomBan', 'BANCO ITAU S.A.')
                    }
                    
                    print(f"Dados do boleto mais recente para ONS {cod_ons}:")
                    print(json.dumps(dados_boleto, indent=2))
                    return dados_boleto
    return None

def baixar_titulo(empresa_nome, cod_ons, nome_ons):
    print(f"\nProcessando {empresa_nome} - ONS {cod_ons} - {nome_ons}")
    
    base_url = EMPRESAS[empresa_nome]["base_url"]
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }

    session = requests.Session()
    
    # Login com os dados corretos
    response = session.post(
        f"{base_url}/",
        data={
            "CodOns": cod_ons,
            "CodEmp": "18"
        },
        headers=headers
    )
    
    if response.status_code == 200:
        # Criar estrutura de pastas dentro de ASSU
        base_path = os.path.join(r"C:\Users\Bruno\Downloads\TUST\ASSU", empresa_nome, cod_ons)
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
                xml_path = os.path.join(base_path, f"NFe_{nome_ons}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml")
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
                danfe_path = os.path.join(base_path, f"DANFE_{nome_ons}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
                with open(danfe_path, 'wb') as f:
                    f.write(response_danfe.content)
                print(f"DANFE baixada com sucesso: {danfe_path}")

        # Download do boleto
        dados_boleto = obter_dados_boleto_recente(session, base_url, cod_ons, headers)
        if dados_boleto:
            response_download = session.get(
                f"{base_url}/Home/DownloadBoleto",
                params=dados_boleto,
                headers=headers
            )
            
            if response_download.status_code == 200:
                boleto_path = os.path.join(base_path, f"Boleto_{nome_ons}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
                with open(boleto_path, 'wb') as f:
                    f.write(response_download.content)
                print(f"Boleto baixado com sucesso: {boleto_path}")
                return True

    else:
        print(f"Erro na autenticação para ONS {cod_ons}: {response.status_code}")
    return False

def processar_todas_empresas():
    for empresa_nome, dados in EMPRESAS.items():
        print(f"\nProcessando empresa: {empresa_nome}")
        for cod_ons, nome_ons in dados["ons"].items():
            try:
                baixar_titulo(empresa_nome, cod_ons, nome_ons)
            except Exception as e:
                print(f"Erro ao processar {empresa_nome} - ONS {cod_ons} - {nome_ons}: {str(e)}")
            print("-" * 50)

if __name__ == "__main__":
    processar_todas_empresas()
