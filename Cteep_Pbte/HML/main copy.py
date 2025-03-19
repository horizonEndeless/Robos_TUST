import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import zipfile
import shutil
import tempfile

class CteepRobot:
    def __init__(self, empresa="LIBRAS"):
        self.session = requests.Session()
        self.base_url = "https://faturamento.isaenergiabrasil.com.br"
        self.empresa = empresa
        
        # Configurações por empresa
        self.empresas = {
            "LIBRAS": {
                "usuario": "kleber@libraligas.com.br",
                "senha": "542D1G6"
            },
            "COREMAS": {
                "usuario": "fatura.coremas@americaenergia.com.br",
                "senha": "2M4TO12"
            },
            "SJP": {
                "usuario": "faturas.sjp@americaenergia.com.br",
                "senha": "QM17DIB10"
            }
        }
        
        self.credentials = self.empresas[empresa]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": self.base_url,
            "Referer": f"{self.base_url}/index.asp"
        }

    def login(self):
        try:
            # Primeiro acessa a página inicial
            initial_response = self.session.get(f"{self.base_url}/index.asp", headers=self.headers)
            print(f"Status página inicial: {initial_response.status_code}")
            
            # Faz o login
            login_url = f"{self.base_url}/login.asp"
            response = self.session.post(
                login_url, 
                data=self.credentials,
                headers=self.headers,
                allow_redirects=True  # Mudado para True para seguir redirecionamentos
            )
            
            print(f"Status login: {response.status_code}")
            print(f"URL após login: {response.url}")
            
            if "RB.asp" in response.url:
                print("Login realizado com sucesso!")
                return True
            else:
                print(f"Falha no login! URL atual: {response.url}")
                return False
                
        except Exception as e:
            print(f"Erro durante o login: {str(e)}")
            return False

    def download_fatura(self, num_fatura, tipo="xml"):
        try:
            # Define o diretório para salvar os arquivos
            download_dir = os.path.join(r"C:\Users\Bruno\Downloads\ISA", self.empresa, datetime.now().strftime("%Y-%m"), num_fatura)
            os.makedirs(download_dir, exist_ok=True)
            
            # URL para download da fatura
            download_url = f"{self.base_url}/download.asp"
            params = {
                "mode": "admin",
                "arquivo": "zip",
                "tipo": tipo,
                "num_fatura": num_fatura
            }
            
            # Realiza o download
            response = self.session.get(download_url, params=params)
            
            if response.status_code == 200:
                # Define o nome do arquivo
                filename = f"{self.empresa}_{num_fatura}_{tipo}.zip"
                filepath = os.path.join(download_dir, filename)
                
                # Salva o arquivo
                with open(filepath, "wb") as f:
                    f.write(response.content)
                    
                print(f"Arquivo {filename} baixado com sucesso!")
                return filepath
                
            else:
                print(f"Erro ao baixar fatura {num_fatura}")
                return None
                
        except Exception as e:
            print(f"Erro durante o download: {str(e)}")
            return None

    def merge_boleto_into_xml(self, xml_path, boleto_path):
        try:
            # Define o nome do arquivo merged
            xml_dir = os.path.dirname(xml_path)
            merged_filename = f"LIBRAS_merged_{os.path.basename(xml_path)}"
            merged_path = os.path.join(xml_dir, merged_filename)
            
            # Cria uma cópia do XML original
            shutil.copy2(xml_path, merged_path)
            
            # Cria um diretório temporário
            with tempfile.TemporaryDirectory() as temp_dir:
                # Extrai o boleto
                with zipfile.ZipFile(boleto_path, 'r') as boleto_zip:
                    boleto_zip.extractall(temp_dir)
                
                # Adiciona o conteúdo do boleto ao XML.zip
                with zipfile.ZipFile(merged_path, 'a') as xml_zip:
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, temp_dir)
                            xml_zip.write(file_path, arcname)
                
                # Remove os arquivos originais
                os.remove(xml_path)
                os.remove(boleto_path)
                
                print(f"Arquivos mesclados com sucesso em {merged_path}")
                return True

        except Exception as e:
            print(f"Erro ao mesclar arquivos: {str(e)}")
            return False

    def get_faturas(self):
        """Obtém as faturas disponíveis na página"""
        try:
            # Primeiro acessa a página RB.asp para pegar o formulário
            response = self.session.get(f"{self.base_url}/RB.asp", headers=self.headers)
            print(f"Status página inicial RB: {response.status_code}")
            
            # Configura para dezembro/2024
            data_param = "2024|12"
            print(f"Buscando faturas para: {data_param}")
            
            # Envia o formulário com o mês selecionado
            form_data = {
                "data": data_param
            }
            
            response = self.session.post(
                f"{self.base_url}/RB.asp",
                data=form_data,
                headers=self.headers
            )
            
            print(f"Status após envio do formulário: {response.status_code}")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            faturas = []
            
            # Procura todas as fieldsets
            fieldsets = soup.find_all('fieldset')
            print(f"Encontrados {len(fieldsets)} fieldsets")
            
            for fieldset in fieldsets:
                legend = fieldset.find('legend')
                if legend:
                    empresa_fieldset = legend.text.strip()
                    print(f"\nProcessando fieldset: {empresa_fieldset}")
                    
                    # Processa LIBRAS, COREMAS e SJP
                    if ((self.empresa == "COREMAS" and "COREMAS" in empresa_fieldset) or 
                        (self.empresa == "LIBRAS" and "LIBRA LIGAS" in empresa_fieldset) or
                        (self.empresa == "SJP" and "CELEO SAO JOAO DO PIAUI" in empresa_fieldset)):
                        
                        table = fieldset.find('table')
                        if table:
                            rows = table.find_all('tr')
                            for row in rows:
                                # Pula cabeçalho e linha de total
                                if 'titulo_tabela' in row.get('class', []) or 'Total' in row.text:
                                    continue
                                
                                cols = row.find_all('td')
                                if len(cols) >= 6:
                                    empreendimento = cols[0].text.strip()
                                    num_fatura = cols[2].text.strip()
                                    
                                    # Verifica se tem link de boleto
                                    has_boleto = bool(cols[5].find('a'))
                                    tipos = ["xml"]
                                    if has_boleto:
                                        tipos.append("boleto")
                                    
                                    print(f"Fatura encontrada: {empreendimento} - {num_fatura} - Tipos: {tipos}")
                                    
                                    faturas.append({
                                        "numero": num_fatura,
                                        "tipos": tipos,
                                        "empreendimento": empreendimento
                                    })
            
            print(f"\nTotal de faturas encontradas: {len(faturas)}")
            for f in faturas:
                print(f"- {f['empreendimento']}: {f['numero']} ({', '.join(f['tipos'])})")
            
            return faturas
            
        except Exception as e:
            print(f"Erro ao obter faturas: {str(e)}")
            print(f"Detalhes do erro: {e.__class__.__name__}")
            return []

    def executar(self):
        if self.login():
            # Obtém as faturas dinamicamente
            faturas = self.get_faturas()
            
            print(f"\nProcessando faturas da {self.empresa}")
            for fatura in faturas:
                xml_path = None
                boleto_path = None
                
                print(f"Processando fatura {fatura['numero']} - {fatura['empreendimento']}")
                
                for tipo in fatura["tipos"]:
                    if tipo == "xml":
                        xml_path = self.download_fatura(fatura["numero"], tipo)
                    elif tipo == "boleto":
                        boleto_path = self.download_fatura(fatura["numero"], tipo)
                
                if xml_path and boleto_path:
                    self.merge_boleto_into_xml(xml_path, boleto_path)

if __name__ == "__main__":
    empresas = ["LIBRAS", "COREMAS", "SJP"]
    
    for empresa in empresas:
        try:
            print(f"\nIniciando processamento da empresa: {empresa}")
            robot = CteepRobot(empresa)
            robot.executar()
        except Exception as e:
            print(f"Erro ao processar empresa {empresa}: {str(e)}")
