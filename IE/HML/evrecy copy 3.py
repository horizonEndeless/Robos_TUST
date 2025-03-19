import os
import requests
from bs4 import BeautifulSoup
import zipfile
import tempfile
import shutil

def login_evrecy(usuario, senha):
    # URL do site
    url = "https://faturamento.evrecy.com.br/login.asp"
    # url = "https://faturamento.iemg.com.br/login.asp"
    
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
            print("Login realizado com sucesso!")
            return sessao
        else:
            print(f"Erro no login. Código de status: {resposta.status_code}")
            return None
            
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")
        return None

def login_iesul(usuario, senha):
    # URL do site
    url = "https://faturamento.iesul.com.br/login.asp"
    
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
            print("Login IESUL realizado com sucesso!")
            return sessao
        else:
            print(f"Erro no login IESUL. Código de status: {resposta.status_code}")
            return None
            
    except Exception as e:
        print(f"Ocorreu um erro no IESUL: {str(e)}")
        return None

def pesquisar_faturas(sessao):
    # URL da página de rede básica
    url_rb = "https://faturamento.evrecy.com.br/RB.asp"
    
    # Headers para simular um navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Primeiro acesso à página para obter o período mais recente
        resposta = sessao.get(url_rb, headers=headers)
        
        # Dados para o formulário de pesquisa
        # O valor "2024|11" representa Novembro/2024 (período mais recente)
        dados_pesquisa = {
            'data': '2025|02'
        }
        
        # Fazendo a requisição POST para pesquisar
        resposta_pesquisa = sessao.post(url_rb, data=dados_pesquisa, headers=headers)
        
        if resposta_pesquisa.status_code == 200:
            print("Pesquisa realizada com sucesso!")
            return resposta_pesquisa.text
        else:
            print(f"Erro na pesquisa. Código de status: {resposta_pesquisa.status_code}")
            return None
            
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")
        return None

def pesquisar_faturas_iesul(sessao):
    # URL da página de rede básica
    url_rb = "https://faturamento.iesul.com.br/RB.asp"
    
    # Headers para simular um navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Primeiro acesso à página para obter o período mais recente
        resposta = sessao.get(url_rb, headers=headers)
        
        # Dados para o formulário de pesquisa
        # O valor "2024|11" representa Novembro/2024 (período mais recente)
        dados_pesquisa = {
            'data': '2025|02'
        }
        
        # Fazendo a requisição POST para pesquisar
        resposta_pesquisa = sessao.post(url_rb, data=dados_pesquisa, headers=headers)
        
        if resposta_pesquisa.status_code == 200:
            print("Pesquisa IESUL realizada com sucesso!")
            return resposta_pesquisa.text
        else:
            print(f"Erro na pesquisa IESUL. Código de status: {resposta_pesquisa.status_code}")
            return None
            
    except Exception as e:
        print(f"Ocorreu um erro na pesquisa IESUL: {str(e)}")
        return None

def extrair_e_mostrar_transmissoras(html, empresa):
    soup = BeautifulSoup(html, 'html.parser')
    print("\n=== Transmissoras Encontradas ===")
    print("Período: Novembro/2024")
    
    # Encontrar todas as fieldsets (cada uma representa uma transmissora)
    transmissoras = soup.find_all('fieldset')
    
    total_geral = 0
    for transmissora in transmissoras:
        # Pegar o nome da transmissora da legend
        nome_transmissora = transmissora.find('legend').text.strip()
        print(f"\n{nome_transmissora}")
        print("-" * 50)
        
        # Encontrar todas as linhas da tabela dentro desta fieldset
        linhas = transmissora.find_all('tr')[1:]  # Pula o cabeçalho
        
        total_transmissora = 0
        for linha in linhas:
            colunas = linha.find_all('td')
            if len(colunas) >= 4:  # Verifica se é uma linha válida
                empreendimento = colunas[0].text.strip()
                codigo_ons = colunas[1].text.strip()
                fatura = colunas[2].text.strip()
                valor = colunas[3].text.strip()
                
                if empreendimento and codigo_ons and "Total" not in empreendimento:
                    print(f"\nEmpreendimento: {empreendimento}")
                    print(f"Código ONS: {codigo_ons}")
                    print(f"Número da Fatura: {fatura}")
                    print(f"Valor: R$ {valor}")
                    try:
                        total_transmissora += float(valor.replace(',', '.'))
                    except:
                        pass
        
        print(f"\nTotal {nome_transmissora}: R$ {total_transmissora:.2f}")
        total_geral += total_transmissora
    
    print("\n" + "=" * 50)
    print(f"Valor Total Geral: R$ {total_geral:.2f}")
    print("=" * 50)

def download_documentos(sessao, html, base_path):
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
            if len(colunas) >= 6:  # Verifica se é uma linha válida com links
                empreendimento = colunas[0].text.strip()
                num_fatura = colunas[2].text.strip()
                
                # Pula o cabeçalho da tabela e a linha de total
                if not empreendimento or "Total" in empreendimento or "Empreendimento/Contrato" in empreendimento:
                    continue

                # Criar pasta temporária para trabalhar com os arquivos
                with tempfile.TemporaryDirectory() as temp_dir:
                    base_url = "https://faturamento.evrecy.com.br/download.asp"
                    
                    # Download da fatura (XML)
                    url_fatura = f"{base_url}?mode=admin&arquivo=zip&tipo=xml&num_fatura={num_fatura}"
                    temp_fatura = os.path.join(temp_dir, f"fatura_{num_fatura}.zip")
                    
                    try:
                        # Baixar fatura
                        response = sessao.get(url_fatura)
                        if response.status_code == 200:
                            with open(temp_fatura, 'wb') as f:
                                f.write(response.content)
                            print(f"Fatura {num_fatura} baixada com sucesso!")

                            # Baixar boleto
                            url_boleto = f"{base_url}?mode=admin&tipo=boleto&arquivo=zip&num_fatura={num_fatura}"
                            temp_boleto = os.path.join(temp_dir, f"boleto_{num_fatura}.zip")
                            
                            response_boleto = sessao.get(url_boleto)
                            if response_boleto.status_code == 200 and len(response_boleto.content) > 0:
                                # Extrair o PDF do ZIP do boleto
                                with open(temp_boleto, 'wb') as f:
                                    f.write(response_boleto.content)
                                
                                # Criar novo arquivo ZIP com fatura e boleto
                                arquivo_final = os.path.join(pasta_transmissora, f"fatura_{num_fatura}.zip")
                                
                                # Copiar conteúdo da fatura para o arquivo final
                                shutil.copy2(temp_fatura, arquivo_final)
                                
                                # Adicionar boleto ao ZIP da fatura
                                with zipfile.ZipFile(temp_boleto, 'r') as zip_boleto:
                                    with zipfile.ZipFile(arquivo_final, 'a') as zip_final:
                                        for arquivo in zip_boleto.namelist():
                                            if arquivo.endswith('.pdf'):
                                                zip_final.writestr(f"boleto_{num_fatura}.pdf", 
                                                                 zip_boleto.read(arquivo))
                                
                                print(f"Documentos da fatura {num_fatura} combinados com sucesso!")
                            else:
                                # Se não houver boleto, apenas copia a fatura
                                arquivo_final = os.path.join(pasta_transmissora, f"fatura_{num_fatura}.zip")
                                shutil.copy2(temp_fatura, arquivo_final)
                                
                    except Exception as e:
                        print(f"Erro ao processar documentos da fatura {num_fatura}: {str(e)}")

def download_documentos_iesul(sessao, html, base_path):
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
                    base_url = "https://faturamento.iesul.com.br/download.asp"
                    
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
                            print(f"Fatura IESUL {num_fatura} baixada com sucesso!")
                            
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
                                else:
                                    boleto_ext = '.dat'
                                
                                # Salvar o boleto separadamente
                                boleto_final = os.path.join(pasta_transmissora, f"boleto_{num_fatura}{boleto_ext}")
                                shutil.copy2(temp_boleto, boleto_final)
                                print(f"Boleto IESUL {num_fatura} salvo com sucesso!")
                            
                    except Exception as e:
                        print(f"Erro ao processar documentos IESUL da fatura {num_fatura}: {str(e)}")

def extrair_e_mostrar_transmissoras_iesul(html, empresa):
    soup = BeautifulSoup(html, 'html.parser')
    print("\n=== Transmissoras Encontradas IESUL ===")
    print("Período: Fevereiro/2025")
    
    # Encontrar todas as fieldsets (cada uma representa uma transmissora)
    transmissoras = soup.find_all('fieldset')
    
    total_geral = 0
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
                        
                        if empreendimento and codigo_ons:
                            print(f"\nEmpreendimento: {empreendimento}")
                            print(f"Código ONS: {codigo_ons}")
                            print(f"Número da Fatura: {fatura}")
                            print(f"Valor: R$ {valor}")
                            try:
                                total_transmissora += float(valor.replace(',', '.'))
                            except:
                                pass
                
                # Tentar obter o total da linha de total
                try:
                    linha_total = tabela.find_all('tr')[-1]
                    valor_total = linha_total.find_all('td')[3].text.strip()
                    total_transmissora = float(valor_total.replace(',', '.'))
                    print(f"\nTotal {nome_transmissora}: R$ {total_transmissora:.2f}")
                except:
                    print(f"\nTotal {nome_transmissora}: R$ {total_transmissora:.2f}")
                
                total_geral += total_transmissora
    
    print("\n" + "=" * 50)
    print(f"Valor Total Geral: R$ {total_geral:.2f}")
    print("=" * 50)
    
    return total_geral > 0  # Retorna True se encontrou faturas

def login_ienne(usuario, senha):
    # URL do site
    url = "https://faturamento.ienne.com.br/login.asp"
    
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
            print("Login IENNE realizado com sucesso!")
            return sessao
        else:
            print(f"Erro no login IENNE. Código de status: {resposta.status_code}")
            return None
            
    except Exception as e:
        print(f"Ocorreu um erro no IENNE: {str(e)}")
        return None

def pesquisar_faturas_ienne(sessao):
    # URL da página de rede básica
    url_rb = "https://faturamento.ienne.com.br/RB.asp"
    
    # Headers para simular um navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Primeiro acesso à página para obter o período mais recente
        resposta = sessao.get(url_rb, headers=headers)
        
        # Dados para o formulário de pesquisa
        dados_pesquisa = {
            'data': '2025|02'
        }
        
        # Fazendo a requisição POST para pesquisar
        resposta_pesquisa = sessao.post(url_rb, data=dados_pesquisa, headers=headers)
        
        if resposta_pesquisa.status_code == 200:
            print("Pesquisa IENNE realizada com sucesso!")
            return resposta_pesquisa.text
        else:
            print(f"Erro na pesquisa IENNE. Código de status: {resposta_pesquisa.status_code}")
            return None
            
    except Exception as e:
        print(f"Ocorreu um erro na pesquisa IENNE: {str(e)}")
        return None

def extrair_e_mostrar_transmissoras_ienne(html, empresa):
    soup = BeautifulSoup(html, 'html.parser')
    print("\n=== Transmissoras Encontradas IENNE ===")
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
                        
                        if empreendimento and codigo_ons:
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

def download_documentos_ienne(sessao, html, base_path):
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
                    base_url = "https://faturamento.ienne.com.br/download.asp"
                    
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
                            print(f"Fatura IENNE {num_fatura} baixada com sucesso!")
                            
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
                                else:
                                    boleto_ext = '.dat'
                                
                                # Salvar o boleto separadamente
                                boleto_final = os.path.join(pasta_transmissora, f"boleto_{num_fatura}{boleto_ext}")
                                shutil.copy2(temp_boleto, boleto_final)
                                print(f"Boleto IENNE {num_fatura} salvo com sucesso!")
                            
                    except Exception as e:
                        print(f"Erro ao processar documentos IENNE da fatura {num_fatura}: {str(e)}")

def login_iemg(usuario, senha):
    # URL do site
    url = "https://faturamento.iemg.com.br/login.asp"
    
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
            print("Login IEMG realizado com sucesso!")
            return sessao
        else:
            print(f"Erro no login IEMG. Código de status: {resposta.status_code}")
            return None
            
    except Exception as e:
        print(f"Ocorreu um erro no IEMG: {str(e)}")
        return None

def pesquisar_faturas_iemg(sessao):
    # URL da página de rede básica
    url_rb = "https://faturamento.iemg.com.br/RB.asp"
    
    # Headers para simular um navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Primeiro acesso à página para obter o período mais recente
        resposta = sessao.get(url_rb, headers=headers)
        
        # Dados para o formulário de pesquisa
        dados_pesquisa = {
            'data': '2025|02'
        }
        
        # Fazendo a requisição POST para pesquisar
        resposta_pesquisa = sessao.post(url_rb, data=dados_pesquisa, headers=headers)
        
        if resposta_pesquisa.status_code == 200:
            print("Pesquisa IEMG realizada com sucesso!")
            return resposta_pesquisa.text
        else:
            print(f"Erro na pesquisa IEMG. Código de status: {resposta_pesquisa.status_code}")
            return None
            
    except Exception as e:
        print(f"Ocorreu um erro na pesquisa IEMG: {str(e)}")
        return None

def extrair_e_mostrar_transmissoras_iemg(html, empresa):
    soup = BeautifulSoup(html, 'html.parser')
    print("\n=== Transmissoras Encontradas IEMG ===")
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
                        
                        if empreendimento and codigo_ons:
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

def download_documentos_iemg(sessao, html, base_path):
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
                    base_url = "https://faturamento.iemg.com.br/download.asp"
                    
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
                            print(f"Fatura IEMG {num_fatura} baixada com sucesso!")
                            
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
                                else:
                                    boleto_ext = '.dat'
                                
                                # Salvar o boleto separadamente
                                boleto_final = os.path.join(pasta_transmissora, f"boleto_{num_fatura}{boleto_ext}")
                                shutil.copy2(temp_boleto, boleto_final)
                                print(f"Boleto IEMG {num_fatura} salvo com sucesso!")
                            
                    except Exception as e:
                        print(f"Erro ao processar documentos IEMG da fatura {num_fatura}: {str(e)}")

def login_iemadeira(usuario, senha):
    # URL do site
    url = "https://faturamento.iemadeira.com.br/login.asp"
    
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
            print("Login IEMADEIRA realizado com sucesso!")
            return sessao
        else:
            print(f"Erro no login IEMADEIRA. Código de status: {resposta.status_code}")
            return None
            
    except Exception as e:
        print(f"Ocorreu um erro no IEMADEIRA: {str(e)}")
        return None

def pesquisar_faturas_iemadeira(sessao):
    # URL da página de rede básica
    url_rb = "https://faturamento.iemadeira.com.br/RB.asp"
    
    # Headers para simular um navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Primeiro acesso à página para obter o período mais recente
        resposta = sessao.get(url_rb, headers=headers)
        
        # Dados para o formulário de pesquisa
        dados_pesquisa = {
            'data': '2025|02'
        }
        
        # Fazendo a requisição POST para pesquisar
        resposta_pesquisa = sessao.post(url_rb, data=dados_pesquisa, headers=headers)
        
        if resposta_pesquisa.status_code == 200:
            print("Pesquisa IEMADEIRA realizada com sucesso!")
            return resposta_pesquisa.text
        else:
            print(f"Erro na pesquisa IEMADEIRA. Código de status: {resposta_pesquisa.status_code}")
            return None
            
    except Exception as e:
        print(f"Ocorreu um erro na pesquisa IEMADEIRA: {str(e)}")
        return None

def extrair_e_mostrar_transmissoras_iemadeira(html, empresa):
    soup = BeautifulSoup(html, 'html.parser')
    print("\n=== Transmissoras Encontradas IEMADEIRA ===")
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
                        
                        if empreendimento and codigo_ons:
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

def download_documentos_iemadeira(sessao, html, base_path):
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
                    base_url = "https://faturamento.iemadeira.com.br/download.asp"
                    
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
                            print(f"Fatura IEMADEIRA {num_fatura} baixada com sucesso!")
                            
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
                                else:
                                    boleto_ext = '.dat'
                                
                                # Salvar o boleto separadamente
                                boleto_final = os.path.join(pasta_transmissora, f"boleto_{num_fatura}{boleto_ext}")
                                shutil.copy2(temp_boleto, boleto_final)
                                print(f"Boleto IEMADEIRA {num_fatura} salvo com sucesso!")
                            
                    except Exception as e:
                        print(f"Erro ao processar documentos IEMADEIRA da fatura {num_fatura}: {str(e)}")

def login_iejaguar9(usuario, senha):
    # URL do site
    url = "https://faturamento.iejaguar9.com.br/login.asp"
    
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
            print("Login IEJAGUAR9 realizado com sucesso!")
            return sessao
        else:
            print(f"Erro no login IEJAGUAR9. Código de status: {resposta.status_code}")
            return None
            
    except Exception as e:
        print(f"Ocorreu um erro no IEJAGUAR9: {str(e)}")
        return None

def pesquisar_faturas_iejaguar9(sessao):
    # URL da página de rede básica
    url_rb = "https://faturamento.iejaguar9.com.br/RB.asp"
    
    # Headers para simular um navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Primeiro acesso à página para obter o período mais recente
        resposta = sessao.get(url_rb, headers=headers)
        
        # Dados para o formulário de pesquisa
        dados_pesquisa = {
            'data': '2025|02'
        }
        
        # Fazendo a requisição POST para pesquisar
        resposta_pesquisa = sessao.post(url_rb, data=dados_pesquisa, headers=headers)
        
        if resposta_pesquisa.status_code == 200:
            print("Pesquisa IEJAGUAR9 realizada com sucesso!")
            return resposta_pesquisa.text
        else:
            print(f"Erro na pesquisa IEJAGUAR9. Código de status: {resposta_pesquisa.status_code}")
            return None
            
    except Exception as e:
        print(f"Ocorreu um erro na pesquisa IEJAGUAR9: {str(e)}")
        return None

def extrair_e_mostrar_transmissoras_iejaguar9(html, empresa):
    soup = BeautifulSoup(html, 'html.parser')
    print("\n=== Transmissoras Encontradas IEJAGUAR9 ===")
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
                        
                        if empreendimento and codigo_ons:
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

def download_documentos_iejaguar9(sessao, html, base_path):
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
                    base_url = "https://faturamento.iejaguar9.com.br/download.asp"
                    
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
                            print(f"Fatura IEJAGUAR9 {num_fatura} baixada com sucesso!")
                            
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
                                else:
                                    boleto_ext = '.dat'
                                
                                # Salvar o boleto separadamente
                                boleto_final = os.path.join(pasta_transmissora, f"boleto_{num_fatura}{boleto_ext}")
                                shutil.copy2(temp_boleto, boleto_final)
                                print(f"Boleto IEJAGUAR9 {num_fatura} salvo com sucesso!")
                            
                    except Exception as e:
                        print(f"Erro ao processar documentos IEJAGUAR9 da fatura {num_fatura}: {str(e)}")

def main():
    # Lista de credenciais e suas respectivas empresas
    credenciais = [
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
        {
            "usuario": "fatbol_dressler@vbasystems.com.br",
            "senha": "27093977",
            "pasta_base": "DRESSLER",
            "empresa": "DE"
        }
    ]
    
    # Processar EVRECY
    print("\n=== PROCESSANDO EVRECY ===")
    for credencial in credenciais:
        empresa_pasta = credencial["empresa"]  # AE ou DE
        
        if isinstance(credencial["pasta_base"], str):  # Se for LIBRAS ou DRESSLER
            print(f"\nProcessando empresa: {credencial['pasta_base']}")
            print("-" * 50)
            
            # Fazer login
            sessao = login_evrecy(credencial["usuario"], credencial["senha"])
            
            if sessao:
                resultado = pesquisar_faturas(sessao)
                if resultado:
                    extrair_e_mostrar_transmissoras(resultado, credencial["pasta_base"])
                    print("\nIniciando downloads dos documentos...")
                    
                    base_path = os.path.join(r"C:\Users\Bruno\Downloads\TUST\EVRECRY", empresa_pasta, credencial["pasta_base"])
                    download_documentos(sessao, resultado, base_path)
                    
                    print(f"\nProcesso finalizado para {credencial['pasta_base']}!")
        
        else:  # Se for COREMAS ou SJP
            # Fazer login uma única vez
            sessao = login_evrecy(credencial["usuario"], credencial["senha"])
            
            if sessao:
                resultado = pesquisar_faturas(sessao)
                if resultado:
                    # Para cada transmissora
                    soup = BeautifulSoup(resultado, 'html.parser')
                    transmissoras = soup.find_all('fieldset')
                    
                    for i, transmissora in enumerate(transmissoras):
                        nome_transmissora = transmissora.find('legend').text.strip()
                        pasta_base = credencial["pasta_base"][i]  # COREMAS I,II,III ou SJP1,2,5,6
                        
                        print(f"\nProcessando: {pasta_base}")
                        print("-" * 50)
                        
                        # Criar HTML específico para esta transmissora
                        novo_html = f"""
                        <fieldset>
                            <legend>{nome_transmissora}</legend>
                            {transmissora.find('table').prettify()}
                        </fieldset>
                        """
                        
                        extrair_e_mostrar_transmissoras(novo_html, pasta_base)
                        print("\nIniciando downloads dos documentos...")
                        
                        base_path = os.path.join(r"C:\Users\Bruno\Downloads\TUST\EVRECRY", empresa_pasta, pasta_base)
                        download_documentos(sessao, novo_html, base_path)
                        
                        print(f"\nProcesso finalizado para {pasta_base}!")
    
    # Processar IESUL
    print("\n=== PROCESSANDO IESUL ===")
    for credencial in credenciais:
        empresa_pasta = credencial["empresa"]  # AE ou DE
        
        if isinstance(credencial["pasta_base"], str):  # Se for LIBRAS ou DRESSLER
            print(f"\nProcessando empresa IESUL: {credencial['pasta_base']}")
            print("-" * 50)
            
            # Fazer login
            sessao = login_iesul(credencial["usuario"], credencial["senha"])
            
            if sessao:
                resultado = pesquisar_faturas_iesul(sessao)
                if resultado:
                    tem_faturas = extrair_e_mostrar_transmissoras_iesul(resultado, credencial["pasta_base"])
                    if tem_faturas:
                        print("\nIniciando downloads dos documentos IESUL...")
                        
                        base_path = os.path.join(r"C:\Users\Bruno\Downloads\TUST\IESUL", empresa_pasta, credencial["pasta_base"])
                        download_documentos_iesul(sessao, resultado, base_path)
                        
                        print(f"\nProcesso IESUL finalizado para {credencial['pasta_base']}!")
                    else:
                        print(f"\nNenhuma fatura encontrada no IESUL para {credencial['pasta_base']}!")
        
        else:  # Se for COREMAS ou SJP
            # Fazer login uma única vez
            sessao = login_iesul(credencial["usuario"], credencial["senha"])
            
            if sessao:
                resultado = pesquisar_faturas_iesul(sessao)
                if resultado:
                    # Para cada transmissora
                    soup = BeautifulSoup(resultado, 'html.parser')
                    transmissoras = soup.find_all('fieldset')
                    
                    for i, transmissora in enumerate(transmissoras):
                        nome_transmissora = transmissora.find('legend').text.strip()
                        pasta_base = credencial["pasta_base"][i]  # COREMAS I,II,III ou SJP1,2,5,6
                        
                        print(f"\nProcessando IESUL: {pasta_base}")
                        print("-" * 50)
                        
                        # Criar HTML específico para esta transmissora
                        novo_html = f"""
                        <fieldset>
                            <legend>{nome_transmissora}</legend>
                            {transmissora.find('table').prettify()}
                        </fieldset>
                        """
                        
                        extrair_e_mostrar_transmissoras(novo_html, pasta_base)
                        print("\nIniciando downloads dos documentos IESUL...")
                        
                        base_path = os.path.join(r"C:\Users\Bruno\Downloads\TUST\IESUL", empresa_pasta, pasta_base)
                        download_documentos_iesul(sessao, novo_html, base_path)
                        
                        print(f"\nProcesso IESUL finalizado para {pasta_base}!")

    # Processar IENNE
    print("\n=== PROCESSANDO IENNE ===")
    for credencial in credenciais:
        empresa_pasta = credencial["empresa"]  # AE ou DE
        
        if isinstance(credencial["pasta_base"], str):  # Se for LIBRAS ou DRESSLER
            print(f"\nProcessando empresa IENNE: {credencial['pasta_base']}")
            print("-" * 50)
            
            # Fazer login
            sessao = login_ienne(credencial["usuario"], credencial["senha"])
            
            if sessao:
                resultado = pesquisar_faturas_ienne(sessao)
                if resultado:
                    tem_faturas = extrair_e_mostrar_transmissoras_ienne(resultado, credencial["pasta_base"])
                    if tem_faturas:
                        print("\nIniciando downloads dos documentos IENNE...")
                        
                        base_path = os.path.join(r"C:\Users\Bruno\Downloads\TUST\IENNE", empresa_pasta, credencial["pasta_base"])
                        download_documentos_ienne(sessao, resultado, base_path)
                        
                        print(f"\nProcesso IENNE finalizado para {credencial['pasta_base']}!")
                    else:
                        print(f"\nNenhuma fatura encontrada no IENNE para {credencial['pasta_base']}!")
        
        else:  # Se for COREMAS ou SJP
            # Fazer login uma única vez
            sessao = login_ienne(credencial["usuario"], credencial["senha"])
            
            if sessao:
                resultado = pesquisar_faturas_ienne(sessao)
                if resultado:
                    # Para cada transmissora
                    soup = BeautifulSoup(resultado, 'html.parser')
                    transmissoras = soup.find_all('fieldset')
                    
                    for i, transmissora in enumerate(transmissoras):
                        nome_transmissora = transmissora.find('legend').text.strip()
                        pasta_base = credencial["pasta_base"][i]  # COREMAS I,II,III ou SJP1,2,5,6
                        
                        print(f"\nProcessando IENNE: {pasta_base}")
                        print("-" * 50)
                        
                        # Criar HTML específico para esta transmissora
                        novo_html = f"""
                        <fieldset>
                            <legend>{nome_transmissora}</legend>
                            {transmissora.find('table').prettify()}
                        </fieldset>
                        """
                        
                        extrair_e_mostrar_transmissoras_ienne(novo_html, pasta_base)
                        print("\nIniciando downloads dos documentos IENNE...")
                        
                        base_path = os.path.join(r"C:\Users\Bruno\Downloads\TUST\IENNE", empresa_pasta, pasta_base)
                        download_documentos_ienne(sessao, novo_html, base_path)
                        
                        print(f"\nProcesso IENNE finalizado para {pasta_base}!")

    # Processar IEMG
    print("\n=== PROCESSANDO IEMG ===")
    for credencial in credenciais:
        empresa_pasta = credencial["empresa"]  # AE ou DE
        
        if isinstance(credencial["pasta_base"], str):  # Se for LIBRAS ou DRESSLER
            print(f"\nProcessando empresa IEMG: {credencial['pasta_base']}")
            print("-" * 50)
            
            # Fazer login
            sessao = login_iemg(credencial["usuario"], credencial["senha"])
            
            if sessao:
                resultado = pesquisar_faturas_iemg(sessao)
                if resultado:
                    tem_faturas = extrair_e_mostrar_transmissoras_iemg(resultado, credencial["pasta_base"])
                    if tem_faturas:
                        print("\nIniciando downloads dos documentos IEMG...")
                        
                        base_path = os.path.join(r"C:\Users\Bruno\Downloads\TUST\IEMG", empresa_pasta, credencial["pasta_base"])
                        download_documentos_iemg(sessao, resultado, base_path)
                        
                        print(f"\nProcesso IEMG finalizado para {credencial['pasta_base']}!")
                    else:
                        print(f"\nNenhuma fatura encontrada no IEMG para {credencial['pasta_base']}!")
        
        else:  # Se for COREMAS ou SJP
            # Fazer login uma única vez
            sessao = login_iemg(credencial["usuario"], credencial["senha"])
            
            if sessao:
                resultado = pesquisar_faturas_iemg(sessao)
                if resultado:
                    # Para cada transmissora
                    soup = BeautifulSoup(resultado, 'html.parser')
                    transmissoras = soup.find_all('fieldset')
                    
                    for i, transmissora in enumerate(transmissoras):
                        nome_transmissora = transmissora.find('legend').text.strip()
                        pasta_base = credencial["pasta_base"][i]  # COREMAS I,II,III ou SJP1,2,5,6
                        
                        print(f"\nProcessando IEMG: {pasta_base}")
                        print("-" * 50)
                        
                        # Criar HTML específico para esta transmissora
                        novo_html = f"""
                        <fieldset>
                            <legend>{nome_transmissora}</legend>
                            {transmissora.find('table').prettify()}
                        </fieldset>
                        """
                        
                        extrair_e_mostrar_transmissoras_iemg(novo_html, pasta_base)
                        print("\nIniciando downloads dos documentos IEMG...")
                        
                        base_path = os.path.join(r"C:\Users\Bruno\Downloads\TUST\IEMG", empresa_pasta, pasta_base)
                        download_documentos_iemg(sessao, novo_html, base_path)
                        
                        print(f"\nProcesso IEMG finalizado para {pasta_base}!")

    # Processar IEMADEIRA
    print("\n=== PROCESSANDO IEMADEIRA ===")
    for credencial in credenciais:
        empresa_pasta = credencial["empresa"]  # AE ou DE
        
        if isinstance(credencial["pasta_base"], str):  # Se for LIBRAS ou DRESSLER
            print(f"\nProcessando empresa IEMADEIRA: {credencial['pasta_base']}")
            print("-" * 50)
            
            # Fazer login
            sessao = login_iemadeira(credencial["usuario"], credencial["senha"])
            
            if sessao:
                resultado = pesquisar_faturas_iemadeira(sessao)
                if resultado:
                    tem_faturas = extrair_e_mostrar_transmissoras_iemadeira(resultado, credencial["pasta_base"])
                    if tem_faturas:
                        print("\nIniciando downloads dos documentos IEMADEIRA...")
                        
                        base_path = os.path.join(r"C:\Users\Bruno\Downloads\TUST\IEMADEIRA", empresa_pasta, credencial["pasta_base"])
                        download_documentos_iemadeira(sessao, resultado, base_path)
                        
                        print(f"\nProcesso IEMADEIRA finalizado para {credencial['pasta_base']}!")
                    else:
                        print(f"\nNenhuma fatura encontrada no IEMADEIRA para {credencial['pasta_base']}!")
        
        else:  # Se for COREMAS ou SJP
            # Fazer login uma única vez
            sessao = login_iemadeira(credencial["usuario"], credencial["senha"])
            
            if sessao:
                resultado = pesquisar_faturas_iemadeira(sessao)
                if resultado:
                    # Para cada transmissora
                    soup = BeautifulSoup(resultado, 'html.parser')
                    transmissoras = soup.find_all('fieldset')
                    
                    for i, transmissora in enumerate(transmissoras):
                        nome_transmissora = transmissora.find('legend').text.strip()
                        pasta_base = credencial["pasta_base"][i]  # COREMAS I,II,III ou SJP1,2,5,6
                        
                        print(f"\nProcessando IEMADEIRA: {pasta_base}")
                        print("-" * 50)
                        
                        # Criar HTML específico para esta transmissora
                        novo_html = f"""
                        <fieldset>
                            <legend>{nome_transmissora}</legend>
                            {transmissora.find('table').prettify()}
                        </fieldset>
                        """
                        
                        extrair_e_mostrar_transmissoras_iemadeira(novo_html, pasta_base)
                        print("\nIniciando downloads dos documentos IEMADEIRA...")
                        
                        base_path = os.path.join(r"C:\Users\Bruno\Downloads\TUST\IEMADEIRA", empresa_pasta, pasta_base)
                        download_documentos_iemadeira(sessao, novo_html, base_path)
                        
                        print(f"\nProcesso IEMADEIRA finalizado para {pasta_base}!")

    # Processar IEJAGUAR9
    print("\n=== PROCESSANDO IEJAGUAR9 ===")
    for credencial in credenciais:
        empresa_pasta = credencial["empresa"]  # AE ou DE
        
        if isinstance(credencial["pasta_base"], str):  # Se for LIBRAS ou DRESSLER
            print(f"\nProcessando empresa IEJAGUAR9: {credencial['pasta_base']}")
            print("-" * 50)
            
            # Fazer login
            sessao = login_iejaguar9(credencial["usuario"], credencial["senha"])
            
            if sessao:
                resultado = pesquisar_faturas_iejaguar9(sessao)
                if resultado:
                    tem_faturas = extrair_e_mostrar_transmissoras_iejaguar9(resultado, credencial["pasta_base"])
                    if tem_faturas:
                        print("\nIniciando downloads dos documentos IEJAGUAR9...")
                        
                        base_path = os.path.join(r"C:\Users\Bruno\Downloads\TUST\IEJAGUAR9", empresa_pasta, credencial["pasta_base"])
                        download_documentos_iejaguar9(sessao, resultado, base_path)
                        
                        print(f"\nProcesso IEJAGUAR9 finalizado para {credencial['pasta_base']}!")
                    else:
                        print(f"\nNenhuma fatura encontrada no IEJAGUAR9 para {credencial['pasta_base']}!")
        
        else:  # Se for COREMAS ou SJP
            # Fazer login uma única vez
            sessao = login_iejaguar9(credencial["usuario"], credencial["senha"])
            
            if sessao:
                resultado = pesquisar_faturas_iejaguar9(sessao)
                if resultado:
                    # Para cada transmissora
                    soup = BeautifulSoup(resultado, 'html.parser')
                    transmissoras = soup.find_all('fieldset')
                    
                    for i, transmissora in enumerate(transmissoras):
                        nome_transmissora = transmissora.find('legend').text.strip()
                        pasta_base = credencial["pasta_base"][i]  # COREMAS I,II,III ou SJP1,2,5,6
                        
                        print(f"\nProcessando IEJAGUAR9: {pasta_base}")
                        print("-" * 50)
                        
                        # Criar HTML específico para esta transmissora
                        novo_html = f"""
                        <fieldset>
                            <legend>{nome_transmissora}</legend>
                            {transmissora.find('table').prettify()}
                        </fieldset>
                        """
                        
                        extrair_e_mostrar_transmissoras_iejaguar9(novo_html, pasta_base)
                        print("\nIniciando downloads dos documentos IEJAGUAR9...")
                        
                        base_path = os.path.join(r"C:\Users\Bruno\Downloads\TUST\IEJAGUAR9", empresa_pasta, pasta_base)
                        download_documentos_iejaguar9(sessao, novo_html, base_path)
                        
                        print(f"\nProcesso IEJAGUAR9 finalizado para {pasta_base}!")

if __name__ == "__main__":
    main()