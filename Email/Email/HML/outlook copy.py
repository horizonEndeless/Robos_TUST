import os
import requests
import email
import imaplib
from datetime import datetime, timedelta
from email.header import decode_header

# Configurações de autenticação OAuth2
CLIENT_ID = "53475b80-4d2d-4d59-b1a5-61614d590165"
CLIENT_SECRET = "nd88Q~ZMZ3fuQIBA3Czd9XP-D5ejC~M5ZMCTkc3c"
TENANT_ID = "c125ac39-075a-417e-9ebf-a89d09d08846"
EMAIL = "faturas.libra@americaenergia.com.br"
REMETENTE = "nfe@neoenergia.com"

# Configurações do servidor IMAP
IMAP_SERVER = "outlook.office365.com"
IMAP_PORT = 993

# Configurações do diretório para salvar anexos
PASTA_DESTINO = r"C:\Users\Bruno\Downloads\TUST\ANEXOS OUTLOOK"

def obter_token_oauth2():
    """Obtém um token OAuth2 usando o fluxo client_credentials"""
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/token"
    
    dados = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'resource': 'https://outlook.office.com'
    }
    
    resposta = requests.post(url, data=dados)
    
    if resposta.status_code == 200:
        return resposta.json().get('access_token')
    else:
        print(f"Erro ao obter token: {resposta.status_code} - {resposta.text}")
        return None

def baixar_anexos():
    """Baixa anexos de emails dos últimos 30 dias do remetente especificado"""
    # Criar pasta de destino se não existir
    if not os.path.exists(PASTA_DESTINO):
        os.makedirs(PASTA_DESTINO)
    
    # Obter token OAuth2
    print("Obtendo token de autenticação OAuth2...")
    token = obter_token_oauth2()
    
    if not token:
        print("Falha ao obter token de autenticação.")
        return
    
    try:
        # Conectar ao servidor IMAP
        print(f"Conectando ao servidor IMAP {IMAP_SERVER}...")
        imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        
        # Autenticar com OAuth2
        auth_string = f'user={EMAIL}\x01auth=Bearer {token}\x01\x01'
        imap.authenticate('XOAUTH2', lambda x: auth_string)
        
        # Selecionar a caixa de entrada
        imap.select('INBOX')
        
        # Calcular data de 30 dias atrás
        data_inicial = (datetime.now() - timedelta(days=30)).strftime("%d-%b-%Y")
        
        # Buscar emails do remetente específico desde a data inicial
        print(f"Buscando emails de {REMETENTE} nos últimos 30 dias...")
        status, mensagens = imap.search(None, f'(SINCE "{data_inicial}" FROM "{REMETENTE}")')
        
        ids_mensagens = mensagens[0].split()
        
        contador_emails = 0
        contador_anexos = 0
        
        # Processar cada mensagem
        for id_mensagem in ids_mensagens:
            contador_emails += 1
            
            # Buscar a mensagem completa
            status, dados = imap.fetch(id_mensagem, '(RFC822)')
            mensagem_raw = dados[0][1]
            mensagem = email.message_from_bytes(mensagem_raw)
            
            # Obter assunto e data
            assunto = decode_header(mensagem['Subject'])[0][0]
            if isinstance(assunto, bytes):
                assunto = assunto.decode()
            
            data_recebimento = datetime.strptime(mensagem['Date'], "%a, %d %b %Y %H:%M:%S %z")
            print(f"Processando email: {assunto} ({data_recebimento.strftime('%Y-%m-%d')})")
            
            # Processar anexos
            for parte in mensagem.walk():
                if parte.get_content_maintype() == 'multipart':
                    continue
                
                if parte.get('Content-Disposition') is None:
                    continue
                
                nome_arquivo = parte.get_filename()
                if nome_arquivo:
                    # Decodificar nome do arquivo se necessário
                    nome_arquivo_decodificado = decode_header(nome_arquivo)[0][0]
                    if isinstance(nome_arquivo_decodificado, bytes):
                        nome_arquivo = nome_arquivo_decodificado.decode()
                    
                    # Criar caminho completo para salvar o arquivo
                    caminho_arquivo = os.path.join(PASTA_DESTINO, nome_arquivo)
                    
                    # Verificar se arquivo já existe
                    if os.path.exists(caminho_arquivo):
                        nome_base, extensao = os.path.splitext(nome_arquivo)
                        data_formatada = data_recebimento.strftime("%Y-%m-%d")
                        caminho_arquivo = os.path.join(PASTA_DESTINO, f"{nome_base}_{data_formatada}{extensao}")
                    
                    # Salvar anexo
                    with open(caminho_arquivo, 'wb') as arquivo:
                        arquivo.write(parte.get_payload(decode=True))
                    
                    contador_anexos += 1
                    print(f"Anexo salvo: {caminho_arquivo}")
        
        print(f"Processamento concluído: {contador_emails} emails encontrados, {contador_anexos} anexos salvos.")
        
        # Fechar conexão
        imap.close()
        imap.logout()
        
    except Exception as e:
        print(f"Erro durante o processo: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        print("Iniciando download de anexos do Outlook...")
        baixar_anexos()
        print("Download de anexos concluído com sucesso!")
    except Exception as e:
        print(f"Erro durante o processo: {str(e)}")
        import traceback
        traceback.print_exc()