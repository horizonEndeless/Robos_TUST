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
            'data': '2024|11'
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

def main():
    # Lista de credenciais e suas respectivas empresas
    credenciais = [
        {
            "usuario": "kleber@libraligas.com.br",
            "senha": "542D1G6",
            "pasta_base": "LIBRAS"
        },
        {
            "usuario": "fatura.coremas@americaenergia.com.br",
            "senha": "2M4TO12",
            "pasta_base": ["COREMAS I", "COREMAS II", "COREMAS III"]
        },
        {
            "usuario": "faturas.sjp@americaenergia.com.br",
            "senha": "QM17DIB10",
            "pasta_base": ["SJP1", "SJP2","SPJ3", "SJP4", "SJP5", "SJP6"]
        }
    ]
    
    for credencial in credenciais:
        if isinstance(credencial["pasta_base"], str):  # Se for LIBRAS
            print(f"\nProcessando empresa: {credencial['pasta_base']}")
            print("-" * 50)
            
            # Fazer login
            sessao = login_evrecy(credencial["usuario"], credencial["senha"])
            
            if sessao:
                resultado = pesquisar_faturas(sessao)
                if resultado:
                    extrair_e_mostrar_transmissoras(resultado, credencial["pasta_base"])
                    print("\nIniciando downloads dos documentos...")
                    
                    base_path = os.path.join(r"C:\Users\Bruno\Downloads\IE", credencial["pasta_base"])
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
                        
                        base_path = os.path.join(r"C:\Users\Bruno\Downloads\IE", pasta_base)
                        download_documentos(sessao, novo_html, base_path)
                        
                        print(f"\nProcesso finalizado para {pasta_base}!")

if __name__ == "__main__":
    main()