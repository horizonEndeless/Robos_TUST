import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import pdfkit

class REDownloader:
    def __init__(self, ons_code, empresa):
        self.ons_code = ons_code
        self.empresa = empresa
        self.base_path = os.path.join(r"C:\Users\Bruno\Downloads\TUST\VERENE", "AE", str(ons_code))
        self.setup_base_directory()
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        self.wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        self.pdf_options = {
            'page-size': 'A4',
            'encoding': 'UTF-8',
            'no-images': False,
            'enable-local-file-access': True
        }

    def setup_base_directory(self):
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def setup_transmissora_directory(self, codigo, nome):
        dir_name = f"{codigo} - {nome}"
        transmissora_path = os.path.join(self.base_path, dir_name)
        if not os.path.exists(transmissora_path):
            os.makedirs(transmissora_path)
        return transmissora_path

    def download_file(self, url, transmissora_path, filename):
        try:
            response = self.session.get(url, headers=self.headers)
            if response.status_code == 200:
                filepath = os.path.join(transmissora_path, filename)
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"[{self.empresa}] Arquivo salvo: {filepath}")
                return True
        except Exception as e:
            print(f"[{self.empresa}] Erro ao baixar arquivo {filename}: {str(e)}")
        return False

    def download_boleto(self, url, transmissora_path, filename):
        try:
            response = self.session.get(url, headers=self.headers)
            if response.status_code == 200:
                temp_html = os.path.join(transmissora_path, 'temp_boleto.html')
                with open(temp_html, 'w', encoding='utf-8') as f:
                    f.write(response.text)

                pdf_path = os.path.join(transmissora_path, filename)
                config = pdfkit.configuration(wkhtmltopdf=self.wkhtmltopdf_path)
                pdfkit.from_file(temp_html, pdf_path, options=self.pdf_options, configuration=config)

                os.remove(temp_html)
                print(f"[{self.empresa}] Boleto salvo: {pdf_path}")
                return True
        except Exception as e:
            print(f"[{self.empresa}] Erro ao baixar boleto {filename}: {str(e)}")
        return False

    def run(self):
        try:
            print(f"\nIniciando download para {self.empresa} (ONS: {self.ons_code})")
            url = f"https://sys.sigetplus.com.br/cobranca/company/41/invoices?agent={self.ons_code}"
            response = self.session.get(url, headers=self.headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                rows = soup.select("table tbody tr")

                for row in rows:
                    transmissora_info = row.select_one("td:nth-child(1)").text.strip()
                    codigo = transmissora_info.split('-')[0].strip()
                    nome = transmissora_info.split('-')[1].strip()
                    
                    transmissora_path = self.setup_transmissora_directory(codigo, nome)
                    numero_fatura = row.select_one("td:nth-child(2) a").text.strip()
                    data_atual = datetime.now().strftime("%Y%m")
                    
                    # Download dos boletos
                    boleto_links = row.select("td:nth-child(4) a, td:nth-child(5) a, td:nth-child(6) a")
                    for i, boleto_link in enumerate(boleto_links, 1):
                        if boleto_link.get('href'):
                            boleto_filename = f"{numero_fatura}_boleto_{i}_{data_atual}.pdf"
                            self.download_boleto(boleto_link['href'], transmissora_path, boleto_filename)
                    
                    # Download XML e DANFE
                    xml_link = row.select_one("a[data-original-title='XML']")
                    danfe_link = row.select_one("a[data-original-title='DANFE']")
                    
                    if xml_link:
                        xml_url = xml_link['href']
                        filename = f"{numero_fatura}_{data_atual}.xml"
                        self.download_file(xml_url, transmissora_path, filename)
                    
                    if danfe_link:
                        danfe_url = danfe_link['href']
                        filename = f"{numero_fatura}_{data_atual}.pdf"
                        self.download_file(danfe_url, transmissora_path, filename)

        except Exception as e:
            print(f"[{self.empresa}] Erro durante a execução: {str(e)}")

def main():
    # Lista de empresas e seus códigos ONS
    empresas = [
        (3859, "SJP1"), (3860, "SJP2"), (3861, "SJP3"),
        (3862, "SJP4"), (3863, "SJP5"), (3864, "SJP6"),
        (3740, "COR1"), (3741, "COR2"), (3750, "COR3"),
        (8011, "LIBRA")
    ]

    for ons_code, empresa in empresas:
        downloader = REDownloader(ons_code, empresa)
        downloader.run()

if __name__ == "__main__":
    main()
