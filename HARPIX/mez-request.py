import requests

def acessar_iframe():
    # URL da página de login
    login_url = "https://harpixfat.mezenergia.com/FAT/form.do"
    # Dados para o login
    login_data = {
        "sys": "FAT",
        "formID": "3",
        "action": "form",
        "param": "post",
        "WEBRUN-CSRFTOKEN": "6XCMdpD7lcHWer8pOnYv",  # Certifique-se de que este token está correto
        "goto": "-1",
        "invisibleFields": "",
        "storedProcedureName": "",
        "storedProcedureParams": "",
        "txtONS": "4313"  # Código ONS
    }

    # Headers para a requisição
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/xml,text/html,application/xhtml+xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    # Inicia uma sessão
    with requests.Session() as session:
        # Faz o login
        response = session.post(login_url, data=login_data, headers=headers)
        
        # Verifica se o login foi bem-sucedido
        if response.status_code == 200:
            print("Login realizado com sucesso!")
            
            # URL do iframe
            iframe_url = "https://harpixfat.mezenergia.com/FAT/openform.do?sys=FAT&action=openform&formID=3&firstLoad=true"
            
            # Faz a requisição para acessar o iframe
            response = session.get(iframe_url, headers=headers)
            
            if response.status_code == 200:
                content = response.content.decode('ISO-8859-1')
                print("Conteúdo do iframe:")
                print(content)  # Mostra o conteúdo do iframe
            else:
                print(f"Erro ao acessar o iframe: {response.status_code}")
        else:
            print(f"Erro no login: {response.status_code}")

# Chama a função para acessar o iframe
acessar_iframe()