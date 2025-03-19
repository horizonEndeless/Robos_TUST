import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import getpass
from datetime import datetime
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
    query = f'FROM "{sender}"'
    result, data = mail.search(None, query)
    email_ids = data[0].split()
    emails = []
    
    for e_id in email_ids:
        result, msg_data = mail.fetch(e_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        emails.append((e_id, msg))
    
    return emails

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
    
    mail = connect_imap()
    emails_to_forward = search_emails(mail, sender)
    
    print(f"{len(emails_to_forward)} e-mails encontrados. Encaminhando...")
    for e_id, msg in emails_to_forward:
        forward_email(msg)
    
    print("Processo concluído!")
    mail.logout()

if __name__ == "__main__":
    main()
