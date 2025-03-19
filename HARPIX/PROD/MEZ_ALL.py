from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
import requests
import traceback
import json
import urllib3
import os
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
from bs4 import BeautifulSoup

class ExtratorFaturas:
    def __init__(self):
        try:
            print("=== REALIZANDO LOGIN ===")
            chrome_options = Options()
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--ignore-ssl-errors')
            chrome_options.add_argument('--start-maximized')
            
            # Configurar diretório de download
            download_dir = r"C:\Users\Bruno\Downloads\TUST\MEZ"
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)
            
            chrome_options.add_experimental_option('prefs', {
                'download.default_directory': download_dir,
                'download.prompt_for_download': False,
                'download.directory_upgrade': True,
                'safebrowsing.enabled': True,
                'safebrowsing.disable_download_protection': True
            })
            
            caps = DesiredCapabilities.CHROME.copy()
            caps['goog:loggingPrefs'] = {'performance': 'ALL'}
            
            # Combine as opções e capacidades
            chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
            
            # Inicialize o driver com as capacidades combinadas
            self.driver = webdriver.Chrome(service=Service(), options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            self.driver.get("https://harpixfat.mezenergia.com/FAT/open.do?sys=FAT")
            time.sleep(3)
            self.login("4314")
            time.sleep(3)
        except Exception as e:
            print(f"❌ Erro ao inicializar: {str(e)}")
            if hasattr(self, 'driver'):
                self.driver.quit()
            raise e

    def login(self, codigo_ons="4314"):
        try:
            self.driver.get("https://harpixfat.mezenergia.com/FAT/open.do?sys=FAT")
            
            # Aguardar carregamento completo da página
            WebDriverWait(self.driver, 15).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            # Verificar se o iframe mainform está disponível
            iframe = self.wait.until(EC.presence_of_element_located((By.NAME, "mainform")))
            self.driver.switch_to.frame("mainform")
            
            # Aguardar o campo de código ONS ficar visível
            campo_ons = self.wait.until(EC.visibility_of_element_located((By.ID, "WFRInput1051800")))
            campo_ons.clear()
            campo_ons.send_keys(codigo_ons)
            
            # Clicar no botão usando JavaScript para maior confiabilidade
            botao = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn')]")))
            self.driver.execute_script("arguments[0].click();", botao)
            
            # Verificar se o login foi bem-sucedido (aguardar elemento que só aparece após login)
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'grid') or contains(@class, 'table')]"))
                )
                print("✓ Login realizado com sucesso!")
                return True
            except:
                print("⚠️ Login realizado, mas não foi possível confirmar o carregamento da página principal")
                return True
            
        except Exception as e:
            print(f"❌ Erro no login: {str(e)}")
            traceback.print_exc()
            return False

    def baixar_pdf(self, url, empresa, fatura):
        try:
            print(f"\nBaixando PDF da fatura {fatura} para {empresa}...")
            
            # Verificar se o arquivo já existe
            download_dir = os.path.join(r"C:\Users\Bruno\Downloads\MEZ", empresa)
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)
                print(f"✓ Pasta criada: {download_dir}")
            
            file_path = os.path.join(download_dir, f"boleto_{empresa}_{fatura}.pdf")
            if os.path.exists(file_path):
                print(f"✓ PDF já existe: {file_path}")
                return True
            
            # Pegar os cookies da sessão atual
            cookies = {cookie['name']: cookie['value'] for cookie in self.driver.get_cookies()}
            
            # Headers para simular o navegador
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0',
                'Accept': 'application/pdf'
            }
            
            response = requests.get(
                url,
                cookies=cookies,
                headers=headers,
                verify=False,
                stream=True
            )
            
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                print(f"✓ PDF baixado com sucesso: {file_path}")
                return True
            else:
                print(f"❌ Erro ao baixar PDF. Status: {response.status_code}")
                return False
            
        except Exception as e:
            print(f"❌ Erro ao baixar PDF: {str(e)}")
            traceback.print_exc()
            return False

    def processar_boleto(self, id_botao, max_tentativas=3):
        for tentativa in range(max_tentativas):
            try:
                print(f"\nTentativa {tentativa + 1} de {max_tentativas} para o botão {id_botao}")
                
                # Garantir que estamos na janela principal
                if len(self.driver.window_handles) > 1:
                    main_window = self.driver.window_handles[0]
                    for handle in self.driver.window_handles[1:]:
                        self.driver.switch_to.window(handle)
                        self.driver.close()
                    self.driver.switch_to.window(main_window)
                
                # Restaurar frames
                self.driver.switch_to.default_content()
                self.wait.until(EC.frame_to_be_available_and_switch_to_it("mainsystem"))
                self.wait.until(EC.frame_to_be_available_and_switch_to_it("mainform"))
                
                # Procurar e mudar para o frame URLFrame
                frames = self.driver.find_elements(By.TAG_NAME, "iframe")
                for frame in frames:
                    name = frame.get_attribute('name')
                    if name and name.startswith('URLFrame'):
                        self.wait.until(EC.frame_to_be_available_and_switch_to_it(frame))
                        self.wait.until(EC.frame_to_be_available_and_switch_to_it("mainform"))
                        break
                
                # Verificar se o botão existe
                try:
                    botao = self.wait.until(EC.presence_of_element_located((By.ID, id_botao)))
                except:
                    print(f"⚠️ Botão {id_botao} não encontrado, tentando localizar por XPath")
                    try:
                        botao = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//img[@id='{id_botao}']")))
                    except:
                        print(f"❌ Botão {id_botao} não encontrado por ID nem XPath")
                        if tentativa < max_tentativas - 1:
                            time.sleep(5)
                            continue
                        else:
                            return None
                
                # Verificar se o botão está visível
                if not botao.is_displayed():
                    print(f"⚠️ Botão {id_botao} não está visível, tentando rolar até ele")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", botao)
                time.sleep(2)
                
                # Clica no botão do boleto usando JavaScript para maior confiabilidade
                self.driver.execute_script("arguments[0].click();", botao)
                
                # Aguarda a nova aba abrir
                try:
                    WebDriverWait(self.driver, 20).until(lambda d: len(d.window_handles) > 1)
                    nova_aba = self.driver.window_handles[-1]
                    self.driver.switch_to.window(nova_aba)
                    
                    # Aguarda o PDF carregar
                    WebDriverWait(self.driver, 20).until(lambda d: "Generated" in d.current_url or "pdf" in d.current_url.lower())
                    url_pdf = self.driver.current_url
                    
                    print(f"✓ PDF gerado com sucesso: {url_pdf}")
                    
                    # Fecha a aba do PDF
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    
                    return url_pdf
                    
                except Exception as e:
                    print(f"❌ Erro ao processar nova aba: {str(e)}")
                    # Se falhou, tenta recuperar a sessão
                    if len(self.driver.window_handles) > 1:
                        main_window = self.driver.window_handles[0]
                        for handle in self.driver.window_handles[1:]:
                            try:
                                self.driver.switch_to.window(handle)
                                self.driver.close()
                            except:
                                pass
                        self.driver.switch_to.window(main_window)
                    
                    if tentativa < max_tentativas - 1:
                        print("Aguardando antes da próxima tentativa...")
                        time.sleep(5)
                    continue
                
            except Exception as e:
                print(f"❌ Erro na tentativa {tentativa + 1}: {str(e)}")
                if tentativa < max_tentativas - 1:
                    print("Tentando recuperar a sessão...")
                    try:
                        self.driver.switch_to.default_content()
                        time.sleep(5)
                    except:
                        pass
                    continue
        
        print(f"❌ Todas as {max_tentativas} tentativas falharam para o botão {id_botao}")
        return None

    def identificar_botoes_por_padrao(self):
        """Identifica automaticamente os botões de PDF e XML baseado nos padrões encontrados"""
        try:
            print("\n=== IDENTIFICANDO BOTÕES AUTOMATICAMENTE ===")
            
            # Script para encontrar todos os botões que seguem o padrão grid####button##
            script = """
            function encontrarBotoesPorPadrao() {
                // Encontrar todos os elementos com ID que segue o padrão grid####button##
                var botoes = Array.from(document.querySelectorAll('img[id^="grid"][id*="button"]'));
                
                // Extrair informações relevantes
                var infoBotoes = botoes.map(function(btn) {
                    return {
                        id: btn.id,
                        src: btn.src || '',
                        title: btn.title || btn.getAttribute('title') || '',
                        alt: btn.alt || '',
                        visivel: btn.offsetParent !== null
                    };
                });
                
                // Filtrar apenas botões visíveis
                infoBotoes = infoBotoes.filter(btn => btn.visivel);
                
                // Ordenar por ID para manter a sequência
                infoBotoes.sort((a, b) => {
                    // Extrair o número do botão para ordenação numérica
                    var numA = parseInt(a.id.replace(/.*button/, ''));
                    var numB = parseInt(b.id.replace(/.*button/, ''));
                    return numA - numB;
                });
                
                // Analisar URLs para identificar função (PDF, XML, etc)
                infoBotoes.forEach(function(btn) {
                    // Verificar URL da imagem para determinar função
                    if (btn.src.includes('PDF') || btn.title.includes('PDF') || btn.alt.includes('PDF') || 
                        btn.src.includes('boleto') || btn.title.includes('boleto') || btn.alt.includes('boleto')) {
                        btn.funcao = 'PDF';
                    } else if (btn.src.includes('XML') || btn.title.includes('XML') || btn.alt.includes('XML')) {
                        btn.funcao = 'XML';
                    } else {
                        // Se não conseguir identificar pela URL, tentar pelo padrão de sequência
                        // Normalmente os botões seguem um padrão: PDF, XML, Outro
                        var numBotao = parseInt(btn.id.replace(/.*button/, ''));
                        var modulo = numBotao % 3;
                        
                        if (modulo === 1) btn.funcao = 'PDF';
                        else if (modulo === 2) btn.funcao = 'XML';
                        else btn.funcao = 'OUTRO';
                    }
                });
                
                return infoBotoes;
            }
            
            return encontrarBotoesPorPadrao();
            """
            
            botoes = self.driver.execute_script(script)
            
            if not botoes:
                print("❌ Nenhum botão encontrado")
                return None, None
            
            print(f"✓ Total de botões encontrados: {len(botoes)}")
            
            # Separar botões por função
            botoes_pdf = [b['id'] for b in botoes if b['funcao'] == 'PDF']
            botoes_xml = [b['id'] for b in botoes if b['funcao'] == 'XML']
            
            print(f"✓ Botões PDF identificados: {len(botoes_pdf)}")
            print(f"✓ Botões XML identificados: {len(botoes_xml)}")
            
            # Verificar se os botões estão em grupos de 3 (PDF, XML, Outro)
            # Se sim, podemos usar essa informação para identificar corretamente
            if len(botoes) % 3 == 0:
                print("✓ Os botões estão organizados em grupos de 3")
                
                # Reorganizar baseado no padrão observado
                botoes_agrupados = []
                for i in range(0, len(botoes), 3):
                    if i+2 < len(botoes):
                        grupo = {
                            'pdf': botoes[i]['id'],
                            'xml': botoes[i+1]['id'],
                            'outro': botoes[i+2]['id']
                        }
                        botoes_agrupados.append(grupo)
            
                print(f"✓ {len(botoes_agrupados)} grupos de botões identificados")
                
                # Usar os grupos para definir os botões PDF e XML
                botoes_pdf = [g['pdf'] for g in botoes_agrupados]
                botoes_xml = [g['xml'] for g in botoes_agrupados]
            
            # Mostrar os botões identificados
            print("\nBotões PDF:")
            for i, btn in enumerate(botoes_pdf):
                print(f"{i+1}. {btn}")
            
            print("\nBotões XML:")
            for i, btn in enumerate(botoes_xml):
                print(f"{i+1}. {btn}")
            
            return botoes_pdf, botoes_xml
            
        except Exception as e:
            print(f"❌ Erro ao identificar botões por padrão: {str(e)}")
            traceback.print_exc()
            return None, None

    def navegar_ate_tabela(self):
        try:
            self.driver.switch_to.default_content()
            time.sleep(3)
            self.wait.until(EC.frame_to_be_available_and_switch_to_it("mainsystem"))
            time.sleep(3)
            self.wait.until(EC.frame_to_be_available_and_switch_to_it("mainform"))
            time.sleep(3)
            
            # Verificar se há filtro de data e configurar para o mês atual
            try:
                data_atual = datetime.now()
                mes_atual = data_atual.month
                ano_atual = data_atual.year
                
                # Procurar campos de filtro de data
                filtro_data_inicio = self.driver.find_element(By.XPATH, "//input[contains(@id, 'dataInicio') or contains(@id, 'dateFrom')]")
                filtro_data_fim = self.driver.find_element(By.XPATH, "//input[contains(@id, 'dataFim') or contains(@id, 'dateTo')]")
                
                # Configurar para o mês atual
                primeiro_dia = f"01/{mes_atual:02d}/{ano_atual}"
                ultimo_dia = f"{data_atual.day:02d}/{mes_atual:02d}/{ano_atual}"
                
                filtro_data_inicio.clear()
                filtro_data_inicio.send_keys(primeiro_dia)
                
                filtro_data_fim.clear()
                filtro_data_fim.send_keys(ultimo_dia)
                
                # Procurar e clicar no botão de filtrar/pesquisar
                botao_filtrar = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Filtrar') or contains(text(), 'Pesquisar')]")
                botao_filtrar.click()
                
                print(f"✓ Filtro aplicado: {primeiro_dia} até {ultimo_dia}")
                time.sleep(3)
            except Exception as e:
                print(f"⚠️ Não foi possível aplicar filtro de data: {str(e)}")
                # Continuar mesmo sem filtro
            
            # Procurar frames URLFrame
            frames = self.driver.find_elements(By.TAG_NAME, "iframe")
            url_frame = None
            for frame in frames:
                name = frame.get_attribute('name')
                if name and name.startswith('URLFrame'):
                    url_frame = name
                    break
                
            if url_frame:
                self.wait.until(EC.frame_to_be_available_and_switch_to_it(url_frame))
                time.sleep(2)
                self.wait.until(EC.frame_to_be_available_and_switch_to_it("mainform"))
                print("✓ Entrou no último mainform")
                time.sleep(3)
                
                # Verificar se há dados na tabela
                tabela_vazia = self.driver.execute_script("""
                    return document.querySelectorAll('tr').length <= 1;
                """)
                
                if tabela_vazia:
                    print("⚠️ Tabela parece estar vazia, verificando se há mensagens de erro...")
                    mensagens = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'alert') or contains(@class, 'message')]")
                    if mensagens:
                        for msg in mensagens:
                            print(f"Mensagem encontrada: {msg.text}")
                    return False
                
                # Identificar botões automaticamente
                botoes_pdf, botoes_xml = self.identificar_botoes_por_padrao()
                
                # Se não conseguiu identificar, usar os botões padrão
                if not botoes_pdf or not botoes_xml:
                    print("⚠️ Usando IDs de botões padrão")
                    botoes_xml = [
                        "grid1051940button28",
                        "grid1051940button31",
                        "grid1051940button34",
                        "grid1051940button37",
                        "grid1051940button40"
                    ]
                    
                    botoes_pdf = [
                        "grid1051940button27",
                        "grid1051940button30",
                        "grid1051940button33",
                        "grid1051940button36",
                        "grid1051940button39"
                    ]
                
                # Processa XMLs primeiro
                for id_botao in botoes_xml:
                    try:
                        botao = self.wait.until(EC.element_to_be_clickable((By.ID, id_botao)))
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", botao)
                        time.sleep(1)
                        botao.click()
                        print(f"✓ Clicou no botão XML {id_botao}")
                        time.sleep(2)
                    except Exception as e:
                        print(f"❌ Erro ao clicar no botão XML {id_botao}: {str(e)}")
                        continue
                
                # Depois processa os boletos
                print("\nIniciando processamento dos boletos...")
                urls_pdfs = []
                falhas = []
                
                for id_botao in botoes_pdf:
                    url_pdf = self.processar_boleto(id_botao)
                    if url_pdf:
                        urls_pdfs.append(url_pdf)
                        print(f"✓ Boleto {id_botao} processado com sucesso")
                    else:
                        falhas.append(id_botao)
                        print(f"⚠️ Falha ao processar boleto {id_botao}")
                    time.sleep(2)
                
                # Se houver falhas, tenta novamente
                if falhas:
                    print(f"\nTentando novamente para {len(falhas)} boletos que falharam...")
                    for id_botao in falhas:
                        url_pdf = self.processar_boleto(id_botao, max_tentativas=5)  # Mais tentativas para os que falharam
                        if url_pdf:
                            urls_pdfs.append(url_pdf)
                            print(f"✓ Boleto {id_botao} processado com sucesso na segunda tentativa")
                        else:
                            print(f"❌ Falha definitiva ao processar boleto {id_botao}")
                
                print(f"\nTotal de PDFs capturados: {len(urls_pdfs)} de {len(botoes_pdf)}")
                return urls_pdfs
                
            return False
            
        except Exception as e:
            print(f"❌ Erro ao navegar até a tabela: {str(e)}")
            traceback.print_exc()
            return None

    def verificar_carregamento(self):
        try:
            grid_visible = self.driver.execute_script("""
                var grid = document.querySelector('.listGrid') || 
                          document.querySelector('.listTable');
                return grid && grid.offsetParent !== null;
            """)
            if not grid_visible:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            return grid_visible
        except Exception as e:
            print(f"Erro ao verificar carregamento: {str(e)}")
            return False

    def extrair_dados_tabela(self):
        try:
            print("Aguardando carregamento completo da tabela...")
            time.sleep(5)
            
            script = r"""
            function extrairDados() {
                var dados = [];
                var transmissora_atual = '';
                
                // Função para limpar valor monetário
                function limparValor(valor) {
                    return valor.replace(/[^0-9,]/g, '').replace('.', '').replace(',', '.');
                }
                
                // Procura por todas as linhas
                document.querySelectorAll('tr').forEach((row, index) => {
                    // Se for linha de transmissora (tem apenas 1 célula com o nome da MEZ)
                    if (row.cells.length === 1 && row.textContent.includes('MEZ') && row.textContent.includes('ENERGIA S/A')) {
                        transmissora_atual = row.textContent.trim();
                        return;
                    }
                    
                    // Se for linha de dados (tem 13 células)
                    if (row.cells.length === 13) {
                        var texto = row.textContent.trim();
                        
                        // Verifica se a linha tem conteúdo e números
                        if (texto && /\d/.test(texto)) {
                            try {
                                // Extrai os dados usando o texto completo da linha
                                var matches = texto.match(/(\d+)(\d{2})(\d{2})\/(\d{2})\/(\d{4})(\d{2})\/(\d{2})\/(\d{4})([\d,.]+)(Fatura[^0-9]*)([0-9,.]*)/);
                                
                                if (matches) {
                                    var dadosLinha = {
                                        'transmissora': transmissora_atual,
                                        'fatura': matches[1],
                                        'parcela': matches[2],
                                        'emissao': `${matches[3]}/${matches[4]}/${matches[5]}`,
                                        'vencimento': `${matches[6]}/${matches[7]}/${matches[8]}`,
                                        'valor': limparValor(matches[9]),
                                        'situacao': matches[10].trim(),
                                        'valor_pago': limparValor(matches[11] || '0')
                                    };
                                    
                                    dados.push(dadosLinha);
                                    console.log('Dados extraídos:', dadosLinha);
                                }
                            } catch (e) {
                                console.log('Erro ao processar linha:', index, e.message);
                            }
                        }
                    }
                });
                
                return dados;
            }
            return extrairDados();
            """
            
            dados = self.driver.execute_script(script)
            print(f"\nRegistros encontrados: {len(dados)}")
            
            if not dados:
                print("Nenhum dado encontrado!")
                return pd.DataFrame()
            
            # Converte para DataFrame
            df = pd.DataFrame(dados)
            
            # Converte valores numéricos
            df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
            df['valor_pago'] = pd.to_numeric(df['valor_pago'], errors='coerce')
            
            print("\nColunas do DataFrame:", list(df.columns))
            print("\nPrimeiras linhas:")
            print(df.head())
            
            return df

        except Exception as e:
            print(f"Erro ao extrair dados da tabela: {str(e)}")
            print(f"Stack trace: {traceback.format_exc()}")
            return pd.DataFrame()

    def verificar_xmls_baixados(self, df):
        try:
            print("\n=== VERIFICANDO XMLs BAIXADOS ===")
            download_dir = r"C:\Users\Bruno\Downloads\MEZ"
            
            # Listar todos os XMLs no diretório
            xmls_baixados = [f for f in os.listdir(download_dir) if f.endswith('.xml')]
            print(f"\nTotal de XMLs encontrados: {len(xmls_baixados)}")
            
            # Criar lista de faturas do DataFrame e remover o zero final
            faturas_df = [str(int(int(fatura)/10)) for fatura in df['fatura'].unique()]
            print(f"Total de faturas no DataFrame: {len(faturas_df)}")
            
            # Verificar XMLs baixados vs faturas
            xmls_encontrados = []
            xmls_faltantes = faturas_df.copy()  # Criar uma cópia para manipular
            
            for xml_file in xmls_baixados:
                try:
                    # Ler o arquivo XML
                    xml_path = os.path.join(download_dir, xml_file)
                    with open(xml_path, 'r', encoding='utf-8') as f:
                        xml_content = f.read()
                    
                    # Usar BeautifulSoup para parse do XML
                    soup = BeautifulSoup(xml_content, 'xml')
                    
                    # Encontrar o número da fatura no XML
                    nf_element = soup.find('nNF')
                    if nf_element:
                        numero_fatura = nf_element.text.strip()
                        print(f"XML {xml_file} contém fatura número: {numero_fatura}")
                        
                        # Verificar se esta fatura está no DataFrame
                        if numero_fatura in faturas_df:
                            xmls_encontrados.append({
                                'fatura': numero_fatura,
                                'arquivo': xml_file,
                                'fatura_original': str(int(numero_fatura) * 10)  # Para mostrar o número original
                            })
                            if numero_fatura in xmls_faltantes:
                                xmls_faltantes.remove(numero_fatura)
                except Exception as e:
                    print(f"Erro ao processar XML {xml_file}: {str(e)}")
                    continue
            
            # Exibir resumo
            print("\n=== RESUMO DA VERIFICAÇÃO ===")
            print(f"XMLs encontrados: {len(xmls_encontrados)}")
            print(f"XMLs faltantes: {len(xmls_faltantes)}")
            
            if xmls_encontrados:
                print("\nXMLs baixados e verificados:")
                for xml in xmls_encontrados:
                    print(f"✓ Fatura {xml['fatura_original']} (XML: {xml['fatura']}): {xml['arquivo']}")
            
            if xmls_faltantes:
                print("\nFaturas sem XML:")
                for fatura in xmls_faltantes:
                    print(f"❌ Fatura {int(fatura) * 10}")
            
            return {
                'encontrados': xmls_encontrados,
                'faltantes': xmls_faltantes
            }
            
        except Exception as e:
            print(f"❌ Erro ao verificar XMLs: {str(e)}")
            traceback.print_exc()
            return None

    def processar_faturas(self):
        try:
            print("\n=== EXTRAINDO FATURAS ===")
            
            # Realizar login primeiro
            if not self.login("4314"):
                print("❌ Falha no login")
                return None
            
            # Aguardar um pouco após o login
            time.sleep(5)
            
            # Navegar até a tabela e capturar URLs dos PDFs
            urls_pdfs = self.navegar_ate_tabela()
            
            if urls_pdfs:
                print(f"\nURLs dos PDFs capturadas: {len(urls_pdfs)}")
                for i, url in enumerate(urls_pdfs, 1):
                    print(f"{i}. {url}")
                
                # Baixar os PDFs
                self.baixar_pdfs(urls_pdfs)
            else:
                print("❌ Nenhuma URL de PDF capturada")
            
            return urls_pdfs
            
        except Exception as e:
            print(f"❌ Erro ao processar faturas: {str(e)}")
            traceback.print_exc()
            return None

    def capturar_url_download(self, fatura_id):
        logs = self.driver.get_log('performance')
        for entry in logs:
            log = json.loads(entry['message'])['message']
            if log['method'] == 'Network.responseReceived':
                url = log['params']['response']['url']
                if f"downloadXML&faturaId={fatura_id}" in url:
                    return url
        return None

    def inicializar_driver(self):
        try:
            # Fechar driver existente se houver
            if hasattr(self, 'driver'):
                try:
                    self.driver.quit()
                except:
                    pass
            
            print("\n=== INICIANDO NOVO NAVEGADOR ===")
            chrome_options = Options()
            
            # Configurações para permitir downloads
            chrome_options.add_experimental_option('prefs', {
                'download.default_directory': r"C:\Users\Bruno\Downloads\MEZ",
                'download.prompt_for_download': False,
                'download.directory_upgrade': True,
                'safebrowsing.enabled': True,
                'safebrowsing.disable_download_protection': True,
                'safebrowsing.download_protection_enabled': False,
                'profile.default_content_setting_values.automatic_downloads': 1,
                'profile.content_settings.exceptions.automatic_downloads.*.setting': 1
            })
            
            # Argumentos adicionais para ignorar avisos de segurança
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--ignore-ssl-errors')
            chrome_options.add_argument('--start-maximized')
            chrome_options.add_argument('--safebrowsing-disable-download-protection')
            chrome_options.add_argument('--disable-web-security')
            
            caps = DesiredCapabilities.CHROME.copy()
            caps['goog:loggingPrefs'] = {'performance': 'ALL'}
            chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
            
            self.driver = webdriver.Chrome(service=Service(), options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            
            # Configurar downloads permitidos via JavaScript
            self.driver.execute_cdp_cmd('Page.setDownloadBehavior', {
                'behavior': 'allow',
                'downloadPath': r"C:\Users\Bruno\Downloads\MEZ"
            })
            
            return True
        except Exception as e:
            print(f"❌ Erro ao inicializar driver: {str(e)}")
            return False

    def baixar_xml(self, fatura_id, empresa, numero):
        try:
            print(f"\nBaixando XML da fatura {fatura_id} para {empresa}...")
            
            # Criar pasta específica para a empresa
            download_dir = os.path.join(r"C:\Users\Bruno\Downloads\MEZ", empresa)
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)
                print(f"✓ Pasta criada: {download_dir}")
            
            # Atualizar pasta de download para a empresa específica
            self.driver.execute_cdp_cmd('Page.setDownloadBehavior', {
                'behavior': 'allow',
                'downloadPath': download_dir
            })
            
            # Encontrar e clicar no botão XML
            xml_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//img[contains(@src, 'XML')]")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", xml_button)
            time.sleep(1)
            xml_button.click()
            
            # Aguardar download
            max_espera = 30
            inicio = time.time()
            while time.time() - inicio < max_espera:
                downloads = os.listdir(download_dir)
                xml_files = [f for f in downloads if f.endswith('.xml') and not f.endswith('.crdownload')]
                if xml_files:
                    ultimo_xml = max(xml_files, key=lambda f: os.path.getctime(os.path.join(download_dir, f)))
                    old_path = os.path.join(download_dir, ultimo_xml)
                    new_path = os.path.join(download_dir, f"xml_{empresa}_{numero}.xml")
                    
                    # Aguardar arquivo terminar de baixar
                    time.sleep(2)
                    try:
                        os.rename(old_path, new_path)
                        print(f"✓ XML salvo em: {new_path}")
                        return True
                    except Exception as e:
                        print(f"❌ Erro ao renomear XML: {str(e)}")
                        return False
                time.sleep(1)
            
            print("❌ Timeout aguardando download do XML")
            return False
                
        except Exception as e:
            print(f"❌ Erro ao baixar XML: {str(e)}")
            traceback.print_exc()
            return False

    def processar_empresa(self, codigo_ons, nome_empresa):
        try:
            print(f"\n=== PROCESSANDO {nome_empresa} (Código: {codigo_ons}) ===")
            
            # Criar pasta específica para a empresa
            empresa_dir = os.path.join(r"C:\Users\Bruno\Downloads\MEZ", nome_empresa)
            if not os.path.exists(empresa_dir):
                os.makedirs(empresa_dir)
                print(f"✓ Pasta criada: {empresa_dir}")
            
            # Verificar arquivos já baixados para evitar duplicação
            arquivos_existentes = [f for f in os.listdir(empresa_dir) if f.endswith('.pdf') or f.endswith('.xml')]
            print(f"✓ {len(arquivos_existentes)} arquivos já existentes para {nome_empresa}")
            
            # Inicializar novo driver com a pasta de download correta
            chrome_options = Options()
            chrome_options.add_experimental_option('prefs', {
                'download.default_directory': empresa_dir,
                'download.prompt_for_download': False,
                'download.directory_upgrade': True,
                'safebrowsing.enabled': True,
                'safebrowsing.disable_download_protection': True,
                'safebrowsing.download_protection_enabled': False
            })
            
            # Argumentos adicionais
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--ignore-ssl-errors')
            chrome_options.add_argument('--start-maximized')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--disable-features=IsolateOrigins,site-per-process')
            
            # Inicializar driver
            if hasattr(self, 'driver'):
                try:
                    self.driver.quit()
                except:
                    pass
            
            self.driver = webdriver.Chrome(service=Service(), options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            
            # Configurar comportamento de download para a pasta da empresa
            self.driver.execute_cdp_cmd('Page.setDownloadBehavior', {
                'behavior': 'allow',
                'downloadPath': empresa_dir
            })
            
            # Realizar login
            if not self.login(codigo_ons):
                print(f"❌ Falha no login para {nome_empresa}")
                return None
            
            time.sleep(5)
            
            # Navegar e processar
            urls_pdfs = self.navegar_ate_tabela()
            
            if urls_pdfs:
                print(f"\nURLs dos PDFs capturadas: {len(urls_pdfs)}")
                for i, url in enumerate(urls_pdfs, 1):
                    print(f"{i}. {url}")
                    self.baixar_pdf(url, nome_empresa, i)
                    time.sleep(2)
            else:
                print(f"❌ Nenhuma URL de PDF capturada para {nome_empresa}")
            
            return urls_pdfs
            
        except Exception as e:
            print(f"❌ Erro ao processar {nome_empresa}: {str(e)}")
            traceback.print_exc()
            return None
        finally:
            if hasattr(self, 'driver'):
                try:
                    self.driver.quit()
                except:
                    pass

    def processar_todas_empresas(self):
        empresas = [
            # ('4313', 'BRJA'),
            # ('4314', 'BRJB'),
            # ('3430', 'CECA'),
            # ('3431', 'CECB'),
            # ('3432', 'CECC'),
            # ('4415', 'CECD'),
            # ('4315', 'CECE'),
            # ('4316', 'CECF'),
            # ('3502', 'ITA1'),
            # ('3497', 'ITA2'),
            # ('3503', 'ITA3'),
            # ('3530', 'ITA4'),
            # ('3498', 'ITA5'),
            # ('3531', 'ITA6'),
            # ('3532', 'ITA7'),
            # ('3537', 'ITA8'),
            # ('3538', 'ITA9'),
            # ('3947', 'SDBA'),
            # ('3948', 'SDBB'),
            # ('3969', 'SDBC'),
            # ('3970', 'SDBD'),
            # ('3976', 'SDBE'),
            # ('3972', 'SDBF')
            
            # ('3859', 'SJP1'),
            # ('3860', 'SJP2'),
            # ('3861', 'SJP3'),
            # ('3862', 'SJP4'),
            # ('3863', 'SJP5'),
            # ('3864', 'SJP6'),
            # ('3740', 'COR1'),
            # ('3741', 'COR2'),
            # ('3750', 'COR3'),
            # ('8011', 'LIBRA')
            
            ('3748', 'DE')
            
        ]
        
        resultados = {}
        
        for codigo, nome in empresas:
            try:
                print(f"\n{'='*50}")
                print(f"Iniciando processamento da empresa {nome} (Código: {codigo})")
                print(f"{'='*50}")
                
                # Criar pasta específica para a empresa
                empresa_dir = os.path.join(r"C:\Users\Bruno\Downloads\MEZ", nome)
                if not os.path.exists(empresa_dir):
                    os.makedirs(empresa_dir)
                    print(f"✓ Pasta criada: {empresa_dir}")
                
                # Processar empresa
                urls = self.processar_empresa(codigo, nome)
                
                if urls:
                    resultados[nome] = {
                        'status': 'Sucesso',
                        'pdfs_encontrados': len(urls)
                    }
                    print(f"✓ {nome}: {len(urls)} PDFs processados")
                else:
                    resultados[nome] = {
                        'status': 'Falha',
                        'pdfs_encontrados': 0
                    }
                    print(f"⚠️ {nome}: Nenhum PDF encontrado")
                
                # Aguarda entre empresas
                print(f"\nAguardando 10 segundos antes da próxima empresa...")
                time.sleep(10)
                
            except Exception as e:
                print(f"❌ Erro processando {nome}: {str(e)}")
                resultados[nome] = {
                    'status': 'Erro',
                    'erro': str(e)
                }
                continue
        
        # Mostrar resumo final
        print("\n=== RESUMO DO PROCESSAMENTO ===")
        print(f"Total de empresas: {len(empresas)}")
        
        sucessos = sum(1 for r in resultados.values() if r['status'] == 'Sucesso')
        falhas = sum(1 for r in resultados.values() if r['status'] == 'Falha')
        erros = sum(1 for r in resultados.values() if r['status'] == 'Erro')
        
        print(f"\nEmpresas processadas com sucesso: {sucessos}")
        print(f"Empresas sem PDFs: {falhas}")
        print(f"Empresas com erro: {erros}")
        
        print("\nDetalhes por empresa:")
        for empresa, resultado in resultados.items():
            status = resultado['status']
            if status == 'Sucesso':
                print(f"✓ {empresa}: {resultado['pdfs_encontrados']} PDFs baixados")
            elif status == 'Falha':
                print(f"⚠️ {empresa}: Nenhum PDF encontrado")
            else:
                print(f"❌ {empresa}: {resultado.get('erro', 'Erro desconhecido')}")
        
        return resultados

if __name__ == "__main__":
    extrator = ExtratorFaturas()
    resultados = extrator.processar_todas_empresas()