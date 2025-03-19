import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import getpass
from datetime import datetime, timedelta
import smtplib

# Configurações do Roundcube (IMAP)
IMAP_SERVER = "imap.engenho.com"  # CONFIRMAR!
IMAP_PORT = 993
EMAIL_USER = "carolina@engenho.com"
EMAIL_PASS = "Carol2019"  # Senha fixa definida

# E-mail de destino
DEST_EMAIL = "tust@pontalenergy.com"

def connect_imap():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("inbox")
    return mail

def search_emails(mail, sender):
    # Criar data_atual e data_limite com fuso horário
    data_atual = datetime.now().astimezone()
    data_limite = (data_atual - timedelta(days=30))
    
    query = '(FROM "faturas_transmissao")'
    print(f"Executando query: {query}")
    
    result, data = mail.search(None, query)
    email_ids = data[0].split()
    filtered_emails = []
    
    print(f"Total de emails encontrados inicialmente: {len(email_ids)}")
    print(f"Buscando emails de {data_limite.strftime('%d/%m/%Y %H:%M:%S %z')} até {data_atual.strftime('%d/%m/%Y %H:%M:%S %z')}")
    
    for e_id in email_ids:
        result, msg_data = mail.fetch(e_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        print(f"\nProcessando email:")
        print(f"De: {msg['From']}")
        print(f"Data: {msg['Date']}")
        print(f"Assunto: {msg['Subject']}")
        
        email_date = msg["Date"]
        try:
            date_formats = [
                "%a, %d %b %Y %H:%M:%S %z",
                "%d %b %Y %H:%M:%S %z",
                "%a, %d %b %Y %H:%M:%S %Z",
                "%a, %d %b %Y %H:%M:%S",
                "%d/%m/%Y %H:%M"
            ]
            
            parsed_date = None
            for date_format in date_formats:
                try:
                    parsed_date = datetime.strptime(email_date, date_format)
                    if parsed_date.tzinfo is None:
                        # Se a data não tem fuso horário, adiciona o fuso local
                        parsed_date = parsed_date.astimezone()
                    print(f"Data parseada com sucesso usando formato: {date_format}")
                    break
                except ValueError:
                    continue
                    
            if parsed_date is None:
                print(f"Não foi possível parsear a data: {email_date}")
                continue
                
            print(f"Data parseada: {parsed_date}")
            
            # Agora ambas as datas têm fuso horário
            if data_limite <= parsed_date <= data_atual:
                filtered_emails.append((e_id, msg))
                print(f"Email adicionado à lista de encaminhamento")
            else:
                print(f"Email fora do período especificado")
                
        except Exception as e:
            print(f"Erro ao processar data do email: {e}")
            continue
    
    return filtered_emails

def forward_email(msg):
    smtp_server = "smtp.engenho.com"  # CONFIRMAR!
    smtp_port = 587  # Porta padrão
    
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASS)
    
    new_msg = MIMEMultipart()
    new_msg["From"] = EMAIL_USER
    new_msg["To"] = DEST_EMAIL
    new_msg["Subject"] = "FWD: " + (msg["Subject"] if msg["Subject"] else "(Sem Assunto)")
    
    body_content = "Encaminhado: \n\n"
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                try:
                    body_content += part.get_payload(decode=True).decode(errors="ignore")
                except AttributeError:
                    pass
    else:
        try:
            body_content += msg.get_payload(decode=True).decode(errors="ignore")
        except AttributeError:
            body_content += "(Sem conteúdo de texto)"
    
    new_msg.attach(MIMEText(body_content, "plain"))
    
    # Encaminhando anexos
    for part in msg.walk():
        if part.get_content_maintype() == "multipart":
            continue
        if part.get("Content-Disposition") is None:
            continue
        
        attachment = MIMEBase("application", "octet-stream")
        attachment.set_payload(part.get_payload(decode=True))
        encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", f'attachment; filename="{part.get_filename()}"')
        new_msg.attach(attachment)
    
    server.sendmail(EMAIL_USER, DEST_EMAIL, new_msg.as_string())
    server.quit()

def main():
    sender = "faturas_transmissao@cpfl.com.br"
    
    try:
        mail = connect_imap()
        print("Conexão IMAP estabelecida com sucesso")
        
        emails_to_forward = search_emails(mail, sender)
        
        print(f"\n{len(emails_to_forward)} e-mails encontrados. Encaminhando...")
        for e_id, msg in emails_to_forward:
            try:
                forward_email(msg)
                print(f"Email encaminhado com sucesso: {msg['Subject']}")
            except Exception as e:
                print(f"Erro ao encaminhar email: {e}")
        
        print("Processo concluído!")
        mail.logout()
    except Exception as e:
        print(f"Erro durante a execução: {e}")

if __name__ == "__main__":
    main()
