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
import pyautogui

class ExtratorFaturas:
    def __init__(self):
        try:
            print("=== REALIZANDO LOGIN ===")
            chrome_options = Options()
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--ignore-ssl-errors')
            chrome_options.add_argument('--start-maximized')
            
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
                return True
            return False
        except Exception as e:
            print(f"❌ Erro ao navegar até a tabela: {str(e)}")
            return False

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
                
                # Baixar XML de cada fatura
                for index, fatura in df.iterrows():
                    fatura_id = fatura['fatura']
                    print(f"\nBaixando XML para fatura {fatura_id}...")
                    if self.baixar_xml(fatura_id):
                        print(f"✓ XML da fatura {fatura_id} baixado com sucesso.")
                    else:
                        print(f"❌ Falha ao baixar XML da fatura {fatura_id}.")
                
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
            # Use o caminho absoluto para a imagem PNG
            caminho_imagem = r'C:\caminho\completo\para\Harpix MEZ\botao_xml.png'
            
            # Use pyautogui para localizar e clicar no botão XML
            button_location = pyautogui.locateCenterOnScreen(caminho_imagem, confidence=0.8)
            if button_location:
                pyautogui.click(button_location)
                time.sleep(3)
                print("Botão XML clicado com sucesso.")
                return True
            else:
                print("Botão XML não encontrado.")
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