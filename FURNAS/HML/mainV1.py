import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import urllib3
import re
from html import unescape
from urllib.parse import quote, quote_plus

# Desabilitar avisos de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class FurnasScraper:
    def __init__(self):
        self.URL_DEFAULT = "http://portaldocliente.furnas.com.br/sap/bc/webdynpro/sap/zwda_portalclientes?sap-client=130&sap-theme=sap_bluecrystal"
        self.URL_LOGIN = "https://portaldocliente.furnas.com.br/sap/bc/webdynpro/sap/zwda_portalclientes?sap-contextid={}"
        self.URL_DOWNLOAD = "https://portaldocliente.furnas.com.br/sap/bc/webdynpro/sap/zwda_portalclientes"
        self.download_path = r"C:\Users\Bruno\Downloads\FURNAS"
        self.session = requests.Session()
        
        # Headers baseados no Postman
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Upgrade-Insecure-Requests': '1',
            'X-Requested-With': 'XMLHttpRequest'
        })

    def login(self, username, password):
        try:
            print("Fazendo requisição inicial...")
            response = self.session.get(self.URL_DEFAULT, verify=False)
            if not response.ok:
                print(f"Erro na requisição inicial: {response.status_code}")
                return False
            
            html = response.text
            
            # Extrair sap-contextid no formato correto
            sap_context_id = self._extract_value(html, "sap-contextid", "&#x3d;", "\"")
            sap_context_id = sap_context_id.replace("&#x25;3a", ":").replace("&#x25;", "%")
            print(f"sap_context_id: {sap_context_id}")
            
            sap_wd_secure_id = self._extract_value(html, "sap-wd-secure-id", "value=\"", "\"")
            print(f"sap_wd_secure_id: {sap_wd_secure_id}")
            
            login_url = self.URL_LOGIN.format(sap_context_id)
            print(f"URL de login: {login_url}")
            
            # Headers exatamente como no curl
            post_headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"'
            }
            
            # Primeiro enviar o ClientInspector_Notify
            client_data = {
                'sap-charset': 'utf-8',
                'sap-wd-secure-id': sap_wd_secure_id,
                '_stateful_': 'X',
                'SAPEVENTQUEUE': (
                    'ClientInspector_Notify~E002Id~E004WD01~E005Data~E004ClientHeight~003A150px~E003'
                    '~E002ResponseData~E004delta~E005EnqueueCardinality~E004single~E003~E002~E003'
                )
            }
            
            print("Enviando dados do cliente...")
            response = self.session.post(login_url, headers=post_headers, data=client_data, verify=False)
            if not response.ok:
                print(f"Erro ao enviar dados do cliente: {response.status_code}")
                return False
            
            # Depois enviar o usuário
            username_data = {
                'sap-charset': 'utf-8',
                'sap-wd-secure-id': sap_wd_secure_id,
                '_stateful_': 'X',
                'SAPEVENTQUEUE': (
                    f'ComboBox_Change~E002Id~E004WD2C~E005Value~E004{username.replace("@", "~0040")}~E003'
                    '~E002ResponseData~E004delta~E005EnqueueCardinality~E004single~E005Delay~E004full~E003~E002~E003'
                )
            }
            
            print("Enviando usuário...")
            response = self.session.post(login_url, headers=post_headers, data=username_data, verify=False)
            if not response.ok or 'sapLsFPMMessageArea' in response.text:
                print(f"Erro ao enviar usuário: {response.status_code}")
                return False
            
            # Depois enviar a senha
            password_data = {
                'sap-charset': 'utf-8',
                'sap-wd-secure-id': sap_wd_secure_id,
                '_stateful_': 'X',
                'SAPEVENTQUEUE': (
                    f'InputField_Change~E002Id~E004WD32~E005Value~E004{password}~E003'
                    '~E002ResponseData~E004delta~E005EnqueueCardinality~E004single~E005Delay~E004full~E003~E002~E003'
                )
            }
            
            print("Enviando senha...")
            response = self.session.post(login_url, headers=post_headers, data=password_data, verify=False)
            if not response.ok or 'sapLsFPMMessageArea' in response.text:
                print(f"Erro ao enviar senha: {response.status_code}")
                return False
            
            # Finalmente, enviar o clique no botão
            button_data = {
                'sap-charset': 'utf-8',
                'sap-wd-secure-id': sap_wd_secure_id,
                '_stateful_': 'X',
                'SAPEVENTQUEUE': (
                    'Button_Press~E002Id~E004WD39~E003'
                    '~E002ResponseData~E004delta~E005ClientAction~E004submit~E003~E002~E003'
                )
            }
            
            print("Clicando no botão...")
            response = self.session.post(login_url, headers=post_headers, data=button_data, verify=False)
            print(f"Status code: {response.status_code}")
            print(f"Resposta: {response.text[:500]}")
            
            if not response.ok or 'sapLsFPMMessageArea' in response.text:
                print(f"Erro ao clicar no botão: {response.status_code}")
                return False
            
            return 'lsTbsPanel2' in response.text
            
        except Exception as e:
            print(f"Erro no login: {str(e)}")
            return False

    def download_faturas(self):
        try:
            if not os.path.exists(self.download_path):
                os.makedirs(self.download_path)
                
            # TODO: Implementar lógica de download baseada nas requisições do Postman
            # 1. Navegar pelas abas (TabStrip_TabSelect)
            # 2. Clicar nos botões de download (Button_Press)
            # 3. Baixar os arquivos XML/PDF usando as URLs de download
            
        except Exception as e:
            print(f"Erro ao baixar faturas: {str(e)}")

    def _extract_value(self, html, input_id, value_delimiter, value_index_of):
        try:
            name_pos = html.find(input_id)
            if name_pos == -1:
                print(f"Não encontrou {input_id}")
                return ""
            value_pos = html.find(value_delimiter, name_pos)
            if value_pos == -1:
                print(f"Não encontrou {value_delimiter}")
                return ""
            start_pos = value_pos + len(value_delimiter)
            end_pos = html.find(value_index_of, start_pos)
            if end_pos == -1:
                print(f"Não encontrou {value_index_of}")
                return ""
            return html[start_pos:end_pos]
        except Exception as e:
            print(f"Erro ao extrair valor: {str(e)}")
            return ""

def main():
    scraper = FurnasScraper()
    if scraper.login("tust@rioenergy.com.br", "tustre3430"):
        print("Login realizado com sucesso!")
        scraper.download_faturas()
    else:
        print("Falha no login!")

if __name__ == "__main__":
    main()
