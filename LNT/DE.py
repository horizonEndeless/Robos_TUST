import requests
from bs4 import BeautifulSoup
import os
import time
import logging
from datetime import datetime
import re
import json
import urllib.parse
import pdfkit
import shutil

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("sigetplus_downloader_lnt.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("SigetPlusDownloaderLNT")

# Mapeamento de códigos para nomes de transmissoras
TRANSMISSORAS = {
    "3748": "DE",
}

class SigetPlusDownloader:
    """
    Classe para baixar faturas do site da Siget Plus para LNT
    (https://sys.sigetplus.com.br/cobranca/transmitter/1143/invoices?agent=3748)
    """
    
    def __init__(self, download_dir=None, wkhtmltopdf_path=None):
        self.session = requests.Session()
        self.base_url = "https://sys.sigetplus.com.br/cobranca"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        
        # Definir diretório de download
        if download_dir:
            self.download_dir = download_dir
        else:
            self.download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "TUST", "LNT", "DE")
        
        # Criar diretório para download se não existir
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
            logger.info(f"Diretório de download criado: {self.download_dir}")
            
        # Criar diretórios para cada transmissora
        self.criar_diretorios_transmissoras()
            
        # Configuração do wkhtmltopdf
        self.wkhtmltopdf_path = wkhtmltopdf_path
        if self.wkhtmltopdf_path:
            self.pdf_config = pdfkit.configuration(wkhtmltopdf=self.wkhtmltopdf_path)
            logger.info(f"wkhtmltopdf configurado: {self.wkhtmltopdf_path}")
        else:
            self.pdf_config = None
            logger.warning("wkhtmltopdf não configurado. Conversão HTML para PDF não estará disponível.")
    
    def criar_diretorios_transmissoras(self):
        """
        Cria diretórios para todas as transmissoras definidas no mapeamento
        """
        for codigo, nome in TRANSMISSORAS.items():
            dir_path = os.path.join(self.download_dir, nome)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                logger.info(f"Diretório para transmissora {nome} (código {codigo}) criado: {dir_path}")
    
    def criar_diretorio_transmissora(self, transmissora_codigo, transmissora_nome):
        """
        Identifica e retorna o diretório correto para a transmissora
        
        Args:
            transmissora_codigo (str): Código da transmissora
            transmissora_nome (str): Nome da transmissora
            
        Returns:
            str: Caminho do diretório para a transmissora
        """
        # Extrair o código da transmissora (primeiro número antes do hífen)
        codigo_transmissora = transmissora_codigo.strip()
        
        # Procurar o código no mapeamento de transmissoras
        nome_pasta = None
        for codigo, nome in TRANSMISSORAS.items():
            if codigo == codigo_transmissora:
                nome_pasta = nome
                break
        
        # Se não encontrou pelo código exato, tentar encontrar pelo início do código
        if not nome_pasta:
            for codigo, nome in TRANSMISSORAS.items():
                if codigo_transmissora.startswith(codigo):
                    nome_pasta = nome
                    break
        
        # Se ainda não encontrou, usar o código original
        if not nome_pasta:
            nome_pasta = codigo_transmissora
            logger.warning(f"Código de transmissora não mapeado: {codigo_transmissora}. Usando o código como nome da pasta.")
        
        # Caminho do diretório
        dir_path = os.path.join(self.download_dir, nome_pasta)
        
        # Criar diretório se não existir
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            logger.info(f"Diretório para transmissora {nome_pasta} criado: {dir_path}")
        
        return dir_path
    
    def acessar_site(self, agent, time_period):
        """
        Acessa o site de faturas da Siget Plus para LNT
        
        Args:
            agent (str): Código do agente (ex: 3748)
            time_period (str): Período de tempo (ex: 202502 para fevereiro de 2025)
            
        Returns:
            str: Conteúdo HTML da página
        """
        try:
            # Construir URL com parâmetros
            url = f"{self.base_url}/transmitter/1143/invoices"
            params = {
                "agent": agent,
                "time": time_period
            }
            
            logger.info(f"Acessando página para o agente {agent} no período {time_period}...")
            response = self.session.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            
            logger.info(f"Página acessada com sucesso. Status code: {response.status_code}")
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao acessar o site: {e}")
            return None
    
    def extrair_links_faturas(self, html_content):
        """
        Extrai os links das faturas disponíveis na página
        
        Args:
            html_content (str): Conteúdo HTML da página
            
        Returns:
            list: Lista de dicionários com informações das faturas
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            faturas = []
            
            # Encontrar todas as linhas da tabela
            linhas = soup.select('table tbody tr')
            logger.info(f"Encontradas {len(linhas)} linhas na tabela")
            
            # # Salvar HTML para debug
            # debug_dir = os.path.join(self.download_dir, "debug")
            # if not os.path.exists(debug_dir):
            #     os.makedirs(debug_dir)
            # debug_file = os.path.join(debug_dir, f"debug_page.html")
            # with open(debug_file, 'w', encoding='utf-8') as f:
            #     f.write(html_content)
            # logger.info(f"HTML da página salvo para debug em: {debug_file}")
            
            # Procurar links XML e DANFE em toda a página
            xml_links = re.findall(r'href=[\'"]([^\'"]*nfe\.xml)[\'"]', html_content)
            danfe_links = re.findall(r'href=[\'"]([^\'"]*\.pdf)[\'"]', html_content)
            
            if xml_links:
                logger.info(f"Links XML encontrados na página: {xml_links}")
            if danfe_links:
                logger.info(f"Links DANFE encontrados na página: {danfe_links}")
            
            for linha in linhas:
                try:
                    # Extrair informações da fatura
                    colunas = linha.find_all('td')
                    if len(colunas) < 5:  # Ajustado para o formato da tabela da LNT
                        logger.warning(f"Linha com número insuficiente de colunas: {len(colunas)}")
                        continue
                    
                    transmissora = "LUZIANIA-NIQUELANDIA TRANSMISSORA S.A"  # Nome fixo da transmissora
                    
                    # Extrair número da fatura da primeira coluna
                    numero_fatura_elem = colunas[0].find('a')
                    if numero_fatura_elem:
                        numero_fatura = numero_fatura_elem.text.strip()
                    else:
                        numero_fatura = colunas[0].text.strip()
                    
                    # Links
                    links = {}
                    
                    # Link da fatura
                    if numero_fatura_elem and numero_fatura_elem.has_attr('href'):
                        links['fatura'] = numero_fatura_elem['href']
                    
                    # Links dos boletos (podem ser até 3)
                    for i in range(1, 4):
                        if i < len(colunas):
                            boleto_elem = colunas[i].find('a')
                            if boleto_elem and boleto_elem.has_attr('href'):
                                links[f'boleto_{i}'] = boleto_elem['href']
                    
                    # Link do XML e DANFE (última coluna)
                    if len(colunas) >= 5:
                        # Extrair HTML da última coluna para debug
                        ultima_coluna_html = str(colunas[4])
                        logger.info(f"HTML da última coluna: {ultima_coluna_html}")
                        
                        # Procurar links XML e DANFE na última coluna
                        xml_match = re.search(r'href=[\'"]([^\'"]*nfe\.xml)[\'"]', ultima_coluna_html)
                        danfe_match = re.search(r'href=[\'"]([^\'"]*\.pdf)[\'"]', ultima_coluna_html)
                        
                        if xml_match:
                            links['xml'] = xml_match.group(1)
                            logger.info(f"Link XML encontrado na coluna: {links['xml']}")
                        
                        if danfe_match:
                            links['danfe'] = danfe_match.group(1)
                            logger.info(f"Link DANFE encontrado na coluna: {links['danfe']}")
                        
                        # Se não encontrou com regex, tentar com BeautifulSoup
                        if 'xml' not in links or 'danfe' not in links:
                            links_ultima_coluna = colunas[4].find_all('a')
                            
                            for link in links_ultima_coluna:
                                href = link.get('href', '')
                                text = link.text.strip()
                                
                                # Verificar se é XML
                                if ('XML' in text) and 'xml' not in links:
                                    links['xml'] = href
                                    logger.info(f"Link XML encontrado via texto do link: {href}")
                                
                                # Verificar se é DANFE
                                elif ('DANFE' in text) and 'danfe' not in links:
                                    links['danfe'] = href
                                    logger.info(f"Link DANFE encontrado via texto do link: {href}")
                    
                    # Se ainda não encontrou XML ou DANFE, procurar em toda a página
                    if 'xml' not in links and xml_links:
                        links['xml'] = xml_links[0]  # Usar o primeiro link XML encontrado
                        logger.info(f"Link XML obtido da página completa: {links['xml']}")
                    
                    if 'danfe' not in links and danfe_links:
                        # Filtrar apenas links DANFE (excluir outros PDFs)
                        danfe_filtered = [link for link in danfe_links if 'danfe' in link.lower()]
                        if danfe_filtered:
                            links['danfe'] = danfe_filtered[0]
                            logger.info(f"Link DANFE obtido da página completa: {links['danfe']}")
                    
                    # Adicionar à lista de faturas apenas se tiver pelo menos um link
                    if links:
                        faturas.append({
                            'transmissora': transmissora,
                            'numero_fatura': numero_fatura,
                            'links': links
                        })
                        logger.info(f"Fatura encontrada: {transmissora} - {numero_fatura}")
                        logger.info(f"Links encontrados: {links}")
                    
                except Exception as e:
                    logger.error(f"Erro ao extrair informações da linha: {e}")
                    continue
            
            logger.info(f"Encontradas {len(faturas)} faturas na página")
            return faturas
        except Exception as e:
            logger.error(f"Erro ao extrair links de faturas: {e}")
            return []
    
    def converter_html_para_pdf(self, html_content, output_path):
        """
        Converte conteúdo HTML para PDF usando wkhtmltopdf
        
        Args:
            html_content (str): Conteúdo HTML
            output_path (str): Caminho de saída para o arquivo PDF
            
        Returns:
            bool: True se a conversão foi bem-sucedida, False caso contrário
        """
        try:
            if not self.pdf_config:
                logger.warning("wkhtmltopdf não configurado. Não é possível converter HTML para PDF.")
                return False
            
            # Salvar HTML temporariamente
            temp_html_path = output_path + ".temp.html"
            with open(temp_html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Converter para PDF
            pdfkit.from_file(temp_html_path, output_path, configuration=self.pdf_config)
            
            # Remover arquivo temporário
            os.remove(temp_html_path)
            
            logger.info(f"HTML convertido para PDF com sucesso: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Erro ao converter HTML para PDF: {e}")
            return False
    
    def baixar_arquivo(self, url, nome_arquivo, dir_path):
        """
        Baixa um arquivo a partir de uma URL
        
        Args:
            url (str): URL do arquivo
            nome_arquivo (str): Nome do arquivo a ser salvo
            dir_path (str): Diretório onde o arquivo será salvo
            
        Returns:
            str: Caminho do arquivo baixado ou None em caso de erro
        """
        try:
            logger.info(f"Baixando arquivo: {nome_arquivo} - URL: {url}")
            
            # Verificar se a URL é relativa e completá-la se necessário
            if url.startswith('/'):
                url = f"https://sys.sigetplus.com.br{url}"
            
            # Configurar headers específicos para XML
            headers = self.headers.copy()
            if '.xml' in url.lower():
                headers.update({
                    "Accept": "application/xml,text/xml,*/*",
                    "Cache-Control": "no-cache, no-store, must-revalidate",
                    "Pragma": "no-cache",
                    "Expires": "0"
                })
            
            # Não adicionar timestamp para URLs de XML externas
            if 'nfe-documentos.sigetplus.com.br' not in url:
                # Adicionar timestamp para evitar cache
                if '?' not in url:
                    url = f"{url}?_={int(time.time())}"
                else:
                    url = f"{url}&_={int(time.time())}"
                
                logger.info(f"URL modificada para XML: {url}")
        
            # Fazer a requisição
            response = self.session.get(url, headers=headers, stream=True)
            response.raise_for_status()
            
            # Verificar se o conteúdo está vazio
            if len(response.content) == 0:
                logger.warning(f"Conteúdo vazio. Tentando novamente com cache desativado.")
                # Tentar novamente com cache explicitamente desativado
                headers.update({
                    "Cache-Control": "no-cache, no-store, must-revalidate",
                    "Pragma": "no-cache",
                    "Expires": "0"
                })
                response = self.session.get(url, headers=headers, stream=True, params={"_": int(time.time())})
                response.raise_for_status()
            
            # Determinar extensão do arquivo
            if 'xml' in url.lower():
                extensao = '.xml'
            elif 'danfe' in url.lower():
                extensao = '.pdf'
            elif 'billet' in url.lower() or 'boleto' in url.lower():
                # Verificar se é HTML ou PDF
                content_type = response.headers.get('Content-Type', '')
                if 'text/html' in content_type:
                    # Se for HTML, vamos salvar como HTML primeiro e depois converter para PDF
                    extensao = '.html'
                else:
                    extensao = '.pdf'
            else:
                # Verificar pelo Content-Type
                content_type = response.headers.get('Content-Type', '')
                if 'application/pdf' in content_type:
                    extensao = '.pdf'
                elif 'text/xml' in content_type or 'application/xml' in content_type:
                    extensao = '.xml'
                elif 'text/html' in content_type:
                    extensao = '.html'
                else:
                    extensao = ''
            
            # Caminho completo do arquivo
            filepath = os.path.join(dir_path, f"{nome_arquivo}{extensao}")
            
            # Salvar o arquivo
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            # Verificar se o arquivo foi salvo corretamente
            if os.path.getsize(filepath) == 0:
                logger.error(f"Arquivo salvo está vazio: {filepath}")
                
                # Para XMLs, tentar baixar diretamente com urllib
                if '.xml' in url.lower():
                    logger.info("Tentando baixar XML com urllib")
                    import urllib.request
                    
                    # Configurar cabeçalhos para urllib
                    opener = urllib.request.build_opener()
                    for key, value in headers.items():
                        opener.addheaders.append((key, value))
                    urllib.request.install_opener(opener)
                    
                    # Baixar o arquivo
                    try:
                        urllib.request.urlretrieve(url, filepath)
                        if os.path.getsize(filepath) > 0:
                            logger.info(f"XML baixado com sucesso usando urllib: {filepath}")
                            return filepath
                    except Exception as e:
                        logger.error(f"Erro ao baixar XML com urllib: {e}")
                
                    # Se ainda falhou, tentar com uma requisição simples sem cache
                    try:
                        logger.info("Tentando baixar XML com requisição simples")
                        simple_response = requests.get(url, headers={
                            "User-Agent": "Mozilla/5.0",
                            "Cache-Control": "no-cache"
                        })
                        if simple_response.content:
                            with open(filepath, 'wb') as f:
                                f.write(simple_response.content)
                            if os.path.getsize(filepath) > 0:
                                logger.info(f"XML baixado com sucesso usando requisição simples: {filepath}")
                                return filepath
                    except Exception as e:
                        logger.error(f"Erro ao baixar XML com requisição simples: {e}")
                
                    return None
            
            # Se for HTML e tivermos wkhtmltopdf configurado, converter para PDF
            if extensao == '.html' and ('boleto' in nome_arquivo.lower() or 'billet' in nome_arquivo.lower()) and self.pdf_config:
                pdf_path = os.path.join(dir_path, f"{nome_arquivo}.pdf")
                
                # Ler o conteúdo HTML
                with open(filepath, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # Converter para PDF
                if self.converter_html_para_pdf(html_content, pdf_path):
                    # Se a conversão for bem-sucedida, retornar o caminho do PDF
                    logger.info(f"Boleto HTML convertido para PDF: {pdf_path}")
                    # Opcionalmente, remover o arquivo HTML original
                    os.remove(filepath)
                    return pdf_path
            
            logger.info(f"Arquivo baixado com sucesso: {filepath}")
            return filepath
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao baixar arquivo: {e}")
            
            # Para XMLs, tentar baixar diretamente com urllib como último recurso
            if '.xml' in url.lower():
                logger.info("Tentando baixar XML com urllib após falha no requests")
                import urllib.request
                
                # Configurar cabeçalhos para urllib
                opener = urllib.request.build_opener()
                for key, value in headers.items():
                    opener.addheaders.append((key, value))
                urllib.request.install_opener(opener)
                
                # Caminho completo do arquivo
                filepath = os.path.join(dir_path, f"{nome_arquivo}.xml")
                
                # Baixar o arquivo
                try:
                    urllib.request.urlretrieve(url, filepath)
                    if os.path.getsize(filepath) > 0:
                        logger.info(f"XML baixado com sucesso usando urllib: {filepath}")
                        return filepath
                except Exception as e2:
                    logger.error(f"Erro ao baixar XML com urllib: {e2}")
            
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao baixar arquivo: {e}")
            return None
    
    def baixar_fatura(self, fatura, agent, time_period):
        """
        Baixa todos os arquivos relacionados a uma fatura
        
        Args:
            fatura (dict): Dicionário com informações da fatura
            agent (str): Código do agente
            time_period (str): Período de tempo
            
        Returns:
            dict: Dicionário com os caminhos dos arquivos baixados
        """
        try:
            transmissora = fatura['transmissora']
            numero_fatura = fatura['numero_fatura'].strip()
            links = fatura['links']
            
            # Para LNT, usamos um código fixo
            codigo_transmissora = "1143"
            nome_transmissora = transmissora
            
            # Determinar o diretório principal
            if agent in TRANSMISSORAS:
                # Usar o diretório do agente
                nome_pasta_principal = TRANSMISSORAS[agent]
                dir_principal = os.path.join(self.download_dir, nome_pasta_principal)
            else:
                # Usar o método criar_diretorio_transmissora como fallback
                dir_principal = self.criar_diretorio_transmissora(codigo_transmissora, transmissora)
            
            # Garantir que o diretório principal existe
            if not os.path.exists(dir_principal):
                os.makedirs(dir_principal)
                logger.info(f"Diretório principal criado: {dir_principal}")
            
            # Criar uma subpasta para a transmissora específica
            nome_pasta_transmissora = f"{codigo_transmissora} - {nome_transmissora}"
            # Remover caracteres inválidos para nomes de pasta
            nome_pasta_transmissora = re.sub(r'[<>:"/\\|?*]', '', nome_pasta_transmissora)
            dir_transmissora = os.path.join(dir_principal, nome_pasta_transmissora)
            
            # Garantir que o diretório da transmissora existe
            if not os.path.exists(dir_transmissora):
                os.makedirs(dir_transmissora)
                logger.info(f"Diretório para transmissora {nome_pasta_transmissora} criado: {dir_transmissora}")
            
            # Criar nome base para os arquivos
            nome_base = f"{codigo_transmissora}_{numero_fatura}_{time_period}"
            nome_base = re.sub(r'[^\w\s-]', '', nome_base).strip().replace(' ', '_')
            
            arquivos_baixados = {}
            
            # Baixar XML
            if 'xml' in links:
                nome_arquivo = f"{nome_base}_XML"
                arquivo_xml = self.baixar_arquivo(links['xml'], nome_arquivo, dir_transmissora)
                if arquivo_xml:
                    arquivos_baixados['xml'] = arquivo_xml
            
            # Baixar DANFE
            if 'danfe' in links:
                nome_arquivo = f"{nome_base}_DANFE"
                arquivo_danfe = self.baixar_arquivo(links['danfe'], nome_arquivo, dir_transmissora)
                if arquivo_danfe:
                    arquivos_baixados['danfe'] = arquivo_danfe
            
            # Baixar Boletos (podem ser até 3)
            for i in range(1, 4):
                boleto_key = f'boleto_{i}'
                if boleto_key in links:
                    nome_arquivo = f"{nome_base}_BOLETO_{i}"
                    arquivo_boleto = self.baixar_arquivo(links[boleto_key], nome_arquivo, dir_transmissora)
                    if arquivo_boleto:
                        arquivos_baixados[boleto_key] = arquivo_boleto
            
            logger.info(f"Fatura {numero_fatura} baixada com sucesso: {len(arquivos_baixados)} arquivos")
            return arquivos_baixados
        except Exception as e:
            logger.error(f"Erro ao baixar fatura: {e}")
            return {}
    
    def baixar_faturas_periodo(self, agent, time_period):
        """
        Baixa todas as faturas de um período específico
        
        Args:
            agent (str): Código do agente
            time_period (str): Período de tempo
            
        Returns:
            int: Número de faturas baixadas
        """
        try:
            logger.info(f"Iniciando download de faturas para o agente {agent} no período {time_period}")
            
            # Acessar página
            html_content = self.acessar_site(agent, time_period)
            if not html_content:
                logger.error(f"Não foi possível acessar a página. Encerrando.")
                return 0
            
            # Extrair links das faturas
            faturas = self.extrair_links_faturas(html_content)
            if not faturas:
                logger.warning(f"Nenhuma fatura encontrada no período {time_period}.")
                return 0
            
            total_faturas_baixadas = 0
            
            # Baixar cada fatura
            for fatura in faturas:
                arquivos = self.baixar_fatura(fatura, agent, time_period)
                if arquivos:
                    total_faturas_baixadas += 1
                
                # Pequena pausa entre downloads para evitar sobrecarga no servidor
                time.sleep(1)
            
            logger.info(f"Download concluído para o período {time_period}. Total de faturas baixadas: {total_faturas_baixadas}")
            return total_faturas_baixadas
        except Exception as e:
            logger.error(f"Erro durante o download de faturas para o período {time_period}: {e}")
            return 0
    
    def baixar_faturas_multiplos_periodos(self, agent, periodos):
        """
        Baixa faturas para múltiplos períodos
        
        Args:
            agent (str): Código do agente
            periodos (list): Lista de períodos (ex: ['202502', '202501'])
            
        Returns:
            dict: Dicionário com o número de faturas baixadas por período
        """
        resultados = {}
        
        for periodo in periodos:
            print(f"\nProcessando período: {periodo}")
            faturas_baixadas = self.baixar_faturas_periodo(agent, periodo)
            resultados[periodo] = faturas_baixadas
            
            # Pausa entre períodos
            time.sleep(3)
        
        return resultados
    
    def baixar_faturas_multiplos_agentes(self, agentes, periodo):
        """
        Baixa faturas para múltiplos agentes em um único período
        
        Args:
            agentes (list): Lista de códigos de agentes
            periodo (str): Período (ex: '202502')
            
        Returns:
            dict: Dicionário com o número de faturas baixadas por agente
        """
        resultados = {}
        total_faturas = 0
        
        for agent in agentes:
            print(f"\nProcessando agente: {agent} ({TRANSMISSORAS.get(agent, 'Desconhecido')})")
            faturas_baixadas = self.baixar_faturas_periodo(agent, periodo)
            resultados[agent] = faturas_baixadas
            total_faturas += faturas_baixadas
            
            # Pausa entre agentes
            time.sleep(2)
        
        return resultados, total_faturas


if __name__ == "__main__":
    print("=" * 50)
    print("SIGET PLUS - Download de Faturas de Empresas Eólicas")
    print("=" * 50)
    print("Este script baixa faturas do site da Siget Plus para empresas eólicas")
    print("As faturas serão organizadas em pastas separadas para cada empresa")
    print(f"Diretório base: C:\\Users\\Bruno\\Downloads\\TUST\\LNT\\DE")
    print("=" * 50)
    
    # Caminho para o executável do wkhtmltopdf
    wkhtmltopdf_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    
    # Verificar se o wkhtmltopdf existe
    if not os.path.exists(wkhtmltopdf_path):
        print(f"AVISO: wkhtmltopdf não encontrado em {wkhtmltopdf_path}")
        print("A conversão de HTML para PDF não estará disponível.")
        print("Os boletos em formato HTML serão salvos como HTML.")
        wkhtmltopdf_path = None
    
    # Criar o downloader com o caminho específico
    download_dir = "C:\\Users\\Bruno\\Downloads\\TUST\\LNT\\DE"
    downloader = SigetPlusDownloader(
        download_dir=download_dir,
        wkhtmltopdf_path=wkhtmltopdf_path
    )
    
    # Mostrar empresas disponíveis
    print("\nEmpresas disponíveis:")
    print("-" * 30)
    print("Código | Nome")
    print("-" * 30)
    for codigo, nome in TRANSMISSORAS.items():
        print(f"{codigo:6} | {nome}")
    print("-" * 30)
    
    # Configurar para baixar de todas as empresas automaticamente
    agentes = list(TRANSMISSORAS.keys())
    print(f"\nBaixando faturas para todas as {len(agentes)} empresas.")
    
    # Perguntar se deseja baixar para um período específico ou para os últimos N períodos
    opcao = input("\nDeseja baixar para um período específico (1) ou para os últimos N períodos (2)? ")
    
    if opcao == "1":
        # Solicitar período
        periodo = input("Digite o período desejado (formato AAAAMM, ex: 202502 para fevereiro de 2025): ")
        
        # Processar múltiplos agentes
        print(f"\nIniciando download para {len(agentes)} agentes no período {periodo}...")
        resultados, total_faturas = downloader.baixar_faturas_multiplos_agentes(agentes, periodo)
        
        # Exibir resumo
        print("\n" + "=" * 50)
        print("RESUMO DO DOWNLOAD")
        print("=" * 50)
        for agente, total in resultados.items():
            print(f"Agente {agente} ({TRANSMISSORAS.get(agente, 'Desconhecido')}): {total} faturas")
        print("-" * 50)
        print(f"Total geral: {total_faturas} faturas")
    
    elif opcao == "2":
        # Solicitar número de períodos
        num_periodos = int(input("Digite o número de períodos recentes que deseja baixar: "))
        
        # Gerar lista de períodos
        periodos = []
        data_atual = datetime.now()
        ano = data_atual.year
        mes = data_atual.month
        
        for i in range(num_periodos):
            periodo = f"{ano}{mes:02d}"
            periodos.append(periodo)
            
            # Mês anterior
            mes -= 1
            if mes == 0:
                mes = 12
                ano -= 1
        
        print(f"\nPeríodos selecionados: {', '.join(periodos)}")
        
        # Processar múltiplos agentes para múltiplos períodos
        print(f"\nProcessando {len(agentes)} agentes para {len(periodos)} períodos...")
        
        total_geral = 0
        resultados_completos = {}
        
        for periodo in periodos:
            print(f"\n--- Processando período: {periodo} ---")
            resultados, total = downloader.baixar_faturas_multiplos_agentes(agentes, periodo)
            resultados_completos[periodo] = resultados
            total_geral += total
        
        # Exibir resumo
        print("\n" + "=" * 50)
        print("RESUMO DO DOWNLOAD")
        print("=" * 50)
        
        for periodo, resultados in resultados_completos.items():
            print(f"\nPeríodo {periodo}:")
            periodo_total = 0
            for agente, total in resultados.items():
                print(f"  Agente {agente} ({TRANSMISSORAS.get(agente, 'Desconhecido')}): {total} faturas")
                periodo_total += total
            print(f"  Total do período: {periodo_total} faturas")
        
        print("-" * 50)
        print(f"Total geral: {total_geral} faturas")
    
    else:
        print("Opção inválida. Encerrando.")
    
    # Mostrar onde os arquivos foram salvos
    print(f"\nAs faturas foram salvas em: {os.path.abspath(download_dir)}")
    
    print("\nPressione Enter para sair...")
    input()