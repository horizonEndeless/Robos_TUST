import requests
import os
from datetime import datetime

class DomPedroPortal:
    def __init__(self, codigo_ons):
        self.codigo_ons = codigo_ons
        self.base_proxy_url = "https://dompedro.useallcloud.com.br/"
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://dompedro.useallcloud.com.br",
            "Referer": "https://dompedro.useallcloud.com.br/portaltransmissoras/index.html",
            "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-platform": "Windows",
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty"
        }
        
    def efetuar_login(self):
        try:
            login_url = self.base_proxy_url + "apiportaltransmissoras/api/CliFornec/EfetuarLogin"
            data = {"CodigoOns": str(self.codigo_ons)}
            
            response = self.session.post(login_url, headers=self.headers, data=data)
            
            if response.status_code == 200:
                json_response = response.json()
                if json_response.get('Success'):
                    print("Login efetuado com sucesso.")
                    # Configurando cookies
                    self.session.cookies.set("EmpresaUseallTransmissoras", "1", domain="dompedro.useallcloud.com.br")
                    self.session.cookies.set("CodigoOnsUseallTransmissoras", str(self.codigo_ons), domain="dompedro.useallcloud.com.br")
                    return True
            return False
        except Exception as e:
            print(f"Erro ao acessar o portal: {str(e)}")
            return False
    
    def baixar_fatura_atual(self):
        try:
            print("\nBuscando fatura mais recente...")
            
            # Primeiro, recupera o nome ONS
            url_nome = self.base_proxy_url + "apiportaltransmissoras/api/VTcoFaturasParc/RecuperarNomeONS"
            print(f"Recuperando nome ONS: {url_nome}")
            response_nome = self.session.post(url_nome, headers=self.headers, data={"Codigo": str(self.codigo_ons)})
            print(f"Resposta nome ONS: {response_nome.text}")
            
            # Depois, recupera as faturas em aberto
            url_faturas = self.base_proxy_url + "apiportaltransmissoras/api/VTcoFaturasParc/RecuperarFaturasEmAberto"
            print(f"Recuperando faturas em aberto: {url_faturas}")
            response_faturas = self.session.post(url_faturas, headers=self.headers, data={"Codigo": str(self.codigo_ons)})
            
            if response_faturas.status_code == 200:
                json_response = response_faturas.json()
                if json_response.get('Success') and json_response.get('Content'):
                    faturas = json_response['Content'][0]['Faturas']
                    if faturas:
                        print(f"Faturas encontradas: {len(faturas)}")
                        fatura = faturas[0]  # Pega a primeira fatura
                        codigo_nf = fatura.get('CodigoCodNota')
                        print(f"Fatura selecionada: {codigo_nf}")
                        
                        # Gera o link do XML
                        url_xml = self.base_proxy_url + "apiportaltransmissoras/api/VTcoFaturasParc/GerarZIPXmlNFePorChave"
                        print(f"Gerando link do XML: {url_xml}")
                        
                        # Dados corretos para a requisição
                        xml_data = {
                            "CodigoNf": str(codigo_nf),
                            "CodigoEmpresa": "1"
                        }
                        print(f"Dados para geração do XML: {xml_data}")
                        
                        response_xml = self.session.post(url_xml, headers=self.headers, data=xml_data)
                        print(f"Resposta da geração do XML: {response_xml.text}")
                        
                        if response_xml.status_code == 200:
                            json_xml = response_xml.json()
                            if json_xml.get('Success') and json_xml.get('Content'):
                                download_url = "https:" + json_xml['Content']
                                print(f"URL de download: {download_url}")
                                
                                # Headers específicos para o download
                                download_headers = {
                                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                                    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                                    "Connection": "keep-alive",
                                    "Referer": "https://dompedro.useallcloud.com.br/",
                                    "Upgrade-Insecure-Requests": "1",
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
                                }
                                
                                zip_response = self.session.get(download_url, headers=download_headers)
                                if zip_response.status_code == 200:
                                    data_atual = datetime.now().strftime("%Y%m%d")
                                    pasta_destino = os.path.join(r"C:\Users\Bruno\Downloads\DPII", f"xmls_{data_atual}")
                                    os.makedirs(pasta_destino, exist_ok=True)
                                    
                                    nome_arquivo = download_url.split('/')[-1]
                                    caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
                                    
                                    with open(caminho_arquivo, 'wb') as f:
                                        f.write(zip_response.content)
                                    
                                    print(f"✓ Arquivo XML baixado com sucesso: {caminho_arquivo}")
                                    return True
                                else:
                                    print(f"✗ Erro ao baixar XML: {zip_response.status_code}")
                            else:
                                print(f"✗ Erro ao gerar link do XML: {json_xml.get('Message')}")
                        else:
                            print(f"✗ Erro ao solicitar link do XML: {response_xml.status_code}")
                    else:
                        print("✗ Nenhuma fatura encontrada")
                else:
                    print(f"✗ Erro na resposta: {json_response.get('Message')}")
            else:
                print(f"✗ Erro ao buscar faturas: {response_faturas.status_code}")
                print(f"Resposta: {response_faturas.text}")
            
            return False
            
        except Exception as e:
            print(f"✗ Erro ao baixar fatura: {str(e)}")
            print(f"Detalhes do erro: {type(e).__name__}")
            return False

if __name__ == "__main__":
    codigo_ons = "3748"
    portal = DomPedroPortal(codigo_ons)
    
    if portal.efetuar_login():
        portal.baixar_fatura_atual()
