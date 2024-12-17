import requests
import os
from datetime import datetime, timedelta
import zipfile
import xml.etree.ElementTree as ET

class BaseDownloader:
    def __init__(self):
        self.base_proxy_url = "https://dompedro.useallcloud.com.br/"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/131.0.0.0 Safari/537.36"
        }
        self.session = requests.Session()

    def baixar_fatura_atual(self, codigo_ons, nome_empresa, pasta_base):
        try:
            print(f"\nBuscando faturas disponíveis para {nome_empresa} (Código ONS: {codigo_ons})...")
            
            # Recupera todas as faturas em aberto
            url_faturas = self.base_proxy_url + "apiportaltransmissoras/api/VTcoFaturasParc/RecuperarFaturasEmAberto"
            response_faturas = self.session.post(url_faturas, headers=self.headers, data={"Codigo": str(codigo_ons)})
            
            if response_faturas.status_code == 200:
                json_response = response_faturas.json()
                if json_response.get('Success') and json_response.get('Content'):
                    faturas = json_response['Content'][0]['Faturas']
                    if faturas:
                        for fatura in faturas:
                            codigo_nf = fatura.get('CodigoCodNota')
                            print(f"Processando fatura {codigo_nf}...")
                            
                            # Download do XML
                            url_xml = self.base_proxy_url + "apiportaltransmissoras/api/VTcoFaturasParc/GerarZIPXmlNFePorChave"
                            xml_data = {"CodigoNf": str(codigo_nf), "CodigoEmpresa": "1"}
                            response_xml = self.session.post(url_xml, headers=self.headers, data=xml_data)
                            
                            if response_xml.status_code == 200:
                                json_xml = response_xml.json()
                                if json_xml.get('Success') and json_xml.get('Content'):
                                    download_url = "https:" + json_xml['Content']
                                    zip_response = self.session.get(download_url, headers=self.headers)
                                    
                                    if zip_response.status_code == 200:
                                        # Criar pasta temporária para extrair
                                        pasta_temp = os.path.join(pasta_base, nome_empresa, "temp")
                                        os.makedirs(pasta_temp, exist_ok=True)
                                        
                                        # Salvar e extrair ZIP
                                        temp_zip = os.path.join(pasta_temp, f"{codigo_nf}.zip")
                                        with open(temp_zip, 'wb') as f:
                                            f.write(zip_response.content)
                                        
                                        with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
                                            xml_files = [f for f in zip_ref.namelist() if f.endswith('.xml')]
                                            if xml_files:
                                                xml_content = zip_ref.read(xml_files[0])
                                                root = ET.fromstring(xml_content)
                                                
                                                # Verificar data no XML
                                                ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
                                                dh_emi = root.find('.//nfe:dhEmi', ns).text
                                                data_emissao = datetime.strptime(dh_emi.split('T')[0], '%Y-%m-%d')
                                                
                                                # Se for do mês vigente, move para pasta final
                                                hoje = datetime.now()
                                                if data_emissao.month == hoje.month and data_emissao.year == hoje.year:
                                                    pasta_destino = os.path.join(pasta_base, nome_empresa, data_emissao.strftime("%Y%m"))
                                                    os.makedirs(pasta_destino, exist_ok=True)
                                                    zip_ref.extractall(pasta_destino)
                                                    print(f"✓ Fatura {codigo_nf} validada e mantida (Mês vigente: {data_emissao.strftime('%m/%Y')})")
                                                else:
                                                    print(f"✗ Fatura {codigo_nf} descartada (Data: {data_emissao.strftime('%m/%Y')})")
                                        
                                        # Limpar arquivos temporários
                                        os.remove(temp_zip)
                                        if os.path.exists(pasta_temp):
                                            os.rmdir(pasta_temp)
                                    else:
                                        print(f"✗ Erro ao baixar XML da fatura {codigo_nf}: {zip_response.status_code}")
                                else:
                                    print(f"✗ Erro ao gerar link do XML da fatura {codigo_nf}: {json_xml.get('Message')}")
                            else:
                                print(f"✗ Erro ao solicitar link do XML da fatura {codigo_nf}: {response_xml.status_code}")
                    else:
                        print("✗ Nenhuma fatura encontrada")
                else:
                    print(f"✗ Erro na resposta: {json_response.get('Message')}")
            else:
                print(f"✗ Erro ao buscar faturas: {response_faturas.status_code}")
            
            return False
                
        except Exception as e:
            print(f"✗ Erro ao processar faturas para {nome_empresa}: {str(e)}")
            return False

class AEDownloader(BaseDownloader):
    def __init__(self):
        super().__init__()
        self.empresas = [
            ('3859', 'SJP1'), ('3860', 'SJP2'), ('3861', 'SJP3'),
            ('3862', 'SJP4'), ('3863', 'SJP5'), ('3864', 'SJP6'),
            ('3740', 'COR1'), ('3741', 'COR2'), ('3750', 'COR3'),
            ('8011', 'LIBRA')
        ]
        self.pasta_base = r"C:\Users\Bruno\Downloads\DPII\AE"

    def baixar_todas_faturas(self):
        print("Iniciando download das faturas AE...")
        for codigo_ons, nome_empresa in self.empresas:
            self.baixar_fatura_atual(codigo_ons, nome_empresa, self.pasta_base)
        print("Download AE finalizado!")

class REDownloader(BaseDownloader):
    def __init__(self):
        super().__init__()
        self.empresas = [
            ('4313', 'BRJA'), ('4314', 'BRJB'), ('3430', 'CECA'),
            ('3431', 'CECB'), ('3432', 'CECC'), ('4415', 'CECD'),
            ('4315', 'CECE'), ('4316', 'CECF'), ('3502', 'ITA1'),
            ('3497', 'ITA2'), ('3503', 'ITA3'), ('3530', 'ITA4'),
            ('3498', 'ITA5'), ('3531', 'ITA6'), ('3532', 'ITA7'),
            ('3537', 'ITA8'), ('3538', 'ITA9'), ('3947', 'SDBA'),
            ('3948', 'SDBB'), ('3969', 'SDBC'), ('3970', 'SDBD'),
            ('3976', 'SDBE'), ('3972', 'SDBF')
        ]
        self.pasta_base = r"C:\Users\Bruno\Downloads\DPII\RE"

    def baixar_todas_faturas(self):
        print("Iniciando download das faturas RE...")
        for codigo_ons, nome_empresa in self.empresas:
            self.baixar_fatura_atual(codigo_ons, nome_empresa, self.pasta_base)
        print("Download RE finalizado!")

class DEDownloader(BaseDownloader):
    def __init__(self):
        super().__init__()
        self.empresas = [
            ('3748', 'DE')
        ]
        self.pasta_base = r"C:\Users\Bruno\Downloads\DPII\DE"

    def baixar_todas_faturas(self):
        print("Iniciando download das faturas DE...")
        for codigo_ons, nome_empresa in self.empresas:
            self.baixar_fatura_atual(codigo_ons, nome_empresa, self.pasta_base)
        print("Download DE finalizado!")

def main():
    print("Iniciando processo de download dos XMLs...")
    print("=" * 50)
    
    # Download AE
    ae_downloader = AEDownloader()
    ae_downloader.baixar_todas_faturas()
    
    # Download RE
    re_downloader = REDownloader()
    re_downloader.baixar_todas_faturas()
    
    # Download DE
    de_downloader = DEDownloader()
    de_downloader.baixar_todas_faturas()
    
    print("\nProcesso finalizado!")

if __name__ == "__main__":
    main()
