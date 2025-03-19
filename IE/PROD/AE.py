import os
import requests
from bs4 import BeautifulSoup
import zipfile
import tempfile
import shutil

class TransmissoraDownloader:
    def __init__(self, base_dir="C:\\Users\\Bruno\\Downloads\\TUST\\IE\\AE"):
        self.base_dir = base_dir
        self.sites = {
            "EVRECY": "https://faturamento.evrecy.com.br",
            # "IESUL": "https://faturamento.iesul.com.br",
            # "IENNE": "https://faturamento.ienne.com.br",
            # "IEMG": "https://faturamento.iemg.com.br",
            # "IEMADEIRA": "https://faturamento.iemadeira.com.br",
            # "IEJAGUAR9": "https://faturamento.iejaguar9.com.br",
            # "IEAGUAPEI":"https://faturamento.ieaguapei.com.br",
            # "IEBIGUACU":"https://faturamento.iebiguacu.com.br",
            # "IEITAPURA":"https://faturamento.ieitapura.com.br",
            # "IEITAQUERE":"https://faturamento.ieitaquere.com.br",
            # "IEITAUNAS":"https://faturamento.ieitaunas.com.br",
            # "IEJAGUAR8":"https://faturamento.iejaguar8.com.br",
            # "IETIBAGI":"https://faturamento.ietibagi.com.br",
            # "IEGARANHUNS":"http://faturamento.iegaranhuns.com.br",
            # "IESERRADOJAPI":"https://faturamento.ieserradojapi.com.br",
            # "CTEEP_PBTE":"https://faturamento.isaenergiabrasil.com.br"
        }
        
        # Lista de credenciais e suas respectivas empresas
        self.credenciais = [
            {
                "usuario": "kleber@libraligas.com.br",
                "senha": "542D1G6",
                "pasta_base": "LIBRAS",
                "empresa": "AE"
            },
            {
                "usuario": "fatura.coremas@americaenergia.com.br",
                "senha": "2M4TO12",
                "pasta_base": ["COREMAS I", "COREMAS II", "COREMAS III"],
                "empresa": "AE"
            },
            {
                "usuario": "faturas.sjp@americaenergia.com.br",
                "senha": "QM17DIB10",
                "pasta_base": ["SJP1", "SJP2","SPJ3", "SJP4", "SJP5", "SJP6"],
                "empresa": "AE"
            },
            # {
            #     "usuario": "fatbol_dressler@vbasystems.com.br",
            #     "senha": "27093977",
            #     "pasta_base": "DRESSLER",
            #     "empresa": "DE"
            # },
            # {
            #     "usuario": "tust@rioenergyllc.com",
            #     "senha": "1XAVYIU04",
            #     "pasta_base": ["ITA9", "ITA5", "ITA6", "ITA7", "ITA8"],
            #     "empresa": "RE"
            # },
            # {
            #     "usuario": "tust@rioenergy.com.br",
            #     "senha": "tustre3430",
            #     "pasta_base": ["BRJA", "CECA", "CECB", "CECC", "CECD", "ITA1", "ITA2", "ITA3", "ITA4", "SDBB", "SDBE", "SDBF"],
            #     "empresa": "RE"
            # },
            # {
            #     "usuario": "rodrigo.abrantes@rioenergy.com.br",
            #     "senha": "625L5Q0",
            #     "pasta_base": ["BRJB", "CECE", "CECF", "SDBA", "SDBC", "SDBD"],
            #     "empresa": "RE"
            # }
        ]
    
    def adicionar_site(self, nome, url):
        """Adiciona um novo site à lista de sites para processamento"""
        self.sites[nome] = url
        print(f"Site {nome} adicionado com sucesso: {url}")
    
    def login(self, site_nome, usuario, senha):
        """Faz login em um site específico"""
        site_url = self.sites.get(site_nome)
        if not site_url:
            print(f"Site {site_nome} não encontrado na lista de sites.")
            return None
            
        # URL do site
        url = f"{site_url}/login.asp"
        
        # Dados do formulário
        dados_login = {
            'usuario': usuario,
            'senha': senha
        }
        
        # Headers para simular um navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        try:
            # Fazendo a requisição POST
            sessao = requests.Session()
            resposta = sessao.post(url, data=dados_login, headers=headers)
            
            # Verificando se o login foi bem sucedido
            if resposta.status_code == 200:
                print(f"Login {site_nome} realizado com sucesso!")
                return sessao
            else:
                print(f"Erro no login {site_nome}. Código de status: {resposta.status_code}")
                return None
                
        except Exception as e:
            print(f"Ocorreu um erro no {site_nome}: {str(e)}")
            return None
    
    def pesquisar_faturas(self, site_nome, sessao, periodo="2025|02"):
        """Pesquisa faturas em um site específico"""
        site_url = self.sites.get(site_nome)
        if not site_url:
            print(f"Site {site_nome} não encontrado na lista de sites.")
            return None
            
        # URL da página de rede básica
        url_rb = f"{site_url}/RB.asp"
        
        # Headers para simular um navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        try:
            # Primeiro acesso à página para obter o período mais recente
            resposta = sessao.get(url_rb, headers=headers)
            
            # Dados para o formulário de pesquisa
            dados_pesquisa = {
                'data': periodo
            }
            
            # Fazendo a requisição POST para pesquisar
            resposta_pesquisa = sessao.post(url_rb, data=dados_pesquisa, headers=headers)
            
            if resposta_pesquisa.status_code == 200:
                print(f"Pesquisa {site_nome} realizada com sucesso!")
                return resposta_pesquisa.text
            else:
                print(f"Erro na pesquisa {site_nome}. Código de status: {resposta_pesquisa.status_code}")
                return None
                
        except Exception as e:
            print(f"Ocorreu um erro na pesquisa {site_nome}: {str(e)}")
            return None
    
    def extrair_e_mostrar_transmissoras(self, site_nome, html, empresa):
        """Extrai e mostra as transmissoras encontradas"""
        soup = BeautifulSoup(html, 'html.parser')
        print(f"\n=== Transmissoras Encontradas {site_nome} ===")
        print("Período: Fevereiro/2025")
        
        # Encontrar todas as fieldsets (cada uma representa uma transmissora)
        transmissoras = soup.find_all('fieldset')
        
        total_geral = 0
        faturas_encontradas = False
        
        for transmissora in transmissoras:
            # Pegar o nome da transmissora da legend
            legend = transmissora.find('legend')
            if legend:
                nome_transmissora = legend.text.strip()
                print(f"\n{nome_transmissora}")
                print("-" * 50)
                
                # Encontrar todas as linhas da tabela dentro desta fieldset
                tabela = transmissora.find('table')
                if tabela:
                    linhas = tabela.find_all('tr')[1:-1]  # Pula o cabeçalho e a linha de total
                    
                    total_transmissora = 0
                    for linha in linhas:
                        colunas = linha.find_all('td')
                        if len(colunas) >= 4:  # Verifica se é uma linha válida
                            empreendimento = colunas[0].text.strip()
                            codigo_ons = colunas[1].text.strip()
                            fatura = colunas[2].text.strip()
                            valor = colunas[3].text.strip()
                            
                            if empreendimento and codigo_ons and "Total" not in empreendimento:
                                faturas_encontradas = True  # Marca que encontrou pelo menos uma fatura
                                print(f"\nEmpreendimento: {empreendimento}")
                                print(f"Código ONS: {codigo_ons}")
                                print(f"Número da Fatura: {fatura}")
                                print(f"Valor: R$ {valor}")
                                try:
                                    valor_float = float(valor.replace(',', '.'))
                                    total_transmissora += valor_float
                                except:
                                    pass
                    
                    # Tentar obter o total da linha de total
                    try:
                        linha_total = tabela.find_all('tr')[-1]
                        valor_total_text = linha_total.find_all('td')[3].text.strip()
                        valor_total = float(valor_total_text.replace(',', '.'))
                        print(f"\nTotal {nome_transmissora}: R$ {valor_total:.2f}")
                        total_geral += valor_total
                    except Exception as e:
                        print(f"\nTotal {nome_transmissora}: R$ {total_transmissora:.2f}")
                        total_geral += total_transmissora
        
        print("\n" + "=" * 50)
        print(f"Valor Total Geral: R$ {total_geral:.2f}")
        print("=" * 50)
        
        return faturas_encontradas  # Retorna True se encontrou faturas
    
    def download_documentos(self, site_nome, sessao, html, base_path):
        """Baixa os documentos de um site específico"""
        site_url = self.sites.get(site_nome)
        if not site_url:
            print(f"Site {site_nome} não encontrado na lista de sites.")
            return
            
        # Criar estrutura de pastas
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        soup = BeautifulSoup(html, 'html.parser')
        
        # Encontrar todas as fieldsets (cada uma representa uma transmissora)
        transmissoras = soup.find_all('fieldset')
        
        for transmissora in transmissoras:
            # Pegar o nome da transmissora da legend
            nome_transmissora = transmissora.find('legend').text.strip()
            
            # Criar pasta para a transmissora específica
            pasta_transmissora = os.path.join(base_path, nome_transmissora.replace(" ", "_"))
            if not os.path.exists(pasta_transmissora):
                os.makedirs(pasta_transmissora)
                
            # Encontrar todas as linhas da tabela dentro desta fieldset
            linhas = transmissora.find_all('tr')[1:]  # Pula o cabeçalho

            for linha in linhas:
                colunas = linha.find_all('td')
                if len(colunas) >= 5:  # Verifica se é uma linha válida com links
                    empreendimento = colunas[0].text.strip()
                    num_fatura = colunas[2].text.strip()
                    
                    # Pula o cabeçalho da tabela e a linha de total
                    if not empreendimento or "Total" in empreendimento or "Empreendimento/Contrato" in empreendimento:
                        continue

                    # Criar pasta temporária para trabalhar com os arquivos
                    with tempfile.TemporaryDirectory() as temp_dir:
                        base_url = f"{site_url}/download.asp"
                        
                        # Download da fatura (XML)
                        url_fatura = f"{base_url}?mode=admin&arquivo=zip&tipo=xml&num_fatura={num_fatura}"
                        temp_fatura = os.path.join(temp_dir, f"fatura_{num_fatura}")  # Sem extensão por enquanto
                        
                        try:
                            # Baixar fatura
                            response = sessao.get(url_fatura)
                            if response.status_code == 200:
                                # Salvar o arquivo sem extensão primeiro
                                with open(temp_fatura, 'wb') as f:
                                    f.write(response.content)
                                print(f"Fatura {site_nome} {num_fatura} baixada com sucesso!")
                                
                                # Verificar o tipo de arquivo
                                content_type = response.headers.get('Content-Type', '')
                                
                                # Determinar a extensão baseada no conteúdo
                                if 'zip' in content_type.lower():
                                    extensao = '.zip'
                                elif 'xml' in content_type.lower():
                                    extensao = '.xml'
                                elif 'pdf' in content_type.lower():
                                    extensao = '.pdf'
                                else:
                                    # Tentar detectar o tipo de arquivo pelo conteúdo
                                    if response.content.startswith(b'PK'):
                                        extensao = '.zip'
                                    elif response.content.startswith(b'%PDF'):
                                        extensao = '.pdf'
                                    elif response.content.startswith(b'<?xml'):
                                        extensao = '.xml'
                                    else:
                                        extensao = '.dat'  # Extensão genérica
                                
                                # Renomear o arquivo com a extensão correta
                                arquivo_final = os.path.join(pasta_transmissora, f"fatura_{num_fatura}{extensao}")
                                shutil.copy2(temp_fatura, arquivo_final)
                                
                                # Descompactar arquivo se for ZIP
                                if extensao == '.zip':
                                    pasta_descompactada = os.path.join(pasta_transmissora, f"fatura_{num_fatura}_extraido")
                                    if not os.path.exists(pasta_descompactada):
                                        os.makedirs(pasta_descompactada)
                                    
                                    try:
                                        with zipfile.ZipFile(arquivo_final, 'r') as zip_ref:
                                            zip_ref.extractall(pasta_descompactada)
                                        print(f"Arquivo ZIP {num_fatura} descompactado com sucesso em {pasta_descompactada}")
                                        
                                        # Excluir o arquivo ZIP após descompactar com sucesso
                                        os.remove(arquivo_final)
                                        print(f"Arquivo ZIP {num_fatura} excluído após descompactação")
                                    except Exception as e:
                                        print(f"Erro ao descompactar o arquivo ZIP {num_fatura}: {str(e)}")
                                
                                # Tentar baixar o boleto também
                                url_boleto = f"{base_url}?mode=admin&tipo=boleto&arquivo=zip&num_fatura={num_fatura}"
                                temp_boleto = os.path.join(temp_dir, f"boleto_{num_fatura}")
                                
                                response_boleto = sessao.get(url_boleto)
                                if response_boleto.status_code == 200 and len(response_boleto.content) > 0:
                                    # Salvar o boleto
                                    with open(temp_boleto, 'wb') as f:
                                        f.write(response_boleto.content)
                                    
                                    # Determinar a extensão do boleto
                                    if response_boleto.content.startswith(b'%PDF'):
                                        boleto_ext = '.pdf'
                                    elif response_boleto.content.startswith(b'PK'):
                                        boleto_ext = '.zip'
                                    else:
                                        boleto_ext = '.dat'
                                    
                                    # Salvar o boleto separadamente
                                    boleto_final = os.path.join(pasta_transmissora, f"boleto_{num_fatura}{boleto_ext}")
                                    shutil.copy2(temp_boleto, boleto_final)
                                    print(f"Boleto {site_nome} {num_fatura} salvo com sucesso!")
                                    
                                    # Descompactar boleto se for ZIP
                                    if boleto_ext == '.zip':
                                        pasta_boleto_descompactado = os.path.join(pasta_transmissora, f"boleto_{num_fatura}_extraido")
                                        if not os.path.exists(pasta_boleto_descompactado):
                                            os.makedirs(pasta_boleto_descompactado)
                                        
                                        try:
                                            with zipfile.ZipFile(boleto_final, 'r') as zip_ref:
                                                zip_ref.extractall(pasta_boleto_descompactado)
                                            print(f"Boleto ZIP {num_fatura} descompactado com sucesso em {pasta_boleto_descompactado}")
                                            
                                            # Excluir o arquivo ZIP do boleto após descompactar com sucesso
                                            os.remove(boleto_final)
                                            print(f"Boleto ZIP {num_fatura} excluído após descompactação")
                                        except Exception as e:
                                            print(f"Erro ao descompactar o boleto ZIP {num_fatura}: {str(e)}")
                                
                        except Exception as e:
                            print(f"Erro ao processar documentos {site_nome} da fatura {num_fatura}: {str(e)}")
    
    def processar_site(self, site_nome):
        """Processa um site específico para todas as credenciais"""
        print(f"\n=== PROCESSANDO {site_nome} ===")
        
        for credencial in self.credenciais:
            empresa_pasta = credencial["empresa"]  # AE ou DE
            
            if isinstance(credencial["pasta_base"], str):  # Se for LIBRAS ou DRESSLER
                print(f"\nProcessando empresa {site_nome}: {credencial['pasta_base']}")
                print("-" * 50)
                
                # Fazer login
                sessao = self.login(site_nome, credencial["usuario"], credencial["senha"])
                
                if sessao:
                    resultado = self.pesquisar_faturas(site_nome, sessao)
                    if resultado:
                        tem_faturas = self.extrair_e_mostrar_transmissoras(site_nome, resultado, credencial["pasta_base"])
                        if tem_faturas:
                            print(f"\nIniciando downloads dos documentos {site_nome}...")
                            
                            base_path = os.path.join(self.base_dir, site_nome, empresa_pasta, credencial["pasta_base"])
                            self.download_documentos(site_nome, sessao, resultado, base_path)
                            
                            print(f"\nProcesso {site_nome} finalizado para {credencial['pasta_base']}!")
                        else:
                            print(f"\nNenhuma fatura encontrada no {site_nome} para {credencial['pasta_base']}!")
            
            else:  # Se for COREMAS ou SJP
                # Fazer login uma única vez
                sessao = self.login(site_nome, credencial["usuario"], credencial["senha"])
                
                if sessao:
                    resultado = self.pesquisar_faturas(site_nome, sessao)
                    if resultado:
                        # Para cada transmissora
                        soup = BeautifulSoup(resultado, 'html.parser')
                        transmissoras = soup.find_all('fieldset')
                        
                        for i, transmissora in enumerate(transmissoras):
                            if i >= len(credencial["pasta_base"]):
                                print(f"Aviso: Mais transmissoras encontradas do que pastas base definidas para {credencial['usuario']}")
                                break
                                
                            nome_transmissora = transmissora.find('legend').text.strip()
                            pasta_base = credencial["pasta_base"][i]  # COREMAS I,II,III ou SJP1,2,5,6
                            
                            print(f"\nProcessando {site_nome}: {pasta_base}")
                            print("-" * 50)
                            
                            # Criar HTML específico para esta transmissora
                            novo_html = f"""
                            <fieldset>
                                <legend>{nome_transmissora}</legend>
                                {transmissora.find('table').prettify()}
                            </fieldset>
                            """
                            
                            self.extrair_e_mostrar_transmissoras(site_nome, novo_html, pasta_base)
                            print(f"\nIniciando downloads dos documentos {site_nome}...")
                            
                            base_path = os.path.join(self.base_dir, site_nome, empresa_pasta, pasta_base)
                            self.download_documentos(site_nome, sessao, novo_html, base_path)
                            
                            print(f"\nProcesso {site_nome} finalizado para {pasta_base}!")
    
    def processar_todos_sites(self):
        """Processa todos os sites configurados"""
        for site_nome in self.sites:
            self.processar_site(site_nome)

def main():
    # Criar instância do downloader
    downloader = TransmissoraDownloader()
    
    # Processar todos os sites
    downloader.processar_todos_sites()
    
    # Ou processar sites específicos
    # downloader.processar_site("EVRECY")
    # downloader.processar_site("IESUL")
    
    # Para adicionar um novo site
    # downloader.adicionar_site("NOVO_SITE", "https://faturamento.novo-site.com.br")
    # downloader.processar_site("NOVO_SITE")

if __name__ == "__main__":
    main()