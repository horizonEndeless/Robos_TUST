import requests
from bs4 import BeautifulSoup
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import shutil
import re  # Adicionando o import do módulo re

class CEMIGDownloader:
    def __init__(self, download_path=None, headless=False):
        """
        Inicializa o downloader da CEMIG
        
        Args:
            download_path: Caminho para salvar os arquivos baixados
            headless: Se True, executa o Chrome em modo headless (sem interface gráfica)
        """
        # Definir o caminho de download padrão se não for especificado
        if download_path is None:
            download_path = r"C:\Users\Bruno\Downloads\TUST\CEMIG"
        
        self.download_path = download_path
        
        # Garantir que o diretório de download exista
        os.makedirs(self.download_path, exist_ok=True)
        
        # Criar pastas para cada transmissora
        self.pasta_cemig = os.path.join(self.download_path, "CEMIG")
        self.pasta_centrooeste = os.path.join(self.download_path, "CENTROOESTE")
        self.pasta_setelagoas = os.path.join(self.download_path, "SETELAGOAS")
        
        os.makedirs(self.pasta_cemig, exist_ok=True)
        os.makedirs(self.pasta_centrooeste, exist_ok=True)
        os.makedirs(self.pasta_setelagoas, exist_ok=True)
        
        # Configurar o Chrome para baixar arquivos automaticamente para o diretório especificado
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option("prefs", {
            "download.default_directory": self.download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        
        # Configurar modo headless se solicitado
        if headless:
            self.chrome_options.add_argument("--headless")
            self.chrome_options.add_argument("--window-size=1920,1080")
        
        # Inicializar o driver do Chrome
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.base_url = "https://web.cemig.com.br/frbe"
        
    def iniciar_sessao(self):
        """Inicia a sessão no site da CEMIG"""
        try:
            self.driver.get(self.base_url)
            print("Sessão iniciada com sucesso")
            return True
        except Exception as e:
            print(f"Erro ao iniciar sessão: {e}")
            return False
    
    def verificar_javascript(self):
        """Verifica se o JavaScript está sendo executado corretamente"""
        try:
            # Tentar executar um JavaScript simples
            resultado = self.driver.execute_script("return document.readyState")
            print(f"Estado do documento: {resultado}")
            
            # Verificar se a função VisualizarArquivo existe
            existe_funcao = self.driver.execute_script("return typeof VisualizarArquivo !== 'undefined'")
            if existe_funcao:
                print("Função VisualizarArquivo encontrada!")
            else:
                print("Função VisualizarArquivo NÃO encontrada.")
            
            return True
        except Exception as e:
            print(f"Erro ao verificar JavaScript: {e}")
            return False
    
    def pesquisar_empresa(self, codigo_empresa):
        """Pesquisa a empresa pelo código ONS"""
        try:
            # Encontrar o campo de entrada e inserir o código
            input_ons = self.driver.find_element(By.ID, "ONS")
            input_ons.clear()
            input_ons.send_keys(codigo_empresa)
            
            print(f"Inserido código da empresa: {codigo_empresa}")
            
            # Verificar o elemento de loading
            loading_element = self.driver.find_element(By.ID, "loading")
            print(f"Estado inicial do loading: {loading_element.get_attribute('style')}")
            
            # Clicar no botão de pesquisa
            botao_pesquisar = self.driver.find_element(By.ID, "btnPesquisar")
            botao_pesquisar.click()
            
            print("Botão de pesquisa clicado, aguardando carregamento...")
            
            # Aguardar que o elemento de loading apareça
            try:
                WebDriverWait(self.driver, 10).until(
                    lambda driver: "display: none" not in driver.find_element(By.ID, "loading").get_attribute("style")
                )
                print("Loading visível, aguardando processamento...")
            except Exception as e:
                print(f"Elemento de loading não ficou visível: {e}")
                print("Tentando continuar mesmo assim...")
            
            # Aguardar que o elemento de loading desapareça - COM TEMPO MAIOR
            max_espera = 60  # Aumentar para 60 segundos
            print(f"Aguardando até {max_espera} segundos para o processamento terminar...")
            
            try:
                WebDriverWait(self.driver, max_espera).until(
                    lambda driver: "display: none" in driver.find_element(By.ID, "loading").get_attribute("style")
                )
                print("Processamento concluído! Loading desapareceu.")
            except Exception as e:
                print(f"Timeout esperando o loading desaparecer: {e}")
                print("Verificando estado atual do loading...")
                
                try:
                    loading_atual = self.driver.find_element(By.ID, "loading").get_attribute("style")
                    print(f"Estado atual do loading: {loading_atual}")
                    
                    if "display: none" in loading_atual:
                        print("Loading está invisível agora, podemos continuar.")
                    else:
                        print("Loading ainda está visível, mas vamos tentar continuar...")
                        
                        # Tentar forçar o loading a desaparecer via JavaScript
                        self.driver.execute_script("document.getElementById('loading').style.display = 'none';")
                        print("Forçado loading a desaparecer via JavaScript")
                except Exception as load_err:
                    print(f"Erro ao verificar loading: {load_err}")
            
            # Aguardar um tempo fixo para garantir
            print("Aguardando 5 segundos adicionais...")
            time.sleep(5)
            
            # Verificar se a div contentAjax foi preenchida
            content_ajax = self.driver.find_element(By.CLASS_NAME, "contentAjax")
            content_html = content_ajax.get_attribute("innerHTML").strip()
            
            print(f"Conteúdo da div contentAjax: {len(content_html)} caracteres")
            
            if len(content_html) < 10:  # Se estiver praticamente vazia
                print("A div contentAjax parece vazia. Tentando abordagem alternativa...")
                
                # Tentar executar o JavaScript diretamente com token de verificação
                try:
                    # Obter o token de verificação
                    token = self.driver.execute_script("""
                        return $('input[name="__RequestVerificationToken"]').val();
                    """)
                    
                    print(f"Token de verificação: {token[:10]}...")
                    
                    # Reenviar a requisição AJAX manualmente com o token
                    ajax_result = self.driver.execute_script("""
                        var result;
                        $.ajax({
                            url: '/FRBE/Home/Pesquisar',
                            type: 'POST',
                            data: { 
                                ONS: arguments[0],
                                __RequestVerificationToken: arguments[1]
                            },
                            async: false,
                            success: function(data) {
                                result = data;
                                $('.contentAjax').html(data);
                            }
                        });
                        return result;
                    """, codigo_empresa, token)
                    
                    print("Requisição AJAX executada manualmente com token")
                    
                    # Aguardar um pouco mais
                    time.sleep(5)
                    
                    # Verificar novamente o conteúdo
                    content_ajax = self.driver.find_element(By.CLASS_NAME, "contentAjax")
                    content_html = content_ajax.get_attribute("innerHTML").strip()
                    print(f"Novo conteúdo da div contentAjax: {len(content_html)} caracteres")
                except Exception as ajax_error:
                    print(f"Erro ao executar AJAX manualmente: {ajax_error}")
                    
                    # Tentar uma abordagem mais direta - recarregar a página e tentar novamente
                    print("Tentando abordagem mais direta...")
                    
                    # Recarregar a página
                    self.driver.refresh()
                    time.sleep(3)
                    
                    # Encontrar o campo de entrada e inserir o código novamente
                    input_ons = self.driver.find_element(By.ID, "ONS")
                    input_ons.clear()
                    input_ons.send_keys(codigo_empresa)
                    
                    # Clicar no botão de pesquisa novamente
                    botao_pesquisar = self.driver.find_element(By.ID, "btnPesquisar")
                    botao_pesquisar.click()
                    
                    # Aguardar mais tempo
                    print("Aguardando 20 segundos após nova tentativa...")
                    time.sleep(20)
                    
                    # Verificar novamente o conteúdo
                    content_ajax = self.driver.find_element(By.CLASS_NAME, "contentAjax")
                    content_html = content_ajax.get_attribute("innerHTML").strip()
                    print(f"Conteúdo após nova tentativa: {len(content_html)} caracteres")
            
            # Verificar se há links de download
            links = self.driver.find_elements(By.TAG_NAME, "a")
            links_download = [link for link in links if "VisualizarArquivo" in (link.get_attribute("onclick") or "")]
            
            print(f"Encontrados {len(links_download)} links de download")
            
            if not links_download:
                print("Nenhum link de download encontrado. Tentando uma última abordagem...")
                
                # Salvar screenshot para diagnóstico
                screenshot_path = os.path.join(self.download_path, f"sem_links_{codigo_empresa}.png")
                self.driver.save_screenshot(screenshot_path)
                print(f"Screenshot salvo em: {screenshot_path}")
                
                # Salvar HTML para diagnóstico
                with open(os.path.join(self.download_path, f"pagina_sem_links_{codigo_empresa}.html"), "w", encoding="utf-8") as f:
                    f.write(self.driver.page_source)
                
                # Tentar uma abordagem completamente diferente - acessar diretamente a URL de resultados
                try:
                    # Construir uma URL direta para os resultados
                    resultado_url = f"{self.base_url}/Home/Resultado?ons={codigo_empresa}"
                    print(f"Tentando acessar diretamente: {resultado_url}")
                    
                    self.driver.get(resultado_url)
                    time.sleep(10)
                    
                    # Verificar novamente se há links
                    links = self.driver.find_elements(By.TAG_NAME, "a")
                    links_download = [link for link in links if "VisualizarArquivo" in (link.get_attribute("onclick") or "")]
                    print(f"Após acesso direto: Encontrados {len(links_download)} links de download")
                    
                    if links_download:
                        print("Links encontrados após acesso direto!")
                        
                        # Salvar a página de resultados para análise
                        with open(os.path.join(self.download_path, f"resultados_direto_{codigo_empresa}.html"), "w", encoding="utf-8") as f:
                            f.write(self.driver.page_source)
                        
                        return True
                except Exception as direct_error:
                    print(f"Erro ao tentar acesso direto: {direct_error}")
                
                return False
            
            # Salvar a página de resultados para análise
            with open(os.path.join(self.download_path, f"resultados_{codigo_empresa}.html"), "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            
            print(f"Pesquisa para empresa {codigo_empresa} realizada com sucesso")
            return True
        except Exception as e:
            print(f"Erro ao pesquisar empresa: {e}")
            
            # Salvar screenshot para diagnóstico
            screenshot_path = os.path.join(self.download_path, f"erro_{codigo_empresa}.png")
            self.driver.save_screenshot(screenshot_path)
            print(f"Screenshot salvo em: {screenshot_path}")
            
            return False
    
    def baixar_arquivos(self, tipo_arquivo=None):
        """Baixa os arquivos encontrados na página de resultados"""
        try:
            # Encontrar todos os links com VisualizarArquivo na página
            links = self.driver.find_elements(By.TAG_NAME, "a")
            links_download = [link for link in links if "VisualizarArquivo" in (link.get_attribute("onclick") or "")]
            
            print(f"Encontrados {len(links_download)} links de download")
            
            if not links_download:
                print("Nenhum link de download encontrado.")
                return False
            
            # Dicionário para mapear nomes de arquivos para textos dos links
            self.mapeamento_arquivos = {}
            
            # Contador para acompanhar os downloads
            downloads_realizados = 0
            arquivos_baixados = []
            
            for link in links_download:
                texto_link = link.text.strip()
                onclick = link.get_attribute("onclick")
                
                # Verificar se o link corresponde ao tipo de arquivo desejado
                if tipo_arquivo:
                    if tipo_arquivo.lower() == "boleto" and "boleto" not in texto_link.lower():
                        continue
                    elif tipo_arquivo.lower() == "xml" and "xml" not in texto_link.lower():
                        continue
                    elif tipo_arquivo.lower() == "danfe" and "danfe" not in texto_link.lower():
                        continue
                
                # Extrair o nome do arquivo do atributo onclick
                match = re.search(r'VisualizarArquivo\("([^"]+)"\)', onclick)
                if match:
                    nome_arquivo = match.group(1)
                    print(f"Tentando baixar: {nome_arquivo}")
                    print(f"Texto do link: {texto_link}")
                    
                    # Armazenar o mapeamento entre nome do arquivo e texto do link
                    self.mapeamento_arquivos[nome_arquivo] = texto_link
                    
                    # Rolar até o link para garantir que está visível
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", link)
                    time.sleep(0.5)  # Pequena pausa após rolagem
                    
                    # Clicar no link para iniciar o download
                    link.click()
                    
                    # Aguardar um tempo para o download iniciar
                    time.sleep(3)
                    
                    downloads_realizados += 1
                    arquivos_baixados.append(nome_arquivo)
            
            # Aguardar um tempo para os downloads concluírem
            if downloads_realizados > 0:
                print(f"Aguardando a conclusão de {downloads_realizados} downloads...")
                tempo_espera = 5 * downloads_realizados  # 5 segundos por arquivo
                print(f"Aguardando {tempo_espera} segundos...")
                time.sleep(tempo_espera)
                print("Downloads concluídos")
                
                # Organizar os arquivos baixados em pastas por transmissora
                self.organizar_arquivos_por_transmissora()
                
                return arquivos_baixados
            else:
                print("Nenhum arquivo encontrado para download")
                return False
            
        except Exception as e:
            print(f"Erro ao baixar arquivos: {e}")
            
            # Salvar screenshot para diagnóstico
            screenshot_path = os.path.join(self.download_path, "erro_download.png")
            self.driver.save_screenshot(screenshot_path)
            print(f"Screenshot salvo em: {screenshot_path}")
            
            return False
    
    def organizar_arquivos_por_transmissora(self):
        """Organiza os arquivos baixados em pastas por transmissora"""
        try:
            print("Organizando arquivos por transmissora...")
            
            # Listar todos os arquivos na pasta de download
            arquivos = [f for f in os.listdir(self.download_path) if os.path.isfile(os.path.join(self.download_path, f))]
            
            # Filtrar apenas os arquivos relevantes (PDF e XML)
            arquivos_relevantes = [f for f in arquivos if f.endswith('.pdf') or f.endswith('.xml')]
            
            print(f"Encontrados {len(arquivos_relevantes)} arquivos para organizar")
            
            for arquivo in arquivos_relevantes:
                caminho_origem = os.path.join(self.download_path, arquivo)
                
                print(f"Processando arquivo: {arquivo}")
                
                # Verificar se temos o mapeamento para este arquivo
                nome_transmissora = None
                
                # Primeiro, tentar identificar pelo nome do arquivo baixado
                for nome_original, texto_link in self.mapeamento_arquivos.items():
                    if nome_original in arquivo:
                        print(f"Encontrado mapeamento: {nome_original} -> {texto_link}")
                        
                        # Extrair o nome da transmissora do texto do link
                        if "CEMIG_GT" in texto_link:
                            nome_transmissora = "CEMIG"
                        elif "Centroeste" in texto_link:
                            nome_transmissora = "CENTROOESTE"
                        elif "SeteLagoas" in texto_link:
                            nome_transmissora = "SETELAGOAS"
                        
                        break
                
                # Se não encontrou pelo mapeamento, tentar pelo nome do arquivo
                if nome_transmissora is None:
                    if "_510_" in arquivo:
                        nome_transmissora = "CEMIG"
                    elif "_720_" in arquivo:
                        nome_transmissora = "CENTROOESTE"
                    elif "_740_" in arquivo:
                        nome_transmissora = "SETELAGOAS"
                    elif "CEMIG" in arquivo:
                        nome_transmissora = "CEMIG"
                    elif "Centroeste" in arquivo or "CENTROOESTE" in arquivo:
                        nome_transmissora = "CENTROOESTE"
                    elif "SeteLagoas" in arquivo or "SETELAGOAS" in arquivo:
                        nome_transmissora = "SETELAGOAS"
                
                # Se ainda não identificou, verificar pelo conteúdo do arquivo
                if nome_transmissora is None:
                    print(f"Não foi possível identificar a transmissora para o arquivo: {arquivo}")
                    continue
                
                print(f"Transmissora identificada: {nome_transmissora}")
                
                # Determinar a pasta de destino
                if nome_transmissora == "CEMIG":
                    pasta_destino = self.pasta_cemig
                elif nome_transmissora == "CENTROOESTE":
                    pasta_destino = self.pasta_centrooeste
                elif nome_transmissora == "SETELAGOAS":
                    pasta_destino = self.pasta_setelagoas
                else:
                    print(f"Pasta não identificada para transmissora: {nome_transmissora}")
                    continue
                
                # Determinar o tipo de arquivo
                if arquivo.startswith("B_") or "boleto" in arquivo.lower():
                    tipo = "BOLETO"
                elif arquivo.endswith(".xml"):
                    tipo = "XML"
                elif arquivo.startswith("F_") or "danfe" in arquivo.lower():
                    tipo = "DANFE"
                else:
                    tipo = "OUTRO"
                
                print(f"Tipo de arquivo: {tipo}")
                
                # Manter o nome original para evitar problemas com caracteres especiais
                caminho_destino = os.path.join(pasta_destino, arquivo)
                
                # Mover o arquivo
                try:
                    # Se o arquivo já existir, adicionar timestamp para evitar sobrescrever
                    if os.path.exists(caminho_destino):
                        nome_base, extensao = os.path.splitext(arquivo)
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        novo_nome = f"{nome_base}_{timestamp}{extensao}"
                        caminho_destino = os.path.join(pasta_destino, novo_nome)
                        print(f"Arquivo já existe, usando novo nome: {novo_nome}")
                    
                    print(f"Movendo de {caminho_origem} para {caminho_destino}")
                    shutil.move(caminho_origem, caminho_destino)
                    print(f"Arquivo movido com sucesso para pasta {nome_transmissora}")
                except Exception as move_error:
                    print(f"Erro ao mover arquivo {arquivo}: {move_error}")
                    
                    # Tentar copiar em vez de mover
                    try:
                        print(f"Tentando copiar em vez de mover...")
                        shutil.copy2(caminho_origem, caminho_destino)
                        os.remove(caminho_origem)
                        print(f"Arquivo copiado e original removido com sucesso")
                    except Exception as copy_error:
                        print(f"Erro ao copiar arquivo {arquivo}: {copy_error}")
            
            print("Organização de arquivos concluída")
            
        except Exception as e:
            print(f"Erro ao organizar arquivos: {e}")
            import traceback
            traceback.print_exc()
    
    def baixar_boletos(self):
        """Baixa os boletos encontrados na página de resultados"""
        return self.baixar_arquivos("boleto")
    
    def baixar_xmls(self):
        """Baixa os XMLs encontrados na página de resultados"""
        return self.baixar_arquivos("xml")
    
    def baixar_danfes(self):
        """Baixa os DANFEs encontrados na página de resultados"""
        return self.baixar_arquivos("danfe")
    
    def fechar(self):
        """Fecha o navegador"""
        self.driver.quit()

def baixar_documentos_cemig(codigo_empresa, download_path=None, headless=False):
    """
    Função principal para baixar documentos da CEMIG
    
    Args:
        codigo_empresa: Código ONS da empresa
        download_path: Caminho para salvar os arquivos baixados
        headless: Se True, executa o Chrome em modo headless (sem interface gráfica)
    
    Returns:
        Lista de arquivos baixados ou False em caso de erro
    """
    downloader = CEMIGDownloader(download_path, headless)
    
    try:
        # Iniciar sessão
        if not downloader.iniciar_sessao():
            return False
        
        # Verificar JavaScript
        downloader.verificar_javascript()
        
        # Tentar até 3 vezes
        for tentativa in range(1, 4):
            print(f"\n=== Tentativa {tentativa} de 3 ===\n")
            
            # Pesquisar empresa
            if downloader.pesquisar_empresa(codigo_empresa):
                # Verificar JavaScript novamente após a pesquisa
                downloader.verificar_javascript()
                
                # Aguardar um momento para garantir que a página está completamente carregada
                print("Aguardando 5 segundos para garantir carregamento completo...")
                time.sleep(5)
                
                # Baixar todos os tipos de documentos
                arquivos = downloader.baixar_arquivos()
                if arquivos:
                    print("Download concluído com sucesso!")
                    return arquivos
                else:
                    print(f"Falha no download na tentativa {tentativa}")
                    
                    if tentativa < 3:
                        print("Tentando novamente...")
                        # Recarregar a página para nova tentativa
                        downloader.driver.get(downloader.base_url)
                        # Aguardar mais tempo entre tentativas
                        print(f"Aguardando 10 segundos antes da próxima tentativa...")
                        time.sleep(10)
            else:
                print(f"Falha na pesquisa na tentativa {tentativa}")
                
                if tentativa < 3:
                    print("Tentando novamente...")
                    # Recarregar a página para nova tentativa
                    downloader.driver.get(downloader.base_url)
                    # Aguardar mais tempo entre tentativas
                    print(f"Aguardando 10 segundos antes da próxima tentativa...")
                    time.sleep(10)
        
        return False
    finally:
        # Garantir que o navegador seja fechado mesmo em caso de erro
        downloader.fechar()

if __name__ == "__main__":
    # Exemplo de uso
    codigo_empresa = "4313"  # Código de exemplo mencionado
    arquivos_baixados = baixar_documentos_cemig(codigo_empresa)
    
    if arquivos_baixados:
        print("\nArquivos baixados com sucesso:")
        for arquivo in arquivos_baixados:
            print(f"  - {arquivo}")
    else:
        print("\nFalha ao baixar os arquivos.")
