import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os
import pdfkit

class StateGridRobot:
    def __init__(self):
        self.base_url = "https://sys.sigetplus.com.br/cobranca/company/15/invoices"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

    def get_invoices(self, agent_code):
        """Obtém as faturas para um determinado código de agente"""
        try:
            # Monta a URL com o código do agente
            url = f"{self.base_url}?agent={agent_code}"
            
            # Faz a requisição HTTP
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            # Parse do HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Pega o mês mais recente do dropdown
            select = soup.find('select', {'name': 'time'})
            latest_month = select.find('option')['value'] if select else None
            
            # Se encontrou um mês, adiciona à URL
            if latest_month:
                url = f"{url}&time={latest_month}"
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
            
            # Encontra a tabela de faturas
            table = soup.find('table', {'class': 'table'})
            
            # Extrai os dados da tabela
            data = []
            for row in table.find_all('tr')[1:]:  # Pula o cabeçalho
                cols = row.find_all('td')
                if cols:
                    # Encontra o link do XML especificamente
                    xml_element = cols[6].find('a', {'data-original-title': 'XML'})
                    xml_link = xml_element['href'] if xml_element else None
                    
                    # Encontra o link do DANFE
                    danfe_element = cols[6].find('a', {'data-original-title': 'DANFE'})
                    danfe_link = danfe_element['href'] if danfe_element else None
                    
                    invoice = {
                        'transmissora': cols[0].text.strip(),
                        'numero_fatura': cols[1].text.strip(),
                        'parcelas': cols[2].text.strip(),
                        'boleto_1': cols[3].find('a')['href'] if cols[3].find('a') else None,
                        'xml_link': xml_link,
                        'danfe_link': danfe_link
                    }
                    data.append(invoice)
            
            return pd.DataFrame(data)
            
        except requests.exceptions.RequestException as e:
            print(f"Erro ao fazer requisição: {e}")
            return None
        except Exception as e:
            print(f"Erro ao processar dados: {e}")
            return None

    def baixar_boleto(self, url, caminho_destino):
        """Download e conversão do boleto de HTML para PDF"""
        print(f"Tentando baixar boleto de: {url}")
        try:
            # Faz a requisição do HTML do boleto
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            # Converte o HTML para PDF
            pdfkit.from_string(response.text, caminho_destino, configuration=self.config)
            
            if os.path.exists(caminho_destino) and os.path.getsize(caminho_destino) > 0:
                print(f"Boleto salvo como PDF: {caminho_destino}")
                return True
            else:
                print(f"Erro: arquivo PDF vazio ou não criado: {caminho_destino}")
                return False
                
        except Exception as e:
            print(f"Erro ao baixar boleto: {str(e)}")
            return False

    def download_files(self, df, agent_code, base_path="C:\\Users\\Bruno\\Downloads\\TUST\\Stategrid"):
        """Download dos arquivos XML, DANFE e Boleto"""
        # Cria pasta específica para o agente
        output_path = os.path.join(base_path, str(agent_code))
        os.makedirs(output_path, exist_ok=True)
        
        # Cria pasta com a data atual para organização
        current_date = datetime.now().strftime("%Y%m")
        date_path = os.path.join(output_path, current_date)
        os.makedirs(date_path, exist_ok=True)
        
        for idx, row in df.iterrows():
            try:
                # Cria pasta para a transmissora
                transmissora_code = row['transmissora'].split(' - ')[0].strip()
                transmissora_path = os.path.join(date_path, transmissora_code)
                os.makedirs(transmissora_path, exist_ok=True)
                
                # Download XML
                if row['xml_link']:
                    try:
                        xml_response = requests.get(row['xml_link'], headers=self.headers)
                        xml_response.raise_for_status()
                        
                        xml_filename = row['xml_link'].split('/')[-1]
                        if not xml_filename.endswith('.xml'):
                            xml_filename = f"{row['numero_fatura']}.xml"
                        
                        xml_path = os.path.join(transmissora_path, xml_filename)
                        with open(xml_path, 'wb') as f:
                            f.write(xml_response.content)
                        print(f"XML salvo: {xml_path}")
                    except Exception as e:
                        print(f"Erro ao baixar XML da fatura {row['numero_fatura']}: {e}")
                
                # Download DANFE
                if row['danfe_link']:
                    try:
                        danfe_response = requests.get(row['danfe_link'], headers=self.headers)
                        danfe_response.raise_for_status()
                        
                        danfe_filename = f"{row['numero_fatura']}_danfe.pdf"
                        danfe_path = os.path.join(transmissora_path, danfe_filename)
                        with open(danfe_path, 'wb') as f:
                            f.write(danfe_response.content)
                        print(f"DANFE salvo: {danfe_path}")
                    except Exception as e:
                        print(f"Erro ao baixar DANFE da fatura {row['numero_fatura']}: {e}")

                # Download Boleto
                if row['boleto_1']:
                    try:
                        boleto_filename = f"{row['numero_fatura']}_boleto.pdf"
                        boleto_path = os.path.join(transmissora_path, boleto_filename)
                        self.baixar_boleto(row['boleto_1'], boleto_path)
                    except Exception as e:
                        print(f"Erro ao baixar Boleto da fatura {row['numero_fatura']}: {e}")
                        
            except Exception as e:
                print(f"Erro ao processar fatura {row['numero_fatura']}: {e}")

    def process_all_agents(self, agent_codes):
        """Processa todos os agentes fornecidos"""
        for agent_code in agent_codes:
            try:
                print(f"\nProcessando agente {agent_code}...")
                df = self.get_invoices(agent_code)
                if df is not None and not df.empty:
                    print(f"Encontradas {len(df)} faturas para o agente {agent_code}")
                    self.download_files(df, agent_code)
                else:
                    print(f"Nenhuma fatura encontrada para o agente {agent_code}")
            except Exception as e:
                print(f"Erro ao processar agente {agent_code}: {e}")

# Exemplo de uso
if __name__ == "__main__":
    # Lista de agentes organizados por empresa
    agents_RE = [
        4313, 4314, 3430, 3431, 3432, 4415, 4315, 4316,
        3502, 3497, 3503, 3530, 3498, 3531, 3532, 3537,
        3538, 3947, 3948, 3969, 3970, 3976, 3972
    ]
    
    agents_DE = [3748]
    
    agents_AE = [
        3859, 3860, 3861, 3862, 3863, 3864,
        3740, 3741, 3750, 8011
    ]
    
    robot = StateGridRobot()
    
    print("Iniciando processamento dos agentes RE...")
    robot.process_all_agents(agents_RE)
    
    # print("\nIniciando processamento dos agentes DE...")
    # robot.process_all_agents(agents_DE)
    
    # print("\nIniciando processamento dos agentes AE...")
    # robot.process_all_agents(agents_AE)
    
    print("\nProcessamento concluído!")
    
    # Lista os arquivos baixados
    base_path = "C:\\Users\\Bruno\\Downloads\\Stategrid"
    print("\nArquivos baixados:")
    
    # Lista arquivos para todas as empresas
    for company, agents in [("RE", agents_RE), ("DE", agents_DE), ("AE", agents_AE)]:
        print(f"\nEmpresa {company}:")
        for agent in agents:
            agent_path = os.path.join(base_path, str(agent))
            if os.path.exists(agent_path):
                print(f"\nAgente {agent}:")
                for root, dirs, files in os.walk(agent_path):
                    level = root.replace(agent_path, '').count(os.sep)
                    indent = ' ' * 4 * level
                    print(f"{indent}{os.path.basename(root)}/")
                    subindent = ' ' * 4 * (level + 1)
                    for f in files:
                        print(f"{subindent}{f}")