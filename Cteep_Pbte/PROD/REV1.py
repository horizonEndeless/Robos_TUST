import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import zipfile
import shutil
import tempfile

class CteepRobot:
    def __init__(self, empresa="RE"):
        self.session = requests.Session()
        self.base_url = "https://faturamento.isaenergiabrasil.com.br"
        self.empresa = empresa
        
        # Configurações por empresa
        self.empresas = {
            "RE": {
                "credencial1": {
                    "usuario": "rodrigo.abrantes@rioenergy.com.br",
                    "senha": "625L5Q0"
                },
                "credencial2": {
                    "usuario": "tust@rioenergyllc.com",
                    "senha": "1XAVYIU04"
                },
                # "credencial3": {
                #     "usuario": "rodrigo.abrantes@rioenergy.com.br",
                #     "senha": "625L5Q0"
                # }
            }
        }
        
        # Inicialmente usa a primeira credencial
        self.current_credential = "credencial1"
        self.credentials = self.empresas[empresa][self.current_credential]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": self.base_url,
            "Referer": f"{self.base_url}/index.asp"
        }

        # Mapeamento de empresas e seus códigos
        self.empresa_mapping = {
            "BRJA": "4313 - EÓLICA BREJINHOS ALFA S.A",
            "BRJB": "4314 - EÓLICA BREJINHOS B S.A.",
            "CECA": "3430 - EOLICA CAETITE A S.A.",
            "CECB": "3431 - EOLICA CAETITE B S.A.",
            "CECC": "3432 - EOLICA CAETITE C S.A.",
            "CECD": "4415 - EOLICA CAETITE D S.A.",
            "CECE": "4315 - EÓLICA CAETITÉ ECO S.A",
            "CECF": "4316 - EÓLICA CAETITÉ F S.A.",
            "ITA1": "3502 - EÓLICA ITAREMA I S.A.",
            "ITA2": "3497 - EÓLICA ITAREMA II S.A.",
            "ITA3": "3503 - EOLICA ITAREMA III S.A.",
            "ITA4": "3530 - EOLICA ITAREMA IV S.A.",
            "ITA5": "3498 - EOLICA ITAREMA V S.A.",
            "ITA6": "3531 - EOLICA ITAREMA VI S.A.",
            "ITA7": "3532 - EOLICA ITAREMA VII S.A.",
            "ITA8": "3537 - EOLICA ITAREMA VIII S.A.",
            "ITA9": "3538 - EOLICA ITAREMA IX S.A.",
            "SDBA": "3947 - EÓLICA SDB ALFA S.A.",
            "SDBB": "3948 - EÓLICA SDB B S.A.",
            "SDBC": "3969 - EÓLICA SDB C S.A.",
            "SDBD": "3970 - EÓLICA SDB D S.A.",
            "SDBE": "3976 - EÓLICA SDB ECO S.A.",
            "SDBF": "3972 - EÓLICA SDB F S.A."
        }

        # Adicionar categorização das empresas
        self.empresa_categorias = {
            "TRANSMISSORAS": ["1009 - CTEEP", "CTEEP PBTE", "1240 - CTEEP (PBTE)"],
            "BREJINHOS": ["BRJA", "BRJB"],
            "CAETITE": ["CECA", "CECB", "CECC", "CECD", "CECE", "CECF"],
            "ITAREMA": ["ITA1", "ITA2", "ITA3", "ITA4", "ITA5", "ITA6", "ITA7", "ITA8", "ITA9"],
            "SDB": ["SDBA", "SDBB", "SDBC", "SDBD", "SDBE", "SDBF"]
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

    def get_empresa_code(self, empreendimento):
        """Retorna o código da empresa baseado no nome do empreendimento"""
        for codigo, nome in self.empresa_mapping.items():
            if nome.split(" - ")[1] in empreendimento:
                return codigo
        return None

    def get_categoria_empresa(self, empresa_nome):
        """Retorna a categoria da empresa baseado no nome"""
        if "CTEEP" in empresa_nome:
            return "TRANSMISSORAS"
        
        for categoria, empresas in self.empresa_categorias.items():
            for empresa in empresas:
                if empresa in empresa_nome or empresa in self.get_empresa_code(empresa_nome):
                    return categoria
        return "OUTROS"

    def download_fatura(self, num_fatura, tipo="xml", codigo_ons="", empresa_nome=""):
        try:
            # Define o diretório base
            base_dir = os.path.join(r"C:\Users\Bruno\Downloads\ISA", self.empresa, datetime.now().strftime("%Y-%m"))
            
            # Determina a categoria e código da empresa
            categoria = self.get_categoria_empresa(empresa_nome)
            empresa_code = self.get_empresa_code(empresa_nome)
            
            if categoria == "TRANSMISSORAS":
                if "PBTE" in empresa_nome:
                    download_dir = os.path.join(base_dir, categoria, "PBTE", num_fatura)
                else:
                    download_dir = os.path.join(base_dir, categoria, "CTEEP", num_fatura)
            elif empresa_code:
                download_dir = os.path.join(base_dir, categoria, empresa_code, num_fatura)
            else:
                download_dir = os.path.join(base_dir, "OUTROS", num_fatura)
                
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
                # Define o nome do arquivo zip temporário
                temp_zip = os.path.join(download_dir, f"temp_{self.empresa}_{num_fatura}_{tipo}.zip")
                
                # Salva o arquivo zip temporário
                with open(temp_zip, "wb") as f:
                    f.write(response.content)
                
                # Extrai os arquivos
                with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
                    zip_ref.extractall(download_dir)
                
                # Remove o arquivo zip temporário
                os.remove(temp_zip)
                
                # Retorna o diretório onde os arquivos foram extraídos
                print(f"Arquivos da fatura {num_fatura} extraídos com sucesso em {download_dir}")
                return download_dir
                
            else:
                print(f"Erro ao baixar fatura {num_fatura}")
                return None
                
        except Exception as e:
            print(f"Erro durante o download: {str(e)}")
            return None

    def merge_boleto_into_xml(self, xml_dir, boleto_dir):
        try:
            # Como os arquivos já estão extraídos, apenas movemos os arquivos do boleto para o diretório do XML
            for item in os.listdir(boleto_dir):
                source = os.path.join(boleto_dir, item)
                dest = os.path.join(xml_dir, item)
                if os.path.isfile(source):
                    shutil.copy2(source, dest)
            
            print(f"Arquivos mesclados com sucesso em {xml_dir}")
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
            data_param = "2025|01"
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
                    
                    # Processa RE
                    if self.empresa == "RE":
                        table = fieldset.find('table')
                        if table:
                            rows = table.find_all('tr')
                            for row in rows:
                                if 'titulo_tabela' in row.get('class', []) or 'Total' in row.text:
                                    continue
                                
                                cols = row.find_all('td')
                                if len(cols) >= 6:
                                    empreendimento = cols[0].text.strip()
                                    num_fatura = cols[2].text.strip()
                                    
                                    # Extrai o código ONS do empreendimento
                                    codigo_ons = ""
                                    if "1009" in empreendimento:
                                        codigo_ons = "1009 - CTEEP"
                                    elif "PBTE" in empreendimento:
                                        codigo_ons = "1240 - CTEEP (PBTE)"
                                    
                                    has_boleto = bool(cols[5].find('a'))
                                    tipos = ["xml"]
                                    if has_boleto:
                                        tipos.append("boleto")
                                    
                                    faturas.append({
                                        "numero": num_fatura,
                                        "tipos": tipos,
                                        "empreendimento": empreendimento,
                                        "codigo_ons": codigo_ons
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
            faturas = self.get_faturas()
            
            print(f"\nProcessando faturas da {self.empresa}")
            for fatura in faturas:
                xml_path = None
                boleto_path = None
                
                print(f"Processando fatura {fatura['numero']} - {fatura['empreendimento']}")
                
                for tipo in fatura["tipos"]:
                    if tipo == "xml":
                        xml_path = self.download_fatura(
                            fatura["numero"], 
                            tipo, 
                            fatura["codigo_ons"],
                            fatura["empreendimento"]
                        )
                    elif tipo == "boleto":
                        boleto_path = self.download_fatura(
                            fatura["numero"], 
                            tipo, 
                            fatura["codigo_ons"],
                            fatura["empreendimento"]
                        )
                
                if xml_path and boleto_path:
                    self.merge_boleto_into_xml(xml_path, boleto_path)

if __name__ == "__main__":
    empresas = ["RE"]
    
    for empresa in empresas:
        try:
            print(f"\nIniciando processamento da empresa: {empresa}")
            robot = CteepRobot(empresa)
            robot.executar()
        except Exception as e:
            print(f"Erro ao processar empresa {empresa}: {str(e)}")
