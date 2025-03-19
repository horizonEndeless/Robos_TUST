import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import parse_qs, urlparse

def extract_form_url(html_content):
    """Extrai a URL do formulário de login do HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')
    form = soup.find('form')
    if form and form.get('action'):
        return form['action']
    raise Exception("Não foi possível encontrar o formulário de login")

def extract_session_code(form_url):
    """Extrai o session_code da URL do formulário"""
    parsed = urlparse(form_url)
    params = parse_qs(parsed.query)
    session_code = params.get('session_code', [None])[0]
    if not session_code:
        raise Exception("Não foi possível encontrar o session_code")
    return session_code

def extract_execution(form_url):
    """Extrai o parâmetro execution da URL do formulário"""
    parsed = urlparse(form_url)
    params = parse_qs(parsed.query)
    execution = params.get('execution', [None])[0]
    if not execution:
        raise Exception("Não foi possível encontrar o parâmetro execution")
    return execution

def extract_tab_id(form_url):
    """Extrai o tab_id da URL do formulário"""
    parsed = urlparse(form_url)
    params = parse_qs(parsed.query)
    tab_id = params.get('tab_id', [None])[0]
    if not tab_id:
        raise Exception("Não foi possível encontrar o tab_id")
    return tab_id

def login_ons():
    # URL base e endpoints
    base_url = "https://sso.ons.org.br"
    auth_endpoint = "/auth/realms/ONS/protocol/openid-connect/auth"
    
    # Parâmetros da requisição
    params = {
        "client_id": "FEDERATION",
        "redirect_uri": "https://pops.ons.org.br/ons.pop.federation/Azure/",
        "response_type": "code",
        "scope": "openid",
        "code_challenge": "TcVu-KLqdITI9H8gENJ-S4dtGLcDxxHnGgjDLoxGz-4",
        "code_challenge_method": "S256",
        "state": "OpenIdConnect.AuthenticationProperties=61fc66zPrC-YMmzNOFT67CsPrvxlHynKjksHITDfhLKxVgHg69hFp_pE426lw2YNX8hDSHrEpFHgeYHDMMlPT7WHnMp4Klp3Ma_acTNFjUn_06Yp7YHwvhQLRPPwGK8kVViUfjOBTl3PKAbqb9AFfUTGY2KaApp8S6wDQcP95VGug5hVOW2iurDlnnLlXSEbeetEsbXZZG3n5qdMR6GSfeGAUax6Go0tPrQARlJcDa5ujtRTnBbTnkSSizNnyGta82Rz",
        "response_mode": "form_post",
        "nonce": "638749845784231840.ZDZmNWY3N2MtNzI0MS00NjA1LTgyNjMtNGE3YzM1ZWJkMzY1MjQxMDFjNmQtM2Y3Yi00MTA5LTg3NTUtOWE0NTVkYjMxZGJm",
        "x-client-SKU": "ID_NET461",
        "x-client-ver": "5.3.0.0"
    }

    # Atualiza os headers para incluir todos os necessários
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://sso.ons.org.br",
        "Referer": base_url + auth_endpoint,
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Google Chrome\";v=\"133\", \"Chromium\";v=\"133\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }

    # Sessão para manter cookies
    session = requests.Session()

    try:
        # Primeira requisição para obter o formulário de login
        print("Fazendo primeira requisição GET...")
        response = session.get(
            f"{base_url}{auth_endpoint}",
            params=params,
            headers=headers,
            verify=True,
            allow_redirects=True
        )
        
        print(f"Status code inicial: {response.status_code}")
        print(f"Cookies iniciais: {response.cookies.get_dict()}")
        print(f"URL atual: {response.url}")

        # Extrai o URL do formulário e o session_code
        form_url = extract_form_url(response.text)
        session_code = extract_session_code(form_url)
        execution = extract_execution(form_url)

        # Dados do formulário de login
        login_data = {
            "username": "tust@rioenergy.com.br",
            "password": "Ca2003@#",
            "credentialId": "",
            "login": "Entrar",
            "session_code": session_code,
            "execution": execution,
            "client_id": "FEDERATION",
            "tab_id": extract_tab_id(form_url)
        }

        # Faz a requisição POST de login
        print("\nFazendo requisição POST de login...")
        login_response = session.post(
            form_url,
            data=login_data,
            headers=headers,
            verify=True,
            allow_redirects=True
        )
        
        print(f"\nStatus code do login: {login_response.status_code}")
        print(f"Cookies após login: {login_response.cookies.get_dict()}")
        print(f"URL final: {login_response.url}")
        
        if login_response.status_code != 200:
            print(f"Conteúdo da resposta de erro: {login_response.text}")
        
        return login_response

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        print(f"Detalhes do erro: {str(e)}")
        return None

if __name__ == "__main__":
    resultado = login_ons()
    if resultado:
        print("Status code:", resultado.status_code)
        print("Cookies:", resultado.cookies.get_dict())
