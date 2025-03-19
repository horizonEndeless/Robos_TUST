import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

class ETTMRobot:
    def __init__(self):
        self.session = requests.Session()
        self.base_path = r"C:\Users\Bruno\Downloads\TUST\ETTM"
        # Organizando as empresas por tipo
        self.companies = {
            # RE
            "RE": {
                "4313": "BRJA",
                "4314": "BRJB",
                "3430": "CECA",
                "3431": "CECB",
                "3432": "CECC",
                "4415": "CECD",
                "4315": "CECE",
                "4316": "CECF",
                "3502": "ITA1",
                "3497": "ITA2",
                "3503": "ITA3",
                "3530": "ITA4",
                "3498": "ITA5",
                "3531": "ITA6",
                "3532": "ITA7",
                "3537": "ITA8",
                "3538": "ITA9",
                "3947": "SDBA",
                "3948": "SDBB",
                "3969": "SDBC",
                "3970": "SDBD",
                "3976": "SDBE",
                "3972": "SDBF",
            },
            # AE
            "AE": {
                "3859": "SJP1",
                "3860": "SJP2",
                "3861": "SJP3",
                "3862": "SJP4",
                "3863": "SJP5",
                "3864": "SJP6",
                "3740": "COR1",
                "3741": "COR2",
                "3750": "COR3",
                "8011": "LIBRA",
            },
            # DE
            "DE": {
                "3784": "DE"
            }
        }

    def download_document(self, url, filename, agent_id, doc_type):
        """
        Faz download de um documento (XML ou DANFE)
        """
        try:
            # Identificar o tipo de documento (RE, AE ou DE)
            for tipo, empresas in self.companies.items():
                if agent_id in empresas:
                    doc_type = tipo
                    break
                    
            download_path = os.path.join(self.base_path, doc_type, agent_id)
            response = self.session.get(url)
            if response.status_code == 200:
                file_path = os.path.join(download_path, filename)
                os.makedirs(download_path, exist_ok=True)
                
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f"Arquivo salvo com sucesso em: {file_path}")
                return True
            else:
                print(f"Erro ao baixar arquivo {filename}. Status code: {response.status_code}")
                return False
        except Exception as e:
            print(f"Erro ao processar download de {filename}: {str(e)}")
            return False

    def get_invoice_documents(self, agent_id, doc_type):
        """
        Obtém os documentos da fatura atual para um agente específico
        """
        company_name = self.companies[doc_type].get(agent_id, "")
        url = f"https://sys.sigetplus.com.br/cobranca/transmitter/1311/invoices?agent={agent_id}"
        
        try:
            print(f"\nProcessando empresa: {company_name} (Agente: {agent_id})")
            response = self.session.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Encontrar links de XML e DANFE
            xml_link = soup.find('a', {'data-original-title': 'XML'})
            danfe_link = soup.find('a', {'data-original-title': 'DANFE'})
            
            if xml_link and danfe_link:
                xml_url = xml_link.get('href')
                danfe_url = danfe_link.get('href')
                
                # Extrair número da fatura para nomear arquivos
                invoice_number = soup.find('a', href=lambda x: x and 'invoices' in x).text.strip()
                
                # Download dos documentos
                current_date = datetime.now().strftime("%Y%m")
                self.download_document(xml_url, f"{company_name}_NFe_{invoice_number}_{current_date}.xml", agent_id, doc_type)
                self.download_document(danfe_url, f"{company_name}_DANFE_{invoice_number}_{current_date}.pdf", agent_id, doc_type)
                
            else:
                print(f"Links dos documentos não encontrados para {company_name}")
                
        except Exception as e:
            print(f"Erro ao processar página para {company_name}: {str(e)}")

def main():
    robot = ETTMRobot()
    
    # Processar todas as empresas por tipo
    for doc_type, companies in robot.companies.items():
        print(f"\nProcessando documentos do tipo: {doc_type}")
        for agent_id in companies.keys():
            robot.get_invoice_documents(agent_id, doc_type)

if __name__ == "__main__":
    main()
