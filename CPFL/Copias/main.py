import requests

def login_cpfl():
    # URL do login
    url = "https://getweb.cpfl.com.br/getweb/getweb.jsf"
    
    # Dados de login
    payload = {
        'j_username': '27093977000238',
        'j_password': 'Diamante.2024',
        'javax.faces.ViewState': ''  # Precisaremos pegar este valor
    }
    
    # Headers básicos
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    
    # Primeira requisição para pegar o ViewState
    session = requests.Session()
    response = session.get(url)
    
    # Aqui você precisará implementar a lógica para extrair o ViewState
    
    # Fazer o POST com os dados de login
    login_response = session.post(url, data=payload, headers=headers)
    
    return login_response

if __name__ == "__main__":
    response = login_cpfl()
    print(response.status_code)
