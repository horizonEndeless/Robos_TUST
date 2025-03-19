import os
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
import re
import urllib.parse
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurações
# Configurações para múltiplas empresas
EMPRESAS = {
    "LIBRA": {
        "username": "faturas.libra@americaenergia.com.br",
        "password": "123@mudar!",
        "download_dir": r"C:\Users\Bruno\Downloads\TUST\ONS\AE\LIBRA",
        "cnpjs": ["10500221000182"]
    },
    "COREMAS": {
        "username": "fatura.coremas@americaenergia.com.br",
        "password": "123@mudar!",
        "download_dir": r"C:\Users\Bruno\Downloads\TUST\ONS\AE\COREMAS",
        "cnpjs": ["14285232000148", "14285242000183", "24342513000149"]
    },
    "SJP": {
        "username": "faturas.sjp@americaenergia.com.br",
        "password": "123@mudar!",
        "download_dir": r"C:\Users\Bruno\Downloads\TUST\ONS\AE\SJP",
        "cnpjs": ["30520122000170", "30432072000179", "30486042000145", 
                  "30425445000184", "30456405000108", "30421756000175"]
    }
}

# Configuração padrão (será substituída durante a execução para cada empresa)
username = EMPRESAS["LIBRA"]["username"]
password = EMPRESAS["LIBRA"]["password"]
download_dir = EMPRESAS["LIBRA"]["download_dir"]

# Adicionar User-Agents para simular navegadores reais
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15"
]

# URLs do sistema SINTEGRE ONS
URL_HOME = "https://sintegre.ons.org.br/"
URL_TRUST = "https://sintegre.ons.org.br/_trust/default.aspx"
URL_POPS = "https://pops.ons.org.br/"
URL_LOGIN = "https://pops.ons.org.br/ons.pop.federation/"
URL_BOLETOS = "https://sintegre.ons.org.br/sites/1/18/paginas/servicos/historico-de-produtos.aspx?produto=Boletos%20do%20EUST"
URL_NOTAS_FISCAIS = "https://sintegre.ons.org.br/sites/1/18/paginas/servicos/historico-de-produtos.aspx?produto=Notas%20Fiscais%20do%20EUST"
URL_BOLETOS_LIST = "https://sintegre.ons.org.br/sites/1/18/_api/web/lists/GetByTitle('Produtos')/getitems?$select=Id,Title,Produto,DataProdutos,FileRef,Periodicidade,PublicarEm,File_x0020_Type,FileLeafRef,Modified,OData__UIVersionString,UniqueId,File,DescricaoProduto/Length&$expand=file"
URL_DOWNLOAD = "https://sintegre.ons.org.br"

# Lista de CNPJs das empresas que precisamos baixar os boletos
CNPJS_ALVO = []
for empresa in EMPRESAS.values():
    CNPJS_ALVO.extend(empresa["cnpjs"])

# Mapeamento de CNPJs para códigos de empresa
CNPJ_TO_CODE = {
    # LIBRA
    "10500221000182": "LIBRA",
    # COREMAS
    "14285232000148": "COR1",
    "14285242000183": "COR2",
    "24342513000149": "COR3",
    # SJP
    "30520122000170": "SJP1",
    "30432072000179": "SJP2",
    "30486042000145": "SJP3",
    "30425445000184": "SJP4",
    "30456405000108": "SJP5",
    "30421756000175": "SJP6"
}

# Normalizar CNPJs (remover pontos, traços, etc.)
CNPJS_ALVO = [re.sub(r'[^0-9]', '', cnpj) for cnpj in CNPJS_ALVO]

# Parâmetros POST
POST_LOGIN_USERNAME = f"username={urllib.parse.quote(username)}&submit.IdentificarUsuario=Avan%C3%A7ar&EstahNaRede=0&QuemEhNaRede="
POST_LOGIN = f"username={urllib.parse.quote(username)}&password={urllib.parse.quote(password)}&submit.Signin=Entrar&CountLogin=0&CDRESolicitarCadastroUrl=https%3A%2F%2Fsintegre.ons.org.br%2Fsites%2Fcadastro&POPAutenticacaoIntegradaUrl=https%3A%2F%2Fpops.ons.org.br%2Fons.pop.federation%2FAzure%2F%3FReturnUrl%3Dhttps%253a%252f%252fpops.ons.org.br%252fons.pop.federation%252fredirect%252f%253fwa%253dwsignin1.0%2526wtrealm%253dhttps%25253a%25252f%25252fsintegre.ons.org.br%25252f_trust%25252fdefault.aspx%2526wctx%253dhttps%25253a%25252f%25252fsintegre.ons.org.br%25252f_layouts%25252f15%25252fAuthenticate.aspx%25253fSource%25253d%2525252F%2526wreply%253dhttps%25253a%25252f%25252fsintegre.ons.org.br%25252f_trust%25252fdefault.aspx&EstahNaRede=0&QuemEhNaRede=&PasswordRecoveryUrl=https%3A%2F%2Fpops.ons.org.br%2Fons.pop.federation%2Fpasswordrecovery%2F%3FReturnUrl%3Dhttps%253a%252f%252fpops.ons.org.br%252fons.pop.federation%252f%253fwa%253dwsignin1.0%2526wtrealm%253dhttps%25253a%25252f%25252fsintegre.ons.org.br%25252f_trust%25252fdefault.aspx%2526wctx%253dhttps%25253a%25252f%25252fsintegre.ons.org.br%25252f_layouts%25252f15%25252fAuthenticate.aspx%25253fSource%25253d%2525252F%2526wreply%253dhttps%25253a%25252f%25252fsintegre.ons.org.br%25252f_trust%25252fdefault.aspx"
POST_BOLETOS_LIST = """{\"query\":{\"ViewXml\":\"<View Scope='RecursiveAll'>\\n    <Query>\\n          <Where>\\n    <And>\\n        <Eq><FieldRef Name='Title'/><Value Type='Text'>Boletos do EUST</Value></Eq>\\n        \\n      <And>\\n        <Gt><FieldRef Name='ID'/><Value Type='Counter'>0</Value></Gt>\\n        <Eq><FieldRef Name='Pasta'/><Value Type='Boolean'>0</Value></Eq>\\n      </And>\\n    </And></Where>\\n          <OrderBy Override=\\\"TRUE\\\">\\n            <FieldRef Name='Periodicidade' Ascending='False' />\\n            <FieldRef Name='PublicarEm' Ascending='False' />\\n          </OrderBy>\\n    </Query>\\n    <RowLimit>50</RowLimit>\\n  </View>\"}}"""

def get_html_input_value(html, input_id):
    """Extrai o valor de um input do HTML"""
    value_delimiter = 'value="'
    name_position = html.find(input_id)
    value_position = html.find(value_delimiter, name_position)
    start_position = value_position + len(value_delimiter)
    end_position = html.find('"', start_position)
    return html[start_position:end_position]

def get_html_value(html, input_id, value_delimiter, value_index_of):
    """Extrai um valor específico do HTML"""
    name_position = html.find(input_id)
    value_position = html.find(value_delimiter, name_position)
    start_position = value_position + len(value_delimiter)
    end_position = html.find(value_index_of, start_position)
    return html[start_position:end_position]

def get_file_name_from_url(url):
    """Extrai o nome do arquivo da URL"""
    return url.split('/')[-1]

def get_competencia_atual():
    """Retorna o mês atual como competência"""
    now = datetime.now()
    # Retorna o primeiro dia do mês atual
    return datetime(now.year, now.month, 1)

def contains_cnpj(text, cnpjs):
    """Verifica se o texto contém algum dos CNPJs da lista"""
    # Remover caracteres não numéricos do texto para comparação
    text_clean = re.sub(r'[^0-9]', '', text)
    
    for cnpj in cnpjs:
        if cnpj in text_clean:
            return True, cnpj
    return False, None

def testar_conexao(session, url, descricao):
    """Testa uma conexão e retorna detalhes da resposta"""
    print(f"\n--- TESTE: {descricao} ---")
    try:
        response = session.get(url)
        print(f"Status: {response.status_code}")
        print(f"URL final: {response.url}")
        print(f"Tamanho da resposta: {len(response.text)} caracteres")
        
        # Verificar se há redirecionamento para login
        if "login" in response.url.lower():
            print("⚠ ALERTA: Redirecionado para página de login!")
        
        # Salvar resposta para análise
        debug_file = os.path.join(download_dir, f"debug_{descricao.lower().replace(' ', '_')}.html")
        with open(debug_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"HTML da resposta salvo em: {debug_file}")
        
        return response
    except Exception as e:
        print(f"Erro no teste: {str(e)}")
        return None

def extrair_tokens_debug(html_content):
    """Extrai e exibe todos os possíveis tokens e valores importantes do HTML"""
    print("\n--- Análise de tokens no HTML ---")
    
    # Lista de possíveis tokens a procurar
    tokens_para_buscar = [
        "FormDigestValue", "SPRequestGuid", "RequestGuid", 
        "X-RequestDigest", "__VIEWSTATE", "__REQUESTDIGEST",
        "odata.metadata", "Bearer", "Authorization"
    ]
    
    for token in tokens_para_buscar:
        if token in html_content:
            print(f"Token '{token}' encontrado no HTML")
            # Tentar extrair o valor usando diferentes delimitadores
            for delimitador_inicio in [':"', '="', ":'", "='", ": '", ": \""]:
                for delimitador_fim in ['"', "'", '",', "',", '";', "';", '\\', '\n']:
                    try:
                        valor = get_html_value(html_content, token, delimitador_inicio, delimitador_fim)
                        if valor and len(valor) > 5:  # Valor significativo
                            print(f"  Valor encontrado: {valor[:30]}...")
                            break
                    except:
                        continue
        else:
            print(f"Token '{token}' NÃO encontrado no HTML")

def wait_for_page_load(driver, timeout=30):
    """Aguarda o carregamento completo da página"""
    old_page = driver.find_element(By.TAG_NAME, 'html')
    yield
    WebDriverWait(driver, timeout).until(EC.staleness_of(old_page))

def download_file(driver, session, url, file_name, download_dir):
    """Baixa um arquivo usando requests e os cookies do Selenium"""
    try:
        # Obter cookies do Selenium
        selenium_cookies = driver.get_cookies()
        
        # Criar sessão requests e adicionar cookies
        for cookie in selenium_cookies:
            session.cookies.set(cookie['name'], cookie['value'])
        
        # Normalizar URL
        if url.startswith('/'):
            url = URL_DOWNLOAD + url
        
        # Baixar o arquivo
        response = session.get(url, stream=True)
        
        if response.status_code == 200:
            file_path = os.path.join(download_dir, file_name)
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            print(f"Arquivo salvo em: {file_path}")
            return True
        else:
            print(f"Erro ao baixar arquivo: {response.status_code}")
            return False
    except Exception as e:
        print(f"Erro ao baixar arquivo: {str(e)}")
        return False

def main():
    global username, password, download_dir
    
    print("Iniciando processo de download de faturas ONS para múltiplas empresas...")
    
    # Iterar sobre cada empresa
    for empresa_nome, empresa_config in EMPRESAS.items():
        try:
            # Atualizar configurações globais para a empresa atual
            username = empresa_config["username"]
            password = empresa_config["password"]
            download_dir = empresa_config["download_dir"]
            cnpjs_empresa = empresa_config["cnpjs"]
            
            # Criar diretório de download se não existir
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)
            
            print(f"\n\n{'='*50}")
            print(f"PROCESSANDO EMPRESA: {empresa_nome}")
            print(f"{'='*50}")
            print(f"Usando usuário: {username}")
            print(f"CNPJs alvo: {cnpjs_empresa}")
            
            # Configurar o Chrome em modo headless
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Executar em segundo plano
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            # Configurar preferências de download
            prefs = {
                "download.default_directory": download_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "plugins.always_open_pdf_externally": True  # Baixar PDFs em vez de abri-los
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            # Iniciar o navegador Chrome
            print("\n--- PASSO 1: Iniciando navegador Chrome ---")
            driver = webdriver.Chrome(options=chrome_options)
            
            # Criar sessão requests para downloads
            session = requests.Session()
            
            # Acessar a página inicial do SINTEGRE
            print("\n--- PASSO 2: Acessando página inicial do SINTEGRE ---")
            driver.get(URL_HOME)
            print(f"URL atual: {driver.current_url}")
            
            # Aguardar a página de login carregar
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            
            # Preencher o formulário de login
            print("\n--- PASSO 3: Preenchendo formulário de login ---")
            username_field = driver.find_element(By.ID, "username")
            password_field = driver.find_element(By.ID, "password")
            login_button = driver.find_element(By.ID, "kc-login")
            
            username_field.send_keys(username)
            password_field.send_keys(password)
            login_button.click()
            
            # Aguardar o redirecionamento (pode levar algum tempo)
            print("\n--- PASSO 4: Aguardando redirecionamentos ---")
            max_wait = 120  # segundos (aumentado para 2 minutos)
            start_time = time.time()
            
            # Aguardar até que estejamos na página do SINTEGRE ou o tempo máximo seja atingido
            while time.time() - start_time < max_wait:
                current_url = driver.current_url
                print(f"Aguardando... URL atual: {current_url}")
                
                # Verificar se estamos em uma página de redirecionamento
                if "redirect" in current_url.lower() or "wsignin" in current_url.lower():
                    # Verificar se há um formulário para submeter
                    try:
                        form = driver.find_element(By.TAG_NAME, "form")
                        if form:
                            print("Encontrado formulário de redirecionamento. Submetendo...")
                            driver.execute_script("document.forms[0].submit();")
                    except:
                        pass
                
                # Verificar se chegamos ao SINTEGRE
                if "sintegre.ons.org.br" in current_url and "login" not in current_url.lower():
                    print(f"✓ Chegamos ao SINTEGRE! URL: {current_url}")
                    break
                    
                time.sleep(5)  # Aguardar 5 segundos antes de verificar novamente
            
            # Verificar se chegamos ao SINTEGRE
            if "sintegre.ons.org.br" in driver.current_url and "login" not in driver.current_url.lower():
                print(f"\n✓ Login bem-sucedido! URL final: {driver.current_url}")
                
                # Acessar a página de boletos diretamente
                print("\n--- PASSO 5: Acessando página de boletos ---")
                driver.get(URL_BOLETOS)
                
                # Aguardar carregamento inicial
                print("Aguardando carregamento inicial da página de boletos (30 segundos)...")
                time.sleep(30)
                
                # Rolar até o final da página várias vezes para carregar todos os boletos
                print("Rolando a página para carregar todos os boletos...")
                for i in range(10):  # Tentar rolar 10 vezes
                    # Rolar até o final da página
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    print(f"Rolagem {i+1}/10 - Aguardando carregamento de mais boletos...")
                    
                    # Verificar se há um elemento "Carregando" visível
                    try:
                        loading_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Carregando')]")
                        if loading_elements:
                            print("Elemento 'Carregando' encontrado. Aguardando...")
                            # Aguardar até que o elemento "Carregando" desapareça (máximo 20 segundos)
                            wait = WebDriverWait(driver, 20)
                            wait.until_not(EC.visibility_of_any_element_located((By.XPATH, "//*[contains(text(), 'Carregando')]")))
                    except:
                        pass
                    
                    # Aguardar um tempo para o carregamento
                    time.sleep(5)
                
                # Aguardar mais um tempo após todas as rolagens
                print("Aguardando carregamento final após rolagens (10 segundos)...")
                time.sleep(10)
                
                print(f"URL atual: {driver.current_url}")
                
                # Verificar se fomos redirecionados para login
                if "login" in driver.current_url.lower() or "auth" in driver.current_url.lower():
                    print("⚠ Redirecionado para login ao acessar página de boletos!")
                    
                    # Tentar novamente com uma abordagem diferente
                    print("Tentando abordagem alternativa...")
                    driver.get(URL_HOME)
                    time.sleep(10)
                    
                    # Navegar pelo menu para chegar à página de boletos
                    try:
                        # Clicar no menu Serviços
                        servicos_menu = driver.find_element(By.XPATH, "//a[contains(text(), 'SERVIÇOS')]")
                        servicos_menu.click()
                        time.sleep(5)
                        
                        # Procurar pelo link de boletos
                        boletos_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Boletos do EUST')]")
                        boletos_link.click()
                        time.sleep(30)  # Aguardar carregamento
                        
                        print(f"Navegação alternativa: {driver.current_url}")
                    except Exception as e:
                        print(f"Erro na navegação alternativa: {str(e)}")
                
                # Salvar o HTML da página para análise
                with open(os.path.join(download_dir, f"{empresa_nome}_boletos_page.html"), 'w', encoding='utf-8') as f:
                    f.write(driver.page_source)
                
                print(f"HTML da página de boletos salvo para análise em {empresa_nome}_boletos_page.html")
                
                # Capturar screenshot para análise visual
                driver.save_screenshot(os.path.join(download_dir, f"{empresa_nome}_boletos_page.png"))
                print(f"Screenshot da página de boletos salvo para análise em {empresa_nome}_boletos_page.png")
                
                # Procurar por links de boletos usando o formato específico
                print("\n--- PASSO 6: Procurando links de boletos ---")
                
                # Usar BeautifulSoup para analisar o HTML
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                
                # Procurar por links com o padrão específico
                boletos_links = {}  # CNPJ -> URL
                
                # Método 1: Procurar por links com class="download-produto"
                links = soup.find_all('a', class_='download-produto')
                print(f"Encontrados {len(links)} links com class='download-produto'")
                
                for link in links:
                    href = link.get('href')
                    if href and 'Produtos/569/' in href:
                        # Verificar se o link contém algum dos CNPJs da empresa atual
                        link_text = link.text.strip()
                        contains, cnpj = contains_cnpj(link_text + href, cnpjs_empresa)
                        if contains:
                            boletos_links[cnpj] = href
                            print(f"Encontrado boleto para CNPJ {cnpj}: {href}")
                
                # Método 2: Procurar por links com id que começa com "linkproduto-"
                links = soup.find_all('a', id=lambda x: x and x.startswith('linkproduto-'))
                print(f"Encontrados {len(links)} links com id que começa com 'linkproduto-'")
                
                for link in links:
                    href = link.get('href')
                    if href and '.pdf' in href:
                        # Verificar se o link contém algum dos CNPJs da empresa atual
                        link_text = link.text.strip()
                        contains, cnpj = contains_cnpj(link_text + href, cnpjs_empresa)
                        if contains:
                            boletos_links[cnpj] = href
                            print(f"Encontrado boleto para CNPJ {cnpj}: {href}")
                
                # Método 3: Usar JavaScript para encontrar links
                js_links = driver.execute_script("""
                    var links = [];
                    var elements = document.querySelectorAll('a[href*=".pdf"]');
                    for (var i = 0; i < elements.length; i++) {
                        var href = elements[i].getAttribute('href');
                        var text = elements[i].innerText;
                        links.push({href: href, text: text});
                    }
                    return links;
                """)
                
                print(f"Encontrados {len(js_links)} links via JavaScript")
                
                for link_data in js_links:
                    href = link_data['href']
                    text = link_data['text']
                    
                    if href and '.pdf' in href:
                        contains, cnpj = contains_cnpj(text + href, cnpjs_empresa)
                        if contains:
                            boletos_links[cnpj] = href
                            print(f"Encontrado boleto via JavaScript para CNPJ {cnpj}: {href}")
                
                print(f"Total de boletos encontrados para {empresa_nome}: {len(boletos_links)}")
                
                # Verificar CNPJs que não foram encontrados
                cnpjs_encontrados = set(boletos_links.keys())
                cnpjs_faltando = set(cnpjs_empresa) - cnpjs_encontrados
                
                if cnpjs_faltando:
                    print(f"\nAtenção: {len(cnpjs_faltando)} CNPJs de {empresa_nome} não tiveram boletos encontrados:")
                    for cnpj in cnpjs_faltando:
                        print(f"  - {cnpj} ({CNPJ_TO_CODE.get(cnpj, 'N/A')})")
                
                # Baixar os boletos encontrados
                print(f"\n--- PASSO 7: Baixando boletos para {empresa_nome} ---")
                boletos_baixados = 0
                
                for cnpj, href in boletos_links.items():
                    try:
                        # Extrair nome do arquivo
                        file_name = href.split('/')[-1]
                        
                        # Adicionar prefixo com o código da empresa
                        empresa_codigo = CNPJ_TO_CODE.get(cnpj, "")
                        if empresa_codigo:
                            file_name = f"{empresa_codigo}_{file_name}"
                        
                        print(f"Baixando boleto para {cnpj} ({empresa_codigo}): {file_name}")
                        
                        # Baixar o arquivo
                        if download_file(driver, session, href, file_name, download_dir):
                            boletos_baixados += 1
                    except Exception as e:
                        print(f"Erro ao baixar boleto para CNPJ {cnpj}: {str(e)}")
                
                print(f"\nProcesso concluído para {empresa_nome}! {boletos_baixados} boletos baixados.")
                
                # Relatório final para esta empresa
                print(f"\n--- RELATÓRIO FINAL PARA {empresa_nome} ---")
                print(f"Total de CNPJs alvo: {len(cnpjs_empresa)}")
                print(f"CNPJs com boletos encontrados: {len(boletos_links)}")
                
                if cnpjs_faltando:
                    print(f"\nCNPJs sem boletos encontrados: {len(cnpjs_faltando)}")
                    for cnpj in cnpjs_faltando:
                        print(f"  - {cnpj} ({CNPJ_TO_CODE.get(cnpj, 'N/A')})")
            else:
                print(f"⚠ Não foi possível acessar o SINTEGRE após {max_wait} segundos para {empresa_nome}.")
                print(f"URL final: {driver.current_url}")
            
            # Fechar o navegador
            driver.quit()
            
        except Exception as e:
            print(f"Erro durante o processamento da empresa {empresa_nome}: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Tentar fechar o navegador em caso de erro
            try:
                if 'driver' in locals():
                    driver.quit()
            except:
                pass
    
    print("\n\n=================================================")
    print("PROCESSO COMPLETO PARA TODAS AS EMPRESAS")
    print("=================================================")

if __name__ == "__main__":
    main()