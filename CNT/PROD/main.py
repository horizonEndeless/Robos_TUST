import requests
import os
from datetime import datetime

def baixar_xml_cnt(codigo_ons, empresa):
    # Criar uma sessão para manter os cookies
    session = requests.Session()
    
    # 1. Primeiro acesso à página principal
    url_principal = "https://cntgo.com.br/faturas.html"
    
    headers_principal = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }
    
    try:
        # Acessar a página principal
        print(f"\nAcessando página principal para empresa {empresa} - Código ONS: {codigo_ons}...")
        response_principal = session.get(url_principal, headers=headers_principal)
        
        if response_principal.status_code != 200:
            print(f"Erro ao acessar página principal. Status code: {response_principal.status_code}")
            return False
        
        # 2. Simular o envio do formulário (clique no botão BAIXAR)
        url_form = "https://cntgo.com.br/form.php"
        
        headers_form = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://cntgo.com.br",
            "Referer": "https://cntgo.com.br/faturas.html"
        }
        
        form_data = {
            "code": str(codigo_ons)
        }
        
        print(f"Enviando requisição para baixar XML...")
        response_form = session.post(url_form, headers=headers_form, data=form_data)
        
        if response_form.status_code == 200 and response_form.content:
            # Criar pasta base se não existir
            pasta_base = r"C:\Users\Bruno\Downloads\TUST\CNT"
            if not os.path.exists(pasta_base):
                os.makedirs(pasta_base)
            
            # Criar pasta da empresa (RE, AE ou DE)
            pasta_empresa = os.path.join(pasta_base, empresa)
            if not os.path.exists(pasta_empresa):
                os.makedirs(pasta_empresa)
            
            # Criar pasta específica para o código ONS dentro da pasta da empresa
            pasta_ons = os.path.join(pasta_empresa, f"ONS_{codigo_ons}")
            if not os.path.exists(pasta_ons):
                os.makedirs(pasta_ons)
            
            # Salvar o arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = os.path.join(pasta_ons, f"{codigo_ons}_{timestamp}.xml")
            
            with open(nome_arquivo, "wb") as f:
                f.write(response_form.content)
            
            print(f"Arquivo XML baixado com sucesso: {nome_arquivo}")
            return True
        else:
            print(f"Erro ao baixar o arquivo. Status code: {response_form.status_code}")
            print(f"Resposta do servidor: {response_form.text[:200]}")
            return False
            
    except Exception as e:
        print(f"Erro durante o processo: {str(e)}")
        return False

def baixar_todas_empresas():
    # Dicionário com as empresas e seus códigos ONS
    empresas = {
        "RE": [
            "4313", "4314", "3430", "3431", "3432", "4415", "4315", "4316",
            "3502", "3497", "3503", "3530", "3498", "3531", "3532", "3537",
            "3538", "3947", "3948", "3969", "3970", "3976", "3972"
        ],
        "AE": [
            "3859", "3860", "3861", "3862", "3863", "3864",
            "3740", "3741", "3750", "8011"
        ],
        "DE": ["3748"]
    }
    
    print("Iniciando download dos XMLs para todas as empresas...")
    
    for empresa, codigos in empresas.items():
        print(f"\n{'='*50}")
        print(f"Processando empresa: {empresa}")
        print(f"{'='*50}")
        
        for codigo in codigos:
            print(f"\nBaixando XML para código ONS: {codigo}")
            baixar_xml_cnt(codigo, empresa)

if __name__ == "__main__":
    opcao = input("Digite:\n1 - Para baixar XML de uma empresa específica\n2 - Para baixar de todas as empresas\nEscolha: ")
    
    if opcao == "1":
        empresa = input("Digite a empresa (RE, AE ou DE): ").upper()
        codigo_ons = input("Digite o código ONS: ")
        if empresa in ["RE", "AE", "DE"]:
            baixar_xml_cnt(codigo_ons, empresa)
        else:
            print("Empresa inválida!")
    elif opcao == "2":
        baixar_todas_empresas()
    else:
        print("Opção inválida!")
