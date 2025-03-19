import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import pdfkit

class REDownloader:
    def __init__(self, ons_code, empresa, periodo=None):
        self.ons_code = ons_code
        self.empresa = empresa
        self.periodo = self.formatar_periodo(periodo) or datetime.now().strftime("%m/%Y")  # Formato padrão: mês/ano
        self.base_path = os.path.join(r"C:\Users\Bruno\Downloads\TUST\VERENE\DEZEMBRO_2024", "RE", str(ons_code))
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

    def formatar_periodo(self, periodo):
        if not periodo:
            return None
            
        # Remove espaços em branco
        periodo = periodo.strip()
        
        # Verifica se já está no formato MM/AAAA
        if '/' in periodo:
            return periodo
            
        # Tenta converter formatos como MMAAAA (ex: 122024)
        if len(periodo) == 6 and periodo.isdigit():
            return f"{periodo[:2]}/{periodo[2:]}"
        
        # Tenta converter formatos como MAAAA (ex: 12024)
        if len(periodo) == 5 and periodo.isdigit():
            return f"0{periodo[0]}/{periodo[1:]}"
            
        # Tenta converter formatos como YYYYMM (ex: 202412)
        if len(periodo) == 6 and periodo.isdigit():
            return f"{periodo[4:]}/{periodo[:4]}"
            
        return periodo  # Retorna como está se não conseguir formatar

    def run(self):
        try:
            print(f"\nIniciando download para {self.empresa} (ONS: {self.ons_code}) - Período: {self.periodo}")
            
            # Extrair mês e ano do período
            try:
                if '/' in self.periodo:
                    mes, ano = self.periodo.split('/')
                else:
                    # Tratamento de fallback caso o formato ainda esteja incorreto
                    print(f"[{self.empresa}] Formato de período inválido: {self.periodo}. Usando mês atual.")
                    mes = datetime.now().strftime("%m")
                    ano = datetime.now().strftime("%Y")
            except Exception as e:
                print(f"[{self.empresa}] Erro ao processar período: {str(e)}. Usando mês atual.")
                mes = datetime.now().strftime("%m")
                ano = datetime.now().strftime("%Y")
                
            mes_formatado = mes.zfill(2)  # Garante que o mês tenha dois dígitos
            
            # Formato YYYYMM para a URL
            periodo_url = f"{ano}{mes_formatado}"
            
            url = f"https://sys.sigetplus.com.br/cobranca/company/41/invoices?agent={self.ons_code}&time={periodo_url}"
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
                    data_formatada = f"{ano}{mes_formatado}"
                    
                    # Download dos boletos
                    boleto_links = row.select("td:nth-child(4) a, td:nth-child(5) a, td:nth-child(6) a")
                    for i, boleto_link in enumerate(boleto_links, 1):
                        if boleto_link.get('href'):
                            boleto_filename = f"{numero_fatura}_boleto_{i}_{data_formatada}.pdf"
                            self.download_boleto(boleto_link['href'], transmissora_path, boleto_filename)
                    
                    # Download XML e DANFE
                    xml_link = row.select_one("a[data-original-title='XML']")
                    danfe_link = row.select_one("a[data-original-title='DANFE']")
                    
                    if xml_link:
                        xml_url = xml_link['href']
                        filename = f"{numero_fatura}_{data_formatada}.xml"
                        self.download_file(xml_url, transmissora_path, filename)
                    
                    if danfe_link:
                        danfe_url = danfe_link['href']
                        filename = f"{numero_fatura}_{data_formatada}.pdf"
                        self.download_file(danfe_url, transmissora_path, filename)

        except Exception as e:
            print(f"[{self.empresa}] Erro durante a execução: {str(e)}")

def main():
    # Lista de empresas e seus códigos ONS
    empresas = [
        (4313, "BRJA"), (4314, "BRJB"), (3430, "CECA"),
        (3431, "CECB"), (3432, "CECC"), (4415, "CECD"),
        (4315, "CECE"), (4316, "CECF"), (3502, "ITA1"),
        (3497, "ITA2"), (3503, "ITA3"), (3530, "ITA4"),
        (3498, "ITA5"), (3531, "ITA6"), (3532, "ITA7"),
        (3537, "ITA8"), (3538, "ITA9"), (3947, "SDBA"),
        (3948, "SDBB"), (3969, "SDBC"), (3970, "SDBD"),
        (3976, "SDBE"), (3972, "SDBF")
    ]

    # Solicitar o período desejado
    periodo = input("Digite o período desejado (MM/AAAA) ou pressione Enter para usar o mês atual: ")
    
    for ons_code, empresa in empresas:
        downloader = REDownloader(ons_code, empresa, periodo)
        downloader.run()

if __name__ == "__main__":
    main()
