import requests
import os
import logging
import argparse
import time
from bs4 import BeautifulSoup

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
    # Configurar headers para simular um navegador real
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Origin': 'https://portalcliente.tbenergia.com.br',
        'Referer': 'https://portalcliente.tbenergia.com.br/',
    }
    
    # Criar uma sessão para manter cookies
    session = requests.Session()
    session.headers.update(headers)
    
    # Obter a página de login
    login_url = "https://portalcliente.tbenergia.com.br/"
    logger.info(f"Acessando {login_url}...")
    response = session.get(login_url)
    logger.info(f"Status code: {response.status_code}")
    
    # Preparar os dados de login
    login_data = {
        'Login': usuario,
        'Senha': senha
    }
    
    # URL de login baseada no action do formulário
    login_endpoint = "https://portalcliente.tbenergia.com.br/Login/Index"
    logger.info(f"Enviando requisição de login para {login_endpoint}...")
    
    # Enviar requisição de login
    login_response = session.post(login_endpoint, data=login_data, allow_redirects=True)
    logger.info(f"Status code: {login_response.status_code}")
    logger.info(f"URL após login: {login_response.url}")
    
    # Verificar se o login foi bem-sucedido
    if "Fechamento" in login_response.url:
        logger.info(f"Login bem-sucedido para o usuário {usuario}")
        return session
    else:
        logger.error(f"Falha no login para o usuário {usuario}")
        return None

def obter_notas_fiscais(session, codigo_ons):
    """Obtém as notas fiscais da empresa selecionada"""
    # URL para obter as notas fiscais (usando GET como visto no JavaScript)
    notas_url = f"https://portalcliente.tbenergia.com.br/Fechamento/NotasRecentes?CNPJ={codigo_ons}"
    
    logger.info(f"Enviando requisição para obter notas fiscais da empresa {codigo_ons}...")
    
    # Enviar requisição para obter as notas fiscais
    response = session.get(notas_url)
    
    if response.status_code == 200:
        logger.info(f"Notas fiscais obtidas com sucesso para a empresa {codigo_ons}")
        return response.text
    else:
        logger.error(f"Falha ao obter notas fiscais para a empresa {codigo_ons}. Status code: {response.status_code}")
        return None

def extrair_links_xml(html_content):
    """Extrai os links de XML e informações relacionadas do HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Procurar pela tabela de notas fiscais
    table = soup.find('table', {'id': 'NfRecentes'})
    
    if not table:
        logger.error("Tabela de notas fiscais não encontrada no HTML")
        return []
    
    # Procurar pelas linhas da tabela
    tbody = table.find('tbody')
    if not tbody:
        logger.error("Corpo da tabela não encontrado")
        return []
        
    rows = tbody.find_all('tr')
    resultados = []
    
    for row in rows:
        try:
            # Extrair as células da linha
            cells = row.find_all('td')
            
            # Verificar se há células suficientes
            if len(cells) < 7:  # Precisamos de pelo menos 7 células
                continue
                
            # Extrair as informações das células
            competencia = cells[0].text.strip()
            nf_numero = cells[1].text.strip()
            empresa_atual = cells[3].text.strip()
            cnpj_atual = cells[4].text.strip()
            valor = cells[5].text.strip()
            
            # Limpar o CNPJ (remover caracteres especiais)
            cnpj_atual_limpo = ''.join(filter(str.isdigit, cnpj_atual))
            
            # Procurar pelo link do XML
            xml_link = None
            pdf_link = None
            
            # Verificar todos os links na última célula
            for link in cells[-1].find_all('a'):
                if 'XML' in link.text:
                    xml_link = link.get('href')
                elif 'PDF' in link.text or 'DANFE' in link.text:
                    pdf_link = link.get('href')
            
            # Se não encontrou link PDF explícito, vamos construir um baseado no link XML
            if xml_link and not pdf_link:
                # Analisando o link XML para extrair os parâmetros
                if 'DownloadXml' in xml_link:
                    # Extrair os parâmetros do link XML
                    import re
                    nfe_match = re.search(r'Nfe=([^&]+)', xml_link)
                    cnpj_match = re.search(r'cnpj=([^&]+)', xml_link)
                    
                    if nfe_match and cnpj_match:
                        nfe = nfe_match.group(1)
                        cnpj = cnpj_match.group(1)
                        # Construir o link PDF alterando o endpoint ou o parâmetro tp
                        pdf_link = f"https://portalcliente.tbenergia.com.br/Downloads/DownloadPdf?Nfe={nfe}&cnpj={cnpj}&tp=1"
            
            if xml_link:
                resultados.append({
                    'competencia': competencia,
                    'nf_numero': nf_numero,
                    'empresa': empresa_atual,
                    'cnpj': cnpj_atual,
                    'cnpj_limpo': cnpj_atual_limpo,
                    'valor': valor,
                    'xml_link': xml_link,
                    'pdf_link': pdf_link
                })
        except Exception as e:
            logger.error(f"Erro ao processar linha da tabela: {str(e)}")
    
    return resultados

def baixar_arquivo(session, url, download_dir, filename, tipo):
    """Baixa um arquivo usando o link fornecido"""
    try:
        # Garantir que o link seja absoluto
        if not url.startswith('http'):
            url = f"https://portalcliente.tbenergia.com.br{url}"
        
        logger.info(f"Baixando {tipo} de {url}...")
        
        # Fazer a requisição para baixar o arquivo
        response = session.get(url)
        
        if response.status_code == 200:
            # Caminho completo para salvar o arquivo
            file_path = os.path.join(download_dir, filename)
            
            # Salvar o arquivo
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"✓ {tipo} baixado com sucesso: {filename}")
            return True
        else:
            logger.error(f"❌ Falha ao baixar {tipo}. Status code: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Erro ao baixar {tipo}: {str(e)}")
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
            base_download_dir = os.path.join(r"C:\Users\Bruno\Downloads\TUST\TBE", categoria, codigo_ons)
            if not os.path.exists(base_download_dir):
                os.makedirs(base_download_dir)
            
            logger.info(f"\nIniciando processamento da empresa {nome_empresa} (Código ONS: {codigo_ons}, Categoria: {categoria})")
            
            # Realizar login
            session = login_tbe(usuario, senha)
            if not session:
                logger.error(f"Não foi possível processar a empresa {nome_empresa} devido a falha no login")
                continue
            
            # Obter as notas fiscais da empresa
            html_content = obter_notas_fiscais(session, codigo_ons)
            if not html_content:
                logger.error(f"Não foi possível obter as notas fiscais da empresa {nome_empresa}")
                continue
            
            # Salvar o HTML para debug
            debug_file = os.path.join(base_download_dir, "notas_fiscais.html")
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            logger.info(f"HTML das notas fiscais salvo em {debug_file}")
            
            # Extrair os links de XML e PDF
            resultados = extrair_links_xml(html_content)
            
            if not resultados:
                logger.warning(f"Nenhum XML encontrado para a empresa {nome_empresa}")
                continue
            
            logger.info(f"Encontrados {len(resultados)} XMLs para a empresa {nome_empresa}")
            
            # Inicializar contadores
            total_xmls = 0
            total_pdfs = 0
            empresas_processadas = set()
            
            # Processar os resultados
            for i, info in enumerate(resultados, 1):
                try:
                    # Log detalhado do download
                    logger.info(f"\nBaixando arquivos {i}/{len(resultados)}")
                    logger.info(f"Transmissora: {info['empresa']}")
                    logger.info(f"CNPJ: {info['cnpj']}")
                    logger.info(f"NF: {info['nf_numero']}")
                    logger.info(f"Competência: {info['competencia']}")
                    logger.info(f"Valor: {info['valor']}")
                    
                    # Se for uma nova transmissora, criar diretório específico
                    if (info['cnpj_limpo'], info['empresa']) not in empresas_processadas:
                        download_dir = create_download_dir(base_download_dir, info['cnpj_limpo'], info['empresa'])
                        empresas_processadas.add((info['cnpj_limpo'], info['empresa']))
                        logger.info(f"Nova transmissora detectada: {info['empresa']}")
                        logger.info(f"CNPJ: {info['cnpj_limpo']}")
                        logger.info(f"Criado diretório: {download_dir}")
                    else:
                        download_dir = create_download_dir(base_download_dir, info['cnpj_limpo'], info['empresa'])
                    
                    # Baixar o XML
                    xml_filename = f"NF_{info['nf_numero']}_{info['competencia'].replace('/', '_')}.xml"
                    if baixar_arquivo(session, info['xml_link'], download_dir, xml_filename, "XML"):
                        total_xmls += 1
                    
                    # Baixar o PDF (DANFE) se disponível
                    if info['pdf_link']:
                        pdf_filename = f"NF_{info['nf_numero']}_{info['competencia'].replace('/', '_')}.pdf"
                        if baixar_arquivo(session, info['pdf_link'], download_dir, pdf_filename, "PDF"):
                            total_pdfs += 1
                    else:
                        # Tentar construir o link do PDF a partir do link do XML
                        xml_url = info['xml_link']
                        if 'DownloadXml' in xml_url:
                            # Substituir DownloadXml por DownloadPdf
                            pdf_url = xml_url.replace('DownloadXml', 'DownloadPdf')
                            pdf_filename = f"NF_{info['nf_numero']}_{info['competencia'].replace('/', '_')}.pdf"
                            if baixar_arquivo(session, pdf_url, download_dir, pdf_filename, "PDF"):
                                total_pdfs += 1
                    
                    # Pequena pausa para não sobrecarregar o servidor
                    time.sleep(0.5)
                    
                except Exception as e:
                    logger.error(f"❌ Erro ao baixar arquivos: {str(e)}")
                    continue
            
            logger.info(f"Total de XMLs baixados para {nome_empresa}: {total_xmls}")
            logger.info(f"Total de PDFs baixados para {nome_empresa}: {total_pdfs}")
            
        except Exception as e:
            logger.error(f"Erro ao processar empresa {nome_empresa}: {str(e)}")
            continue

def main():
    parser = argparse.ArgumentParser(description='Download de XMLs e PDFs do Portal TBE Energia')
    parser.add_argument('--categorias', nargs='+', choices=['AE', 'DE', 'RE', 'TODAS'], 
                        default=['TODAS'], help='Categorias de empresas a processar (AE, DE, RE ou TODAS)')
    
    args = parser.parse_args()
    
    # Se TODAS for especificado, processar todas as categorias
    if 'TODAS' in args.categorias:
        categorias = ['AE', 'DE', 'RE']
    else:
        categorias = args.categorias
    
    logger.info(f"Iniciando processo de download de XMLs e PDFs para as categorias: {', '.join(categorias)}")
    processar_empresas(categorias)
    logger.info("Processo finalizado")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Erro fatal: {str(e)}")