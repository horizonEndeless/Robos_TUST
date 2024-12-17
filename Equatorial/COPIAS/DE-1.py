import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

class EquatorialClient:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://www.equatorial-t.com.br",
            "Referer": "https://www.equatorial-t.com.br/"
        }
        
    def login(self, cnpj, ons, spe):
        """
        Realiza o login no sistema da Equatorial
        """
        login_url = "https://www.equatorial-t.com.br/login-cliente"
        
        # Dados do formulário de login
        login_data = {
            "user_cnpj": cnpj,
            "user_ons": ons,
            "user_spe": spe.lower(),  # Garante que está em minúsculo
            "redirect_to": "",
            "testcookie": "1",
            "wp-submit": "Entrar"
        }
        
        # Headers específicos para o login
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://www.equatorial-t.com.br",
            "Referer": "https://www.equatorial-t.com.br/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }
        
        try:
            # Primeiro, faz uma requisição GET para pegar cookies iniciais
            self.session.get("https://www.equatorial-t.com.br/")
            
            # Faz o login
            response = self.session.post(
                login_url,
                data=login_data,
                headers=headers,
                allow_redirects=True
            )
            
            # Verifica se foi redirecionado para a página correta
            if "segunda-via-transmissao" in response.url:
                print(f"Login realizado com sucesso para {spe}!")
                return True
            else:
                print(f"Falha no login para {spe}. URL atual: {response.url}")
                return False
                
        except Exception as e:
            print(f"Erro durante o login para {spe}: {str(e)}")
            return False
    
    def buscar_faturas_por_data(self, mes, ano):
        """
        Busca as faturas disponíveis para um determinado mês e ano
        """
        url = "https://www.equatorial-t.com.br/segunda-via-transmissao/"
        
        try:
            response = self.session.get(url, headers=self.headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                faturas = []
                
                tabela = soup.find('table')
                if tabela:
                    rows = tabela.find_all('tr')
                    
                    for row in rows[1:]:  # Pula o cabeçalho
                        cells = row.find_all('td')
                        if len(cells) >= 7:  # Garantir que tem células suficientes
                            status = cells[0].text.strip()
                            
                            if "Em aberto" in status:
                                ons = cells[1].text.strip()
                                spe = cells[2].text.strip()
                                mes_fatura = cells[3].text.strip()
                                ano_fatura = cells[4].text.strip()
                                
                                # Pegar os links de download e adicionar URL base
                                xml_link = cells[5].find('a')['href'] if cells[5].find('a') else None
                                pdf_link = cells[6].find('a')['href'] if cells[6].find('a') else None
                                
                                # Adicionar URL base aos links
                                if xml_link and not xml_link.startswith('http'):
                                    xml_link = f"https://www.equatorial-t.com.br/segunda-via-transmissao/{xml_link}"
                                if pdf_link and not pdf_link.startswith('http'):
                                    pdf_link = f"https://www.equatorial-t.com.br/segunda-via-transmissao/{pdf_link}"
                                
                                if mes_fatura == str(mes) and ano_fatura == str(ano):
                                    faturas.append({
                                        'ons': ons,
                                        'spe': spe,
                                        'mes': mes_fatura,
                                        'ano': ano_fatura,
                                        'xml_link': xml_link,
                                        'pdf_link': pdf_link
                                    })
                                    print(f"Fatura em aberto encontrada: {mes_fatura}/{ano_fatura}")
                                    print(f"Links - XML: {xml_link}, PDF: {pdf_link}")
                
                return faturas
            else:
                print("Nenhuma tabela encontrada na página!")
                return []
                
        except Exception as e:
            print(f"Erro durante a busca: {str(e)}")
            return []
    
    def baixar_fatura(self, fatura_info, tipo='xml', diretorio_base=r"C:\Users\Bruno\Downloads\EQUATORIAL"):
        """
        Baixa a fatura no formato especificado (xml ou pdf)
        """
        try:
            # Criar diretório base se não existir
            os.makedirs(diretorio_base, exist_ok=True)
            
            # Criar subdiretório para a empresa/SPE
            diretorio_saida = os.path.join(diretorio_base, f"{fatura_info['spe']}")
            os.makedirs(diretorio_saida, exist_ok=True)
            
            link = fatura_info['xml_link'] if tipo == 'xml' else fatura_info['pdf_link']
            extensao = 'xml' if tipo == 'xml' else 'pdf'
            
            if not link:
                print(f"Link para {tipo.upper()} não encontrado")
                return False
            
            response = self.session.get(link, headers=self.headers)
            if response.status_code == 200:
                nome_arquivo = f"fatura_{fatura_info['ons']}_{fatura_info['spe']}_{fatura_info['mes']}_{fatura_info['ano']}.{extensao}"
                caminho_completo = os.path.join(diretorio_saida, nome_arquivo)
                
                with open(caminho_completo, 'wb') as f:
                    f.write(response.content)
                
                print(f"Arquivo {tipo.upper()} salvo com sucesso: {caminho_completo}")
                return True
            else:
                print(f"Erro ao baixar {tipo.upper()}. Status code: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Erro durante o download do {tipo.upper()}: {str(e)}")
            return False
    
    def processar_todas_spes(self, mes, ano):
        """
        Processa todas as SPEs de sp01 até sp08
        """
        for sp_num in range(1, 9):
            spe = f"sp0{sp_num}"
            print(f"\nProcessando {spe}...")
            
            # Cria uma nova sessão para cada SPE
            self.session = requests.Session()
            
            # Faz login com a SPE atual
            if self.login("27093977000238", "3748", spe):
                faturas = self.buscar_faturas_por_data(mes, ano)
                
                if faturas:
                    for fatura in faturas:
                        self.baixar_fatura(fatura, tipo='xml')
                        self.baixar_fatura(fatura, tipo='pdf')
                else:
                    print(f"Nenhuma fatura em aberto encontrada para {spe} no período {mes}/{ano}")
            else:
                print(f"Falha no login para {spe}")

# Exemplo de uso
if __name__ == "__main__":
    client = EquatorialClient()
    
    # Processa todas as SPEs
    client.processar_todas_spes(11, 2024)
