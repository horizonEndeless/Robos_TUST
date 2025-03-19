import win32com.client
import os
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import json

def carregar_mapeamento_cnpj():
    # Caminho para o arquivo de mapeamento
    arquivo_mapeamento = r"C:\Users\Bruno\Desktop\Workspace\Email\mapeamento_cnpj.json"
    
    try:
        with open(arquivo_mapeamento, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Arquivo de mapeamento não encontrado em: {arquivo_mapeamento}")
        return {}
    except Exception as e:
        print(f"Erro ao ler arquivo de mapeamento: {str(e)}")
        return {}

def extrair_cnpj_do_xml(caminho_xml):
    try:
        tree = ET.parse(caminho_xml)
        root = tree.getroot()
        
        # Procurar pelo CNPJ em qualquer namespace
        for elem in root.iter():
            if 'emit' in elem.tag:
                for child in elem:
                    if 'CNPJ' in child.tag:
                        return child.text
        return None
    except Exception as e:
        print(f"Erro ao ler XML: {str(e)}")
        return None

def baixar_anexos_outlook(remetente, dias_atras):
    # Criar uma instância do Outlook
    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")

    # Configurar a conta de email
    for account in namespace.Accounts:
        if account.SmtpAddress == "services.easytust@outlook.com":
            inbox = account.DeliveryStore.GetDefaultFolder(6)
            break
    
    # Pasta para salvar os anexos
    pasta_destino = r"C:\Users\Bruno\Desktop\Workspace\Email\Anexos"
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    # Carregar mapeamento de CNPJs
    mapeamento_cnpj = carregar_mapeamento_cnpj()

    # Calcular a data inicial (dias atrás a partir de hoje)
    data_atual = datetime.now()
    data_inicial = data_atual - timedelta(days=dias_atras)
    print(f"Buscando emails de {data_inicial.strftime('%d/%m/%Y')} até {data_atual.strftime('%d/%m/%Y')}")

    # Filtrar emails
    emails = inbox.Items
    emails.Sort("[ReceivedTime]", True)

    for email in emails:
        try:
            if hasattr(email, 'ReceivedTime') and hasattr(email, 'SenderEmailAddress'):
                data_email = email.ReceivedTime.date()
                
                # Verificar se o email está dentro do período e é do remetente correto
                if (email.SenderEmailAddress.lower() == remetente.lower() and 
                    data_inicial.date() <= data_email <= data_atual.date()):
                    
                    data_hora_email = email.ReceivedTime.strftime("%Y%m%d_%H%M%S")
                    assunto = email.Subject[:30]
                    assunto = "".join(c for c in assunto if c.isalnum() or c in (' ', '-', '_')).strip()
                    nome_pasta_temp = f"{data_hora_email}_{assunto}"
                    pasta_email_temp = os.path.join(pasta_destino, nome_pasta_temp)
                    
                    if not os.path.exists(pasta_email_temp):
                        os.makedirs(pasta_email_temp)
                    
                    cnpj_encontrado = None
                    
                    # Primeiro, salvar todos os anexos
                    if email.Attachments.Count > 0:
                        for anexo in email.Attachments:
                            if anexo.FileName.lower().endswith(('.pdf', '.doc', '.docx', '.xml')):
                                caminho_arquivo = os.path.join(pasta_email_temp, anexo.FileName)
                                anexo.SaveAsFile(caminho_arquivo)
                                
                                # Se for XML, tentar extrair CNPJ
                                if anexo.FileName.lower().endswith('.xml'):
                                    cnpj = extrair_cnpj_do_xml(caminho_arquivo)
                                    if cnpj and cnpj in mapeamento_cnpj:
                                        cnpj_encontrado = cnpj
                    
                    # Renomear a pasta se encontrou CNPJ mapeado
                    if cnpj_encontrado:
                        nome_pasta_final = mapeamento_cnpj[cnpj_encontrado]
                        pasta_email_final = os.path.join(pasta_destino, nome_pasta_final)
                        
                        # Se já existir pasta com esse nome, adiciona um número
                        contador = 1
                        nome_pasta_base = nome_pasta_final
                        while os.path.exists(pasta_email_final):
                            nome_pasta_final = f"{nome_pasta_base}_{contador}"
                            pasta_email_final = os.path.join(pasta_destino, nome_pasta_final)
                            contador += 1
                        
                        os.rename(pasta_email_temp, pasta_email_final)
                        print(f"Pasta renomeada para: {nome_pasta_final}")
                    else:
                        print(f"CNPJ não encontrado ou não mapeado. Mantendo nome original: {nome_pasta_temp}")
        except Exception as e:
            print(f"Erro ao processar email: {str(e)}")
            continue

def main():
    remetente = input("Digite o email do remetente: ")
    dias = int(input("Digite quantos dias para trás você quer buscar: "))
    
    try:
        baixar_anexos_outlook(remetente, dias)
        print("Processo concluído com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")

if __name__ == "__main__":
    main()
