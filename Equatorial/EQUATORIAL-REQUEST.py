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
        
        # Dicionário de empresas
        self.empresas = {
            "DE": [  # DiamantEnergia
                {"cnpj": "27093977000238", "ons": "3748", "codigo": "", "empresa": "DE"}
            ],
            "RE": [  # RioEnergy
                {"cnpj": "33485728000100", "ons": "4313", "codigo": "1108376", "empresa": "BRJA"},
                {"cnpj": "33485874000135", "ons": "4314", "codigo": "1108377", "empresa": "BRJB"},
                {"cnpj": "19233858000205", "ons": "3430", "codigo": "1101532", "empresa": "CECA"},
                {"cnpj": "19235607000260", "ons": "3431", "codigo": "1101533", "empresa": "CECB"},
                {"cnpj": "19560109000292", "ons": "3432", "codigo": "1101534", "empresa": "CECC"},
                {"cnpj": "33457932000117", "ons": "4415", "codigo": "1108935", "empresa": "CECD"},
                {"cnpj": "33471379000177", "ons": "4315", "codigo": "1108378", "empresa": "CECE"},
                {"cnpj": "33468809000100", "ons": "4316", "codigo": "1108379", "empresa": "CECF"},
                {"cnpj": "19560032000250", "ons": "3502", "codigo": "1101690", "empresa": "ITA1"},
                {"cnpj": "19560074000291", "ons": "3497", "codigo": "1101632", "empresa": "ITA2"},
                {"cnpj": "19560839000293", "ons": "3503", "codigo": "1101691", "empresa": "ITA3"},
                {"cnpj": "20553751000223", "ons": "3530", "codigo": "1101738", "empresa": "ITA4"},
                {"cnpj": "19560868000255", "ons": "3498", "codigo": "1101633", "empresa": "ITA5"},
                {"cnpj": "20533879000225", "ons": "3531", "codigo": "1101739", "empresa": "ITA6"},
                {"cnpj": "20533473000242", "ons": "3532", "codigo": "1101740", "empresa": "ITA7"},
                {"cnpj": "20533310000260", "ons": "3537", "codigo": "1101754", "empresa": "ITA8"},
                {"cnpj": "20533377000202", "ons": "3538", "codigo": "1101755", "empresa": "ITA9"},
                {"cnpj": "30063842000234", "ons": "3947", "codigo": "1105036", "empresa": "SDBA"},
                {"cnpj": "29527877000206", "ons": "3948", "codigo": "1105037", "empresa": "SDBB"},
                {"cnpj": "29591504000296", "ons": "3969", "codigo": "1105267", "empresa": "SDBC"},
                {"cnpj": "30062725000256", "ons": "3970", "codigo": "1105268", "empresa": "SDBD"},
                {"cnpj": "30062736000236", "ons": "3976", "codigo": "1105116", "empresa": "SDBE"},
                {"cnpj": "30234798000288", "ons": "3972", "codigo": "1105270", "empresa": "SDBF"}
            ],
            "AE": [  # AE
                {"cnpj": "30520122000170", "ons": "3859", "codigo": "", "empresa": "SJP1"},
                {"cnpj": "30432072000179", "ons": "3860", "codigo": "", "empresa": "SJP2"},
                {"cnpj": "30486042000145", "ons": "3861", "codigo": "", "empresa": "SJP3"},
                {"cnpj": "30425445000184", "ons": "3862", "codigo": "", "empresa": "SJP4"},
                {"cnpj": "30456405000108", "ons": "3863", "codigo": "", "empresa": "SJP5"},
                {"cnpj": "30421756000175", "ons": "3864", "codigo": "", "empresa": "SJP6"},
                {"cnpj": "14285232000148", "ons": "3740", "codigo": "", "empresa": "COR1"},
                {"cnpj": "14285242000183", "ons": "3741", "codigo": "", "empresa": "COR2"},
                {"cnpj": "24342513000149", "ons": "3750", "codigo": "", "empresa": "COR3"},
                {"cnpj": "10500221000182", "ons": "8011", "codigo": "", "empresa": "LIBRA"}
            ]
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
            
            # Criar estrutura de diretórios: EMPRESA/SPE/SUBEMPRESA
            diretorio_empresa = os.path.join(diretorio_base, fatura_info['grupo'])  # DE ou RE
            diretorio_spe = os.path.join(diretorio_empresa, fatura_info['spe'])  # SP01, SP02, etc
            diretorio_saida = os.path.join(diretorio_spe, fatura_info['empresa'])  # BRJA, CECA, etc
            
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
    
    def processar_empresa(self, grupo_empresa, empresa_info, mes, ano):
        """
        Processa uma empresa específica
        """
        for sp_num in range(1, 9):
            spe = f"sp0{sp_num}"
            print(f"\nProcessando {grupo_empresa}/{spe}/{empresa_info['empresa']}...")
            
            # Nova sessão para cada tentativa
            self.session = requests.Session()
            
            if self.login(empresa_info['cnpj'], empresa_info['ons'], spe):
                faturas = self.buscar_faturas_por_data(mes, ano)
                
                if faturas:
                    for fatura in faturas:
                        # Adiciona informações adicionais à fatura
                        fatura['grupo'] = grupo_empresa  # DE ou RE
                        fatura['spe'] = spe.upper()  # SP01
                        fatura['empresa'] = empresa_info['empresa']  # BRJA, CECA, etc
                        
                        self.baixar_fatura(fatura, tipo='xml')
                        self.baixar_fatura(fatura, tipo='pdf')
                else:
                    print(f"Nenhuma fatura encontrada para {grupo_empresa}/{spe}/{empresa_info['empresa']}")

    def processar_todas_empresas(self, mes, ano):
        """
        Processa todas as empresas de todos os grupos
        """
        for grupo, empresas in self.empresas.items():
            print(f"\nProcessando grupo: {grupo}")
            for empresa_info in empresas:
                self.processar_empresa(grupo, empresa_info, mes, ano)

# Exemplo de uso
if __name__ == "__main__":
    client = EquatorialClient()
    client.processar_todas_empresas(11, 2024)
