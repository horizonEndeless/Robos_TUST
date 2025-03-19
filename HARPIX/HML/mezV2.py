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
            download_dir = r"C:\Users\Bruno\Downloads\MEZ"
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
            self.login("4313")
            time.sleep(3)
        except Exception as e:
            print(f"❌ Erro ao inicializar: {str(e)}")
            if hasattr(self, 'driver'):
                self.driver.quit()
            raise e

    def login(self, codigo_ons="4313"):
        try:
            self.driver.get("https://harpixfat.mezenergia.com/FAT/open.do?sys=FAT")
            iframe = self.wait.until(EC.presence_of_element_located((By.NAME, "mainform")))
            self.driver.switch_to.frame("mainform")
            campo_ons = self.wait.until(EC.presence_of_element_located((By.ID, "WFRInput1051800")))
            campo_ons.clear()
            campo_ons.send_keys(codigo_ons)
            botao = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn')]")))
            botao.click()
            print("✓ Login realizado!")
            time.sleep(10)
            return True
        except Exception as e:
            print(f"❌ Erro no login: {str(e)}")
            return False

    def processar_boleto(self, id_botao):
        try:
            # Clica no botão do boleto
            botao = self.wait.until(EC.element_to_be_clickable((By.ID, id_botao)))
            botao.click()
            
            # Aguarda a nova aba abrir (até 20 segundos)
            WebDriverWait(self.driver, 20).until(lambda d: len(d.window_handles) > 1)
            
            # Muda para a nova aba
            nova_aba = self.driver.window_handles[-1]
            self.driver.switch_to.window(nova_aba)
            
            # Aguarda o PDF carregar e captura a URL
            WebDriverWait(self.driver, 20).until(lambda d: "Generated" in d.current_url)
            url_pdf = self.driver.current_url
            
            print(f"✓ PDF gerado com sucesso: {url_pdf}")
            
            # Fecha a aba do PDF
            self.driver.close()
            
            # Volta para a aba principal
            self.driver.switch_to.window(self.driver.window_handles[0])
            
            # Retorna aos frames corretos
            self.driver.switch_to.default_content()
            self.wait.until(EC.frame_to_be_available_and_switch_to_it("mainsystem"))
            self.wait.until(EC.frame_to_be_available_and_switch_to_it("mainform"))
            
            # Procura e muda para o frame URLFrame
            frames = self.driver.find_elements(By.TAG_NAME, "iframe")
            url_frame = None
            for frame in frames:
                name = frame.get_attribute('name')
                if name and name.startswith('URLFrame'):
                    url_frame = name
                    break
                
            if url_frame:
                self.wait.until(EC.frame_to_be_available_and_switch_to_it(url_frame))
                self.wait.until(EC.frame_to_be_available_and_switch_to_it("mainform"))
            
            return url_pdf
            
        except Exception as e:
            print(f"❌ Erro ao processar boleto {id_botao}: {str(e)}")
            traceback.print_exc()  # Adicionado para mostrar o stack trace completo
            return None

    def navegar_ate_tabela(self):
        try:
            self.driver.switch_to.default_content()
            time.sleep(3)
            self.wait.until(EC.frame_to_be_available_and_switch_to_it("mainsystem"))
            time.sleep(3)
            self.wait.until(EC.frame_to_be_available_and_switch_to_it("mainform"))
            time.sleep(3)
            frames = self.driver.find_elements(By.TAG_NAME, "iframe")
            url_frame = None
            for frame in frames:
                name = frame.get_attribute('name')
                if name and name.startswith('URLFrame'):
                    url_frame = name
                    break
            if url_frame:
                self.wait.until(EC.frame_to_be_available_and_switch_to_it(url_frame))
                time.sleep(3)
                self.wait.until(EC.frame_to_be_available_and_switch_to_it("mainform"))
                print("✓ Entrou no último mainform")
                time.sleep(5)
                
                # Primeiro clica nos botões XML
                botoes_xml = [
                    "grid1051940button16",
                    "grid1051940button19",
                    "grid1051940button22",
                    "grid1051940button25",
                    "grid1051940button28",
                ]
                
                # Depois clica nos botões de boleto
                botoes_boleto = [
                    "grid1051940button15",
                    "grid1051940button18",
                    "grid1051940button21",
                    "grid1051940button24",
                    "grid1051940button27",
                ]
                
                # Processa XMLs primeiro
                for id_botao in botoes_xml:
                    try:
                        botao = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//img[@id='{id_botao}']")))
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", botao)
                        time.sleep(1)
                        botao.click()
                        print(f"✓ Clicou no botão XML {id_botao}")
                        time.sleep(2)
                    except Exception as e:
                        print(f"❌ Erro ao clicar no botão XML {id_botao}: {str(e)}")
                        continue
                
                # Depois processa os boletos
                print("\nIniciando download dos boletos...")
                urls_pdfs = []
                for id_botao in botoes_boleto:
                    url_pdf = self.processar_boleto(id_botao)
                    if url_pdf:
                        urls_pdfs.append(url_pdf)
                    time.sleep(2)  # Aguarda 2 segundos entre cada boleto
                
                return urls_pdfs
            return False
        except Exception as e:
            print(f"❌ Erro ao navegar até a tabela: {str(e)}")
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
            if not self.login("4313"):
                print("❌ Falha no login")
                return None
            
            # Aguardar um pouco após o login
            time.sleep(5)
            
            # Depois navegar até a tabela
            if not self.navegar_ate_tabela():
                print("❌ Falha ao navegar até a tabela")
                return None
            
            # Por fim extrair os dados
            if not self.verificar_carregamento():
                print("Aguardando grid ficar visível...")
                time.sleep(5)

            df = self.extrair_dados_tabela()
            
            if df is not None:
                print("\n=== DADOS EXTRAÍDOS COM SUCESSO ===\n")
                
                # Mostrar resumo por transmissora
                print("Resumo por transmissora:")
                resumo = df.groupby('transmissora').agg({
                    'fatura': 'count',
                    'valor': 'sum',
                    'valor_pago': 'sum'
                }).round(2)
                
                # Remover linhas com transmissora vazia
                resumo = resumo[resumo.index != '']
                print(resumo)
                
                # Adicionar verificação dos XMLs após o download
                resultado_verificacao = self.verificar_xmls_baixados(df)
                
                if resultado_verificacao and resultado_verificacao['faltantes']:
                    print("\nTentando baixar XMLs faltantes...")
                    for fatura in resultado_verificacao['faltantes']:
                        print(f"\nTentando baixar XML faltante da fatura {fatura}...")
                        if self.baixar_xml(fatura):
                            print(f"✓ XML da fatura {fatura} baixado com sucesso.")
                        else:
                            print(f"❌ Falha ao baixar XML da fatura {fatura}.")
                
                return df
                
            return None
            
        except Exception as e:
            print(f"❌ Erro ao processar faturas: {str(e)}")
            print(f"Stack trace: {traceback.format_exc()}")
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

    def baixar_xml(self, fatura_id):
        print(f"\nBaixando XML da fatura {fatura_id}...")
        
        try:
            # Encontrar o botão XML
            xml_button = self.driver.execute_script("""
                for (let row of document.querySelectorAll('div[class*="row"]')) {
                    if (row.textContent.includes(arguments[0])) {
                        let xmlBtn = row.querySelector('img[src*="XML"]');
                        if (xmlBtn) {
                            xmlBtn.scrollIntoView();
                            return xmlBtn;
                        }
                    }
                }
                return null;
            """, str(fatura_id))
            
            if not xml_button:
                return False
            
            # Diretório de download
            download_dir = r"C:\Users\Bruno\Downloads\MEZ"
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)
            
            # Clicar no botão XML
            xml_button.click()
            time.sleep(3)
            
            # Verificar se abriu nova aba
            if len(self.driver.window_handles) > 1:
                print("XML abriu em nova aba")
                self.driver.switch_to.window(self.driver.window_handles[-1])
                
                # Pegar o conteúdo XML
                xml_content = self.driver.page_source
                
                # Salvar o arquivo XML
                file_path = os.path.join(download_dir, f"fatura_{fatura_id}.xml")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(xml_content)
                
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                print(f"✓ XML salvo em: {file_path}")
                return True
            
            # Se não abriu nova aba, verificar downloads
            time.sleep(5)  # Aguardar download
            
            # Verificar arquivos baixados
            downloads = os.listdir(download_dir)
            xml_files = [f for f in downloads if f.endswith('.xml')]
            
            if xml_files:
                print(f"✓ XMLs encontrados: {xml_files}")
                return True
            else:
                print("❌ Nenhum arquivo XML encontrado")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao baixar XML: {str(e)}")
            return False

    def processar_nova_aba(self):
        """Processa XML em nova aba"""
        main_window = self.driver.current_window_handle
        try:
            for handle in self.driver.window_handles:
                if handle != main_window:
                    self.driver.switch_to.window(handle)
                    time.sleep(2)
                    
                    # Salvar conteúdo
                    download_dir = r"C:\Users\Bruno\Downloads\MEZ"
                    if not os.path.exists(download_dir):
                        os.makedirs(download_dir)
                        
                    file_path = os.path.join(download_dir, f"fatura_{fatura_id}.xml")
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(self.driver.page_source)
                        
                    self.driver.close()
                    self.driver.switch_to.window(main_window)
                    return True
                    
            return False
        except:
            self.driver.switch_to.window(main_window)
            return False

if __name__ == "__main__":
    extrator = ExtratorFaturas()
    faturas = extrator.processar_faturas()