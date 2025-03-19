import requests
import os
import re


def baixar_arquivo(codigo, data, save_path):
    url = f"https://www.vsbtrans.com.br/getFiles.php?codigo={codigo}&data={data}"
    headers = {
        "accept": "*/*",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "priority": "u=1, i",
        "referer": "https://www.vsbtrans.com.br/",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            json_response = response.json()
            zip_url = json_response.get("zipUrl")
            if zip_url:
                download_url = f"https://www.vsbtrans.com.br{zip_url.replace('/', '/')}"
                download_zip(download_url, codigo, data, save_path)
            else:
                print(f"Erro: 'zipUrl' não encontrado no JSON para o código {codigo}.")
        except ValueError:
            print(f"Falha ao interpretar JSON para o código {codigo}. Conteúdo da resposta: {response.content[:200]}")
    else:
        print(f"Erro ao acessar o arquivo para o código {codigo}. Status code: {response.status_code}")


def download_zip(download_url, codigo, data, save_path):
    response = requests.get(download_url)

    if response.status_code == 200 and response.headers.get('Content-Type') == 'application/zip':
        filename = f"{data}_{codigo}_faturas.zip"
        file_path = os.path.join(save_path, filename)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Arquivo baixado com sucesso: {file_path}")
    else:
        print(f"Falha ao baixar o arquivo ZIP para o código {codigo}. Status code: {response.status_code}")


def obter_data_mais_recente():
    url = "https://www.vsbtrans.com.br/getFiles.php"
    headers = {
        "accept": "*/*",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "referer": "https://www.vsbtrans.com.br/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Procura todas as datas no formato YYYY.MM
            datas = re.findall(r'value="(\d{4}\.\d{2})"', response.text)
            if datas:
                # Ordena as datas em ordem decrescente e pega a primeira
                datas.sort(reverse=True)
                return datas[0]
        return "2025.02"  # Data padrão caso falhe
    except Exception as e:
        print(f"Erro ao obter data mais recente: {e}")
        return "2025.02"  # Data padrão em caso de erro


def rio_energy(save_path):
    empresa = "RE"
    pasta_empresa = os.path.join(save_path, empresa)
    os.makedirs(pasta_empresa, exist_ok=True)
    
    data_recente = obter_data_mais_recente()
    codigos_rio = [
        "4313", "4314", "3430", "3431", "3432", "4415", "4315", "4316", "3502",
        "3497", "3503", "3530", "3498", "3531", "3532", "3537", "3538", "3947",
        "3948", "3969", "3970", "3976", "3972"
    ]
    for codigo in codigos_rio:
        baixar_arquivo(codigo, data_recente, pasta_empresa)


def america(save_path):
    empresa = "AE"
    pasta_empresa = os.path.join(save_path, empresa)
    os.makedirs(pasta_empresa, exist_ok=True)
    
    data_recente = obter_data_mais_recente()
    codigos_america = ["8011", "3740", "3741", "3750", "3859", "3860", "3861", "3862", "3863", "3864"]
    for codigo in codigos_america:
        baixar_arquivo(codigo, data_recente, pasta_empresa)


def diamante_energia(save_path):
    empresa = "DE"
    pasta_empresa = os.path.join(save_path, empresa)
    os.makedirs(pasta_empresa, exist_ok=True)
    
    data_recente = obter_data_mais_recente()
    codigo_diamante = "3748"
    baixar_arquivo(codigo_diamante, data_recente, pasta_empresa)

def main():
    default_path = r"C:\Users\Bruno\Downloads\VSB"
    os.makedirs(default_path, exist_ok=True)
    
    print("\nIniciando download das faturas...")
    
    print("\nBaixando faturas da Rio Energy...")
    rio_energy(default_path)
    
    print("\nBaixando faturas da America...")
    america(default_path)
    
    print("\nBaixando faturas da Diamante Energia...")
    diamante_energia(default_path)
    
    print("\nDownload de todas as faturas concluído!")

if __name__ == '__main__':
    main()
