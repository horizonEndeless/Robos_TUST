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
        logging.FileHandler("sigetplus_downloader.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("SigetPlusDownloader")

# Mapeamento de códigos para nomes de transmissoras
TRANSMISSORAS = {
    "3748": "DE",
}

class SigetPlusDownloader:
    """
    Classe para baixar faturas do site da Siget Plus (https://sys.sigetplus.com.br/cobranca/)
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
            self.download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "TUST", "TAESA")
        
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
    
    def acessar_site(self, agent, time_period, page=1):
        """
        Acessa o site de faturas da Siget Plus
        
        Args:
            agent (str): Código do agente (ex: 8011)
            time_period (str): Período de tempo (ex: 202502 para fevereiro de 2025)
            page (int): Número da página
            
        Returns:
            str: Conteúdo HTML da página
        """
        try:
            # Construir URL com parâmetros
            timestamp = int(datetime.now().timestamp() * 1000)
            url = f"{self.base_url}/company/30/invoices"
            params = {
                "agent": agent,
                "time": time_period,
                "page": page,
                "_": timestamp
            }
            
            logger.info(f"Acessando página {page} para o agente {agent} no período {time_period}...")
            response = self.session.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            
            logger.info(f"Página {page} acessada com sucesso. Status code: {response.status_code}")
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
            
            for linha in linhas:
                try:
                    # Extrair informações da fatura
                    colunas = linha.find_all('td')  # Usando find_all em vez de select
                    if len(colunas) < 8:
                        logger.warning(f"Linha com número insuficiente de colunas: {len(colunas)}")
                        continue
                    
                    transmissora = colunas[0].text.strip()
                    numero_fatura = colunas[1].text.strip()
                    
                    # Links
                    links = {}
                    
                    # Link da fatura
                    link_fatura_elem = colunas[1].find('a')
                    if link_fatura_elem and link_fatura_elem.has_attr('href'):
                        links['fatura'] = link_fatura_elem['href']
                    
                    # Link do boleto
                    link_boleto_elem = colunas[4].find('a')
                    if link_boleto_elem and link_boleto_elem.has_attr('href'):
                        links['boleto'] = link_boleto_elem['href']
                    
                    # Link do XML
                    link_xml_elem = colunas[7].find('a', class_='btn-primary')
                    if link_xml_elem and link_xml_elem.has_attr('href'):
                        links['xml'] = link_xml_elem['href']
                    
                    # Link do DANFE
                    link_danfe_elem = colunas[7].find('a', class_='btn-info')
                    if link_danfe_elem and link_danfe_elem.has_attr('href'):
                        links['danfe'] = link_danfe_elem['href']
                    
                    # Adicionar à lista de faturas apenas se tiver pelo menos um link
                    if links:
                        faturas.append({
                            'transmissora': transmissora,
                            'numero_fatura': numero_fatura,
                            'links': links
                        })
                        logger.info(f"Fatura encontrada: {transmissora} - {numero_fatura}")
                    
                except Exception as e:
                    logger.error(f"Erro ao extrair informações da linha: {e}")
                    continue
            
            logger.info(f"Encontradas {len(faturas)} faturas na página")
            return faturas
        except Exception as e:
            logger.error(f"Erro ao extrair links de faturas: {e}")
            return []
    
    def verificar_proxima_pagina(self, html_content):
        """
        Verifica se existe uma próxima página
        
        Args:
            html_content (str): Conteúdo HTML da página
            
        Returns:
            bool: True se existe próxima página, False caso contrário
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            next_link = soup.select('ul.pagination li a[rel="next"]')
            
            return len(next_link) > 0
        except Exception as e:
            logger.error(f"Erro ao verificar próxima página: {e}")
            return False
    
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
            
            response = self.session.get(url, headers=self.headers, stream=True)
            response.raise_for_status()
            
            # Determinar extensão do arquivo
            if url.endswith('.xml'):
                extensao = '.xml'
            elif 'danfe' in url.lower():
                extensao = '.pdf'
            elif 'billet' in url.lower():
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
            
            # Se for HTML e tivermos wkhtmltopdf configurado, converter para PDF
            if extensao == '.html' and 'boleto' in nome_arquivo.lower() and self.pdf_config:
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
            
            # Extrair o código e nome da transmissora
            partes_transmissora = transmissora.split(' - ')
            codigo_transmissora = partes_transmissora[0].strip()
            nome_transmissora = transmissora
            if len(partes_transmissora) > 1:
                nome_transmissora = partes_transmissora[1].strip()
            
            # Determinar o diretório principal (SJP1, LIBRA, etc.)
            if agent in TRANSMISSORAS:
                # Usar o diretório do agente
                nome_pasta_principal = TRANSMISSORAS[agent]
                dir_principal = os.path.join(self.download_dir, nome_pasta_principal)
            else:
                # Usar o método criar_diretorio_transmissora como fallback para determinar a pasta principal
                dir_principal = self.criar_diretorio_transmissora(codigo_transmissora, transmissora)
            
            # Garantir que o diretório principal existe
            if not os.path.exists(dir_principal):
                os.makedirs(dir_principal)
                logger.info(f"Diretório principal criado: {dir_principal}")
            
            # Criar uma subpasta para a transmissora específica
            # Usar o código e nome da transmissora para nomear a pasta
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
            
            # Baixar Boleto
            if 'boleto' in links:
                nome_arquivo = f"{nome_base}_BOLETO"
                arquivo_boleto = self.baixar_arquivo(links['boleto'], nome_arquivo, dir_transmissora)
                if arquivo_boleto:
                    arquivos_baixados['boleto'] = arquivo_boleto
            
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
            
            pagina = 1
            tem_proxima_pagina = True
            total_faturas_baixadas = 0
            
            while tem_proxima_pagina:
                # Acessar página
                html_content = self.acessar_site(agent, time_period, pagina)
                if not html_content:
                    logger.error(f"Não foi possível acessar a página {pagina}. Encerrando.")
                    break
                
                # # Salvar HTML para debug
                # debug_dir = os.path.join(self.download_dir, "debug")
                # if not os.path.exists(debug_dir):
                #     os.makedirs(debug_dir)
                # debug_file = os.path.join(debug_dir, f"debug_page_{time_period}_p{pagina}.html")
                # with open(debug_file, 'w', encoding='utf-8') as f:
                #     f.write(html_content)
                # logger.info(f"HTML da página {pagina} salvo para debug em: {debug_file}")
                
                # Extrair links das faturas
                faturas = self.extrair_links_faturas(html_content)
                if not faturas:
                    logger.warning(f"Nenhuma fatura encontrada na página {pagina}.")
                    break
                
                # Baixar cada fatura
                for fatura in faturas:
                    arquivos = self.baixar_fatura(fatura, agent, time_period)
                    if arquivos:
                        total_faturas_baixadas += 1
                    
                    # Pequena pausa entre downloads para evitar sobrecarga no servidor
                    time.sleep(1)
                
                # Verificar se existe próxima página
                tem_proxima_pagina = self.verificar_proxima_pagina(html_content)
                if tem_proxima_pagina:
                    pagina += 1
                    # Pausa entre páginas
                    time.sleep(2)
                else:
                    logger.info(f"Não há mais páginas para o período {time_period}")
            
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
    print("SIGET PLUS - Download de Faturas da Taesa")
    print("=" * 50)
    print("Este script baixa faturas do site da Siget Plus (https://sys.sigetplus.com.br/cobranca/)")
    print("As faturas serão organizadas em pastas separadas para cada empresa (LIBRA, SJP1, etc.)")
    print(f"Diretório base: C:\\Users\\Bruno\\Downloads\\TUST\\TAESA")
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
    download_dir = "C:\\Users\\Bruno\\Downloads\\TUST\\TAESA"
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
    print("0      | Todas as empresas")
    print("-" * 30)
    
    # Perguntar qual empresa deseja baixar
    empresa_opcao = input("\nDigite o código da empresa que deseja baixar (ou 0 para todas): ")
    
    # Definir agentes a serem processados
    agentes = []
    if empresa_opcao == "0":
        # Todas as empresas
        agentes = list(TRANSMISSORAS.keys())
        print(f"\nBaixando faturas para todas as {len(agentes)} empresas.")
    elif empresa_opcao in TRANSMISSORAS:
        # Empresa específica
        agentes = [empresa_opcao]
        print(f"\nBaixando faturas para a empresa {TRANSMISSORAS[empresa_opcao]} (código {empresa_opcao}).")
    else:
        print(f"Código de empresa inválido: {empresa_opcao}. Encerrando.")
        input("\nPressione Enter para sair...")
        exit()
    
    # Perguntar se deseja baixar para um período específico ou para múltiplos períodos
    opcao = input("\nDeseja baixar para um período específico (1) ou para os últimos N períodos (2)? ")
    
    if opcao == "1":
        # Solicitar período
        periodo = input("Digite o período desejado (formato AAAAMM, ex: 202502 para fevereiro de 2025): ")
        
        # Processar cada agente
        if len(agentes) > 1:
            print(f"\nIniciando download para {len(agentes)} agentes no período {periodo}...")
            resultados, total_geral = downloader.baixar_faturas_multiplos_agentes(agentes, periodo)
            
            # Exibir resumo
            print("\n" + "=" * 50)
            print("RESUMO DO DOWNLOAD")
            print("=" * 50)
            for agent, total in resultados.items():
                nome_agente = TRANSMISSORAS.get(agent, agent)
                print(f"Agente {agent} ({nome_agente}): {total} faturas")
            print("-" * 50)
            print(f"Total geral: {total_geral} faturas")
        else:
            # Apenas um agente
            agent = agentes[0]
            print(f"\nIniciando download para o agente {agent} ({TRANSMISSORAS.get(agent, 'Desconhecido')}) no período {periodo}...")
            faturas_baixadas = downloader.baixar_faturas_periodo(agent, periodo)
            print(f"Download concluído para o agente {agent}. Total de faturas baixadas: {faturas_baixadas}")
            total_geral = faturas_baixadas
        
        print(f"\nDownload concluído para todos os agentes. Total geral de faturas baixadas: {total_geral}")
    
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
        
        # Processar cada agente
        resultados_totais = {}
        total_geral = 0
        
        # Contador para mostrar progresso
        total_combinacoes = len(agentes) * len(periodos)
        combinacao_atual = 0
        
        for agent in agentes:
            print(f"\nProcessando agente: {agent} ({TRANSMISSORAS.get(agent, 'Desconhecido')})")
            resultados = downloader.baixar_faturas_multiplos_periodos(agent, periodos)
            
            # Acumular resultados
            for periodo, total in resultados.items():
                if periodo not in resultados_totais:
                    resultados_totais[periodo] = 0
                resultados_totais[periodo] += total
                total_geral += total
                
                # Atualizar progresso
                combinacao_atual += 1
                percentual = (combinacao_atual / total_combinacoes) * 100
                print(f"Progresso: {percentual:.1f}% ({combinacao_atual}/{total_combinacoes})")
        
        # Exibir resumo
        print("\n" + "=" * 50)
        print("RESUMO DO DOWNLOAD")
        print("=" * 50)
        for periodo, total in resultados_totais.items():
            print(f"Período {periodo}: {total} faturas")
        print("-" * 50)
        print(f"Total geral: {total_geral} faturas")
    
    else:
        print("Opção inválida. Encerrando.")
    
    # Mostrar onde os arquivos foram salvos
    print(f"\nAs faturas foram salvas em: {os.path.abspath(download_dir)}")
    print("Organizadas nas seguintes pastas:")
    
    # Mostrar a estrutura de pastas
    for codigo, nome in TRANSMISSORAS.items():
        pasta_principal = os.path.join(download_dir, nome)
        if os.path.exists(pasta_principal):
            # Contar subpastas (transmissoras)
            subpastas = [d for d in os.listdir(pasta_principal) if os.path.isdir(os.path.join(pasta_principal, d))]
            num_transmissoras = len(subpastas)
            
            # Contar total de arquivos em todas as subpastas
            total_arquivos = 0
            for subpasta in subpastas:
                caminho_subpasta = os.path.join(pasta_principal, subpasta)
                num_arquivos = len([f for f in os.listdir(caminho_subpasta) if os.path.isfile(os.path.join(caminho_subpasta, f))])
                total_arquivos += num_arquivos
            
            print(f"- {nome}: {num_transmissoras} transmissoras, {total_arquivos} arquivos")
            
            # Mostrar detalhes de cada transmissora (opcional, pode ser comentado se ficar muito verboso)
            for subpasta in subpastas:
                caminho_subpasta = os.path.join(pasta_principal, subpasta)
                num_arquivos = len([f for f in os.listdir(caminho_subpasta) if os.path.isfile(os.path.join(caminho_subpasta, f))])
                print(f"  └── {subpasta}: {num_arquivos} arquivos")
    
    print("\nPressione Enter para sair...")
    input()
