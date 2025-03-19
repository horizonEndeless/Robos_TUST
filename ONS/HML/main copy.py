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
username = "tust@rioenergy.com.br"
password = "Ca2003@#"
download_dir = r"C:\Users\Bruno\Downloads\TUST\ONS"

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
URL_BOLETOS_LIST = "https://sintegre.ons.org.br/sites/1/18/_api/web/lists/GetByTitle('Produtos')/getitems?$select=Id,Title,Produto,DataProdutos,FileRef,Periodicidade,PublicarEm,File_x0020_Type,FileLeafRef,Modified,OData__UIVersionString,UniqueId,File,DescricaoProduto/Length&$expand=file"
URL_DOWNLOAD = "https://sintegre.ons.org.br"

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

def main():
    # Criar diretório de download se não existir
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    print("Iniciando processo de download de faturas ONS...")
    print(f"Usando usuário: {username}")
    
    try:
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
        max_wait = 60  # segundos
        start_time = time.time()
        
        while "sintegre.ons.org.br" not in driver.current_url and time.time() - start_time < max_wait:
            print(f"Aguardando... URL atual: {driver.current_url}")
            time.sleep(2)
        
        # Verificar se chegamos ao SINTEGRE
        if "sintegre.ons.org.br" in driver.current_url:
            print(f"\n✓ Login bem-sucedido! URL final: {driver.current_url}")
            
            # Acessar a página de boletos
            print("\n--- PASSO 5: Acessando página de boletos ---")
            driver.get(URL_BOLETOS)
            
            # Aguardar a página carregar completamente (tempo aumentado para 30 segundos)
            print("Aguardando carregamento completo da página de boletos (30 segundos)...")
            time.sleep(30)  # Aumentado para 30 segundos conforme sugerido
            
            print(f"URL atual: {driver.current_url}")
            
            # Verificar se fomos redirecionados para login
            if "login" in driver.current_url.lower() or "auth" in driver.current_url.lower():
                print("⚠ Redirecionado para login ao acessar página de boletos!")
            else:
                # Salvar o HTML da página para análise
                with open(os.path.join(download_dir, "boletos_page.html"), 'w', encoding='utf-8') as f:
                    f.write(driver.page_source)
                
                print("HTML da página de boletos salvo para análise.")
                
                # Procurar por elementos específicos do SharePoint que contêm os boletos
                print("\n--- PASSO 6: Procurando boletos na página ---")
                
                # Tentar diferentes seletores para encontrar a tabela de boletos
                selectors = [
                    ".ms-listviewtable tr",  # Tabela padrão do SharePoint
                    "table.ms-listviewtable tr",  # Variação da tabela do SharePoint
                    "div[id*='WebPartWPQ'] table tr",  # Web Parts do SharePoint
                    "div.ms-webpart-zone table tr",  # Zonas de Web Parts
                    "table tr",  # Qualquer tabela
                    "a[href*='.pdf']",  # Links diretos para PDFs
                    "a[href*='FileRef']",  # Links de documentos do SharePoint
                    "a[onclick*='OpenPopUpPage']"  # Links com popup
                ]
                
                boletos_encontrados = False
                
                for selector in selectors:
                    try:
                        print(f"Tentando seletor: {selector}")
                        elementos = driver.find_elements(By.CSS_SELECTOR, selector)
                        
                        if elementos:
                            print(f"Encontrados {len(elementos)} elementos com o seletor '{selector}'")
                            
                            # Mostrar os primeiros 5 elementos
                            for i, elemento in enumerate(elementos[:5]):
                                print(f"Elemento {i+1}: {elemento.text[:100]}...")
                                
                                # Se for um link direto, adicionar à lista de boletos
                                if selector.startswith("a["):
                                    href = elemento.get_attribute("href")
                                    if href:
                                        print(f"  Link: {href}")
                                        boletos_encontrados = True
                                
                                # Se for uma linha de tabela, procurar links dentro dela
                                else:
                                    links = elemento.find_elements(By.TAG_NAME, "a")
                                    for link in links:
                                        href = link.get_attribute("href")
                                        if href:
                                            print(f"  Link: {href}")
                                            boletos_encontrados = True
                        else:
                            print(f"Nenhum elemento encontrado com o seletor '{selector}'")
                    except Exception as e:
                        print(f"Erro ao usar seletor '{selector}': {str(e)}")
                
                if not boletos_encontrados:
                    print("\nNenhum boleto encontrado com os seletores padrão. Tentando abordagem alternativa...")
                    
                    # Tentar encontrar links que possam ser boletos
                    links = driver.find_elements(By.TAG_NAME, "a")
                    boletos_links = []
                    
                    for link in links:
                        try:
                            href = link.get_attribute("href")
                            if href:
                                # Verificar se é um link para um arquivo ou contém palavras-chave
                                if (any(ext in href.lower() for ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx']) or
                                    any(term in href.lower() for term in ['download', 'documento', 'arquivo'])):
                                    # Verificar se parece ser um boleto
                                    link_text = link.text.lower()
                                    if any(term in href.lower() or term in link_text for term in 
                                          ['boleto', 'fatura', 'eust', 'tust', 'pagamento', 'encargo']):
                                        boletos_links.append(href)
                                        print(f"Possível boleto encontrado: {href}")
                        except:
                            continue
                    
                    if boletos_links:
                        print(f"\nEncontrados {len(boletos_links)} possíveis links de boletos.")
                        boletos_encontrados = True
                    else:
                        print("\nNenhum link de boleto encontrado.")
                
                # Capturar screenshot para análise visual
                screenshot_path = os.path.join(download_dir, "boletos_page_screenshot.png")
                driver.save_screenshot(screenshot_path)
                print(f"Screenshot da página salvo em: {screenshot_path}")
                
                # Executar JavaScript para tentar encontrar elementos ocultos
                print("\n--- PASSO 7: Executando JavaScript para análise adicional ---")
                js_results = driver.execute_script("""
                    // Coletar informações sobre elementos na página
                    var info = {
                        tables: document.querySelectorAll('table').length,
                        links: document.querySelectorAll('a').length,
                        iframes: document.querySelectorAll('iframe').length,
                        webParts: document.querySelectorAll('div[id*="WebPartWPQ"]').length,
                        sharePointLists: document.querySelectorAll('.ms-listviewtable').length
                    };
                    
                    // Procurar por links de boletos
                    var links = document.querySelectorAll('a');
                    var boletoLinks = [];
                    
                    for (var i = 0; i < links.length; i++) {
                        var href = links[i].href || '';
                        var text = links[i].innerText || '';
                        
                        if (href.includes('.pdf') || 
                            href.includes('FileRef') || 
                            text.toLowerCase().includes('boleto') ||
                            text.toLowerCase().includes('fatura')) {
                            boletoLinks.push({
                                href: href,
                                text: text
                            });
                        }
                    }
                    
                    return {
                        pageInfo: info,
                        boletos: boletoLinks
                    };
                """)
                
                print("Informações da página:")
                for key, value in js_results['pageInfo'].items():
                    print(f"  {key}: {value}")
                
                if js_results['boletos']:
                    print(f"\nEncontrados {len(js_results['boletos'])} possíveis boletos via JavaScript:")
                    for i, boleto in enumerate(js_results['boletos'][:5]):  # Mostrar apenas os 5 primeiros
                        print(f"  {i+1}. {boleto['text']}: {boleto['href']}")
                    
                    # Baixar os boletos encontrados
                    print("\n--- PASSO 8: Baixando boletos ---")
                    boletos_baixados = 0
                    
                    for boleto in js_results['boletos']:
                        try:
                            href = boleto['href']
                            if href and not href.startswith('javascript:'):
                                file_name = get_file_name_from_url(href)
                                print(f"Baixando boleto: {file_name}")
                                
                                # Usar o navegador para baixar o arquivo
                                driver.get(href)
                                time.sleep(5)  # Aguardar o download iniciar
                                
                                boletos_baixados += 1
                        except Exception as e:
                            print(f"Erro ao baixar boleto: {str(e)}")
                    
                    print(f"\nProcesso concluído! {boletos_baixados} boletos baixados.")
                else:
                    print("\nNenhum boleto encontrado via JavaScript.")
                    
                    # Última tentativa: procurar por elementos específicos do SharePoint
                    print("\n--- PASSO 9: Última tentativa - Procurando elementos específicos ---")
                    
                    # Tentar clicar em elementos que possam revelar os boletos
                    try:
                        # Procurar por botões ou links que possam expandir a visualização
                        expanders = driver.find_elements(By.CSS_SELECTOR, 
                            "a[id*='expand'], button[id*='expand'], .ms-commandLink, .ms-promlink-button")
                        
                        if expanders:
                            print(f"Encontrados {len(expanders)} possíveis expansores. Tentando clicar...")
                            
                            for expander in expanders[:3]:  # Tentar apenas os 3 primeiros
                                try:
                                    print(f"Clicando em: {expander.text}")
                                    expander.click()
                                    time.sleep(5)  # Aguardar possível carregamento
                                    
                                    # Capturar screenshot após o clique
                                    driver.save_screenshot(os.path.join(download_dir, f"after_click_{expander.text}.png"))
                                except:
                                    continue
                    except Exception as e:
                        print(f"Erro ao tentar expandir elementos: {str(e)}")
        else:
            print(f"⚠ Não foi possível acessar o SINTEGRE após {max_wait} segundos.")
            print(f"URL final: {driver.current_url}")
        
        # Fechar o navegador
        driver.quit()
        
    except Exception as e:
        print(f"Erro durante o processo: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Tentar fechar o navegador em caso de erro
        try:
            if 'driver' in locals():
                driver.quit()
        except:
            pass

if __name__ == "__main__":
    main()