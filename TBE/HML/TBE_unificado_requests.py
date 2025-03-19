import requests
import os
import logging
import argparse
import time
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

# Dicionário com todas as empresas organizadas por categoria
EMPRESAS = {
    "AE": [
        ('8011', 'LIBRA LIGAS DO BRASIL S/A', 'klebe1079', 'kl#b#1079'),
        ('3859', 'CELEO SAO JOAO DO PIAUI FV I S.A.', 'bruno1124', 'bruno1124'),
        ('3860', 'CELEO SAO JOAO DO PIAUI FV II S.A.', 'bruno1124', 'bruno1124'),
        ('3861', 'CELEO SAO JOAO DO PIAUI FV III S.A.', 'bruno1124', 'bruno1124'),
        ('3862', 'CELEO SAO JOAO DO PIAUI FV IV S.A.', 'bruno1124', 'bruno1124'),
        ('3863', 'CELEO SAO JOAO DO PIAUI FV V S.A.', 'bruno1124', 'bruno1124'),
        ('3864', 'CELEO SAO JOAO DO PIAUI FV VI S.A.', 'bruno1124', 'bruno1124'),
        ('3740', 'COREMAS I GERACAO DE ENERGIA SPE S.A.', 'anac1205', '@n@c1205'),
        ('3741', 'COREMAS II GERACAO DE ENERGIA II SPE S.A.', 'anac1205', '@n@c1205'),
        ('3750', 'COREMAS III GERACAO DE ENERGIA SPES.A.', 'anac1205', '@n@c1205'),
    ],
    "DE": [
        ('3748', 'DIAMANTE GERACAO DE ENERGIA LTDA', 'najla1447', 'n@jl@1447'),
    ],
    "RE": [
        ('3430', 'EOLICA CAETITE A S.A.', 'carol1758', 'c@rol1758'),
        ('3431', 'EOLICA CAETITE B S.A.', 'carol1758', 'c@rol1758'),
        ('3432', 'EOLICA CAETITE C S.A', 'carol1758', 'c@rol1758'),
        # ... outras empresas RE ...
    ]
}

def setup_logger():
    """Configura e retorna o logger"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)

# Criar logger global
logger = setup_logger()

def create_download_dir(base_dir, cnpj, empresa_nome):
    """Cria diretório específico para a empresa"""
    empresa_nome = empresa_nome.replace('/', '-').replace('\\', '-').strip()
    download_dir = os.path.join(base_dir, f"CNPJ_{cnpj}", empresa_nome)
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    return download_dir

def login_tbe(usuario, senha):
    """Realiza login no portal TBE e retorna a sessão autenticada"""
    session = requests.Session()
    
    # Obter o token CSRF da página de login
    login_url = "https://portalcliente.tbenergia.com.br/"
    response = session.get(login_url)
    
    # Extrair o token CSRF usando BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    token_input = soup.find('input', {'name': '__RequestVerificationToken'})
    
    if not token_input:
        logger.error("Não foi possível encontrar o token CSRF na página de login")
        return None
    
    token = token_input.get('value')
    
    # Preparar os dados de login
    login_data = {
        'Login': usuario,
        'Senha': senha,
        '__RequestVerificationToken': token
    }
    
    # Enviar requisição de login
    login_response = session.post(login_url, data=login_data)
    
    # Verificar se o login foi bem-sucedido
    if "Fechamento" in login_response.url:
        logger.info(f"Login bem-sucedido para o usuário {usuario}")
        return session
    else:
        logger.error(f"Falha no login para o usuário {usuario}")
        return None

def obter_dados_empresa(session, codigo_ons):
    """Obtém os dados da empresa selecionada"""
    url = "https://portalcliente.tbenergia.com.br/Fechamento"
    
    # Primeiro, obter a página para extrair o token CSRF
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    token_input = soup.find('input', {'name': '__RequestVerificationToken'})
    
    if not token_input:
        logger.error("Não foi possível encontrar o token CSRF na página de filtro")
        return None
    
    token = token_input.get('value')
    
    # Preparar os dados para o filtro
    filtro_data = {
        'CNPJ': codigo_ons,
        '__RequestVerificationToken': token
    }
    
    # Enviar requisição para filtrar por empresa
    filtro_response = session.post(url, data=filtro_data)
    
    if filtro_response.status_code == 200:
        logger.info(f"Filtro aplicado com sucesso para o código ONS {codigo_ons}")
        return filtro_response.text
    else:
        logger.error(f"Falha ao aplicar filtro para o código ONS {codigo_ons}")
        return None

def extrair_links_xml(html_content):
    """Extrai os links de XML e informações relacionadas da página HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', {'id': 'NfRecentes'})
    
    if not table:
        logger.error("Tabela de NFs não encontrada na página")
        return []
    
    rows = table.find('tbody').find_all('tr')
    resultados = []
    
    for row in rows:
        try:
            cells = row.find_all('td')
            
            # Extrair informações das células
            competencia = cells[0].text.strip()
            nf_numero = cells[1].text.strip()
            empresa_atual = cells[3].text.strip()
            cnpj_atual = cells[4].text.strip()
            valor = cells[5].text.strip()
            
            # Limpar o CNPJ (remover caracteres especiais)
            cnpj_atual = ''.join(filter(str.isdigit, cnpj_atual))
            
            # Encontrar o link do XML
            xml_link = None
            for link in cells[-1].find_all('a'):
                if 'XML' in link.text:
                    xml_link = link.get('href')
                    break
            
            if xml_link:
                resultados.append({
                    'competencia': competencia,
                    'nf_numero': nf_numero,
                    'empresa': empresa_atual,
                    'cnpj': cnpj_atual,
                    'valor': valor,
                    'xml_link': xml_link
                })
        except Exception as e:
            logger.error(f"Erro ao processar linha da tabela: {str(e)}")
    
    return resultados

def verificar_proxima_pagina(html_content):
    """Verifica se existe uma próxima página e retorna o link se existir"""
    soup = BeautifulSoup(html_content, 'html.parser')
    next_button = soup.find('a', {'id': 'NfRecentes_next'})
    
    if next_button and 'disabled' not in next_button.get('class', []):
        # Extrair o número da próxima página
        current_page = int(soup.find('a', {'class': 'paginate_button current'}).text)
        next_page = current_page + 1
        
        # Construir o link para a próxima página
        return f"https://portalcliente.tbenergia.com.br/Fechamento?page={next_page}"
    
    return None

def baixar_xml(session, xml_link, download_dir, info):
    """Baixa o arquivo XML usando o link fornecido"""
    try:
        # Garantir que o link seja absoluto
        if not xml_link.startswith('http'):
            xml_link = urljoin('https://portalcliente.tbenergia.com.br/', xml_link)
        
        # Fazer a requisição para baixar o XML
        response = session.get(xml_link, stream=True)
        
        if response.status_code == 200:
            # Extrair o nome do arquivo do cabeçalho Content-Disposition ou criar um nome baseado nas informações
            filename = None
            if 'Content-Disposition' in response.headers:
                content_disp = response.headers['Content-Disposition']
                matches = re.findall('filename="(.+?)"', content_disp)
                if matches:
                    filename = matches[0]
            
            if not filename:
                # Criar um nome de arquivo baseado nas informações disponíveis
                filename = f"NF_{info['nf_numero']}_{info['competencia'].replace('/', '_')}.xml"
            
            # Caminho completo para salvar o arquivo
            file_path = os.path.join(download_dir, filename)
            
            # Salvar o arquivo
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            logger.info(f"✓ XML baixado com sucesso: {filename}")
            return True
        else:
            logger.error(f"❌ Falha ao baixar XML. Status code: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Erro ao baixar XML: {str(e)}")
        return False

def processar_empresas(categorias):
    global logger
    
    # Lista para armazenar todas as empresas a serem processadas
    empresas_para_processar = []
    
    # Adicionar empresas das categorias selecionadas
    for categoria in categorias:
        if categoria in EMPRESAS:
            empresas_para_processar.extend([(codigo, nome, usuario, senha, categoria) 
                                           for codigo, nome, *credenciais in EMPRESAS[categoria]
                                           for usuario, senha in [credenciais if len(credenciais) == 2 else ('carol1758', 'c@rol1758')]])
    
    logger.info(f"Total de empresas a processar: {len(empresas_para_processar)}")
    
    for codigo_ons, nome_empresa, usuario, senha, categoria in empresas_para_processar:
        try:
            # Diretório base para downloads
            base_download_dir = os.path.join(r"C:\Users\Bruno\Downloads\TBE", categoria, codigo_ons)
            if not os.path.exists(base_download_dir):
                os.makedirs(base_download_dir)
            
            logger.info(f"\nIniciando processamento da empresa {nome_empresa} (Código ONS: {codigo_ons}, Categoria: {categoria})")
            
            # Realizar login
            session = login_tbe(usuario, senha)
            if not session:
                logger.error(f"Não foi possível processar a empresa {nome_empresa} devido a falha no login")
                continue
            
            # Obter dados da empresa
            html_content = obter_dados_empresa(session, codigo_ons)
            if not html_content:
                logger.error(f"Não foi possível obter dados da empresa {nome_empresa}")
                continue
            
            # Inicializar contadores
            total_xmls = 0
            pagina_atual = 1
            empresas_processadas = set()
            
            logger.info("Iniciando processamento dos XMLs...")
            
            while html_content:
                logger.info(f"\nProcessando página {pagina_atual}")
                
                # Extrair links de XML e informações relacionadas
                resultados = extrair_links_xml(html_content)
                
                logger.info(f"Encontrados {len(resultados)} XMLs na página {pagina_atual}")
                
                for i, info in enumerate(resultados, 1):
                    try:
                        # Log detalhado do download
                        logger.info(f"\nBaixando XML {i}/{len(resultados)} da página {pagina_atual}")
                        logger.info(f"Transmissora: {info['empresa']}")
                        logger.info(f"CNPJ: {info['cnpj']}")
                        logger.info(f"NF: {info['nf_numero']}")
                        logger.info(f"Competência: {info['competencia']}")
                        logger.info(f"Valor: {info['valor']}")
                        
                        # Se for uma nova transmissora, criar diretório específico
                        if (info['cnpj'], info['empresa']) not in empresas_processadas:
                            download_dir = create_download_dir(base_download_dir, info['cnpj'], info['empresa'])
                            empresas_processadas.add((info['cnpj'], info['empresa']))
                            logger.info(f"Nova transmissora detectada: {info['empresa']}")
                            logger.info(f"CNPJ: {info['cnpj']}")
                            logger.info(f"Criado diretório: {download_dir}")
                        else:
                            download_dir = create_download_dir(base_download_dir, info['cnpj'], info['empresa'])
                        
                        # Baixar o XML
                        if baixar_xml(session, info['xml_link'], download_dir, info):
                            total_xmls += 1
                        
                        # Pequena pausa para não sobrecarregar o servidor
                        time.sleep(0.5)
                        
                    except Exception as e:
                        logger.error(f"❌ Erro ao baixar XML na página {pagina_atual}: {str(e)}")
                        continue
                
                # Verificar se existe próxima página
                next_page_url = verificar_proxima_pagina(html_content)
                if next_page_url:
                    logger.info(f"Avançando para a página {pagina_atual + 1}")
                    response = session.get(next_page_url)
                    if response.status_code == 200:
                        html_content = response.text
                        pagina_atual += 1
                    else:
                        logger.error(f"Erro ao acessar a próxima página. Status code: {response.status_code}")
                        break
                else:
                    logger.info("Chegou à última página")
                    break
            
            logger.info(f"Total de XMLs baixados para {nome_empresa}: {total_xmls}")
            
        except Exception as e:
            logger.error(f"Erro ao processar empresa {nome_empresa}: {str(e)}")
            continue

def main():
    parser = argparse.ArgumentParser(description='Download de XMLs do Portal TBE Energia')
    parser.add_argument('--categorias', nargs='+', choices=['AE', 'DE', 'RE', 'TODAS'], 
                        default=['TODAS'], help='Categorias de empresas a processar (AE, DE, RE ou TODAS)')
    
    args = parser.parse_args()
    
    # Se TODAS for especificado, processar todas as categorias
    if 'TODAS' in args.categorias:
        categorias = ['AE', 'DE', 'RE']
    else:
        categorias = args.categorias
    
    logger.info(f"Iniciando processo de download de XMLs para as categorias: {', '.join(categorias)}")
    processar_empresas(categorias)
    logger.info("Processo finalizado")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Erro fatal: {str(e)}") 