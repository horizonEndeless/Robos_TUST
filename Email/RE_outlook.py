import os
import requests
import email
import imaplib
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from email.header import decode_header

# Configurações de autenticação OAuth2
CLIENT_ID = "148e28e7-1ccc-4e36-8fa4-b6521fd72f4d"
CLIENT_SECRET = "7FZ8Q~UCEtpuufXP-fWRb5XjTIA1vIWzhES6Xb9F"
TENANT_ID = "041c491a-706c-407b-ac5f-9cf3fde03c90"

# Configurações de contas de email
CONTAS_EMAIL = {
    "RE": {
        "email": "tust@pontalenergy.com" # PONTAL ENERGY
    }
}

# Email do remetente
REMETENTE = "nfe@neoenergia.com"

# Configurações do servidor IMAP
IMAP_SERVER = "outlook.office365.com"
IMAP_PORT = 993

# Configurações do diretório para salvar anexos
PASTA_DESTINO_BASE = r"C:\Users\Bruno\Downloads\TUST\ANEXOS OUTLOOK"

# Mapeamento de CNPJs para siglas de empresas
EMPRESAS = {
    "33485728000100": {"sigla": "BRJA", "nome": "BRJA", "ons": "4313", "codigo_neoenergia": "1108376"},
    "33485874000135": {"sigla": "BRJB", "nome": "BRJB", "ons": "4314", "codigo_neoenergia": "1108377"},
    "19233858000205": {"sigla": "CECA", "nome": "CECA", "ons": "3430", "codigo_neoenergia": "1101532"},
    "19235607000260": {"sigla": "CECB", "nome": "CECB", "ons": "3431", "codigo_neoenergia": "1101533"},
    "19560109000292": {"sigla": "CECC", "nome": "CECC", "ons": "3432", "codigo_neoenergia": "1101534"},
    "33457932000117": {"sigla": "CECD", "nome": "CECD", "ons": "4415", "codigo_neoenergia": "1108935"},
    "33471379000177": {"sigla": "CECE", "nome": "CECE", "ons": "4315", "codigo_neoenergia": "1108378"},
    "33468809000100": {"sigla": "CECF", "nome": "CECF", "ons": "4316", "codigo_neoenergia": "1108379"},
    "19560032000250": {"sigla": "ITA1", "nome": "ITA1", "ons": "3502", "codigo_neoenergia": "1101690"},
    "19560074000291": {"sigla": "ITA2", "nome": "ITA2", "ons": "3497", "codigo_neoenergia": "1101632"},
    "19560839000293": {"sigla": "ITA3", "nome": "ITA3", "ons": "3503", "codigo_neoenergia": "1101691"},
    "20553751000223": {"sigla": "ITA4", "nome": "ITA4", "ons": "3530", "codigo_neoenergia": "1101738"},
    "19560868000255": {"sigla": "ITA5", "nome": "ITA5", "ons": "3498", "codigo_neoenergia": "1101633"},
    "20533879000225": {"sigla": "ITA6", "nome": "ITA6", "ons": "3531", "codigo_neoenergia": "1101739"},
    "20533473000242": {"sigla": "ITA7", "nome": "ITA7", "ons": "3532", "codigo_neoenergia": "1101740"},
    "20533310000260": {"sigla": "ITA8", "nome": "ITA8", "ons": "3537", "codigo_neoenergia": "1101754"},
    "20533377000202": {"sigla": "ITA9", "nome": "ITA9", "ons": "3538", "codigo_neoenergia": "1101755"},
    "30063842000234": {"sigla": "SDBA", "nome": "SDBA", "ons": "3947", "codigo_neoenergia": "1105036"},
    "29527877000206": {"sigla": "SDBB", "nome": "SDBB", "ons": "3948", "codigo_neoenergia": "1105037"},
    "29591504000296": {"sigla": "SDBC", "nome": "SDBC", "ons": "3969", "codigo_neoenergia": "1105267"},
    "30062725000256": {"sigla": "SDBD", "nome": "SDBD", "ons": "3970", "codigo_neoenergia": "1105268"},
    "30062736000236": {"sigla": "SDBE", "nome": "SDBE", "ons": "3976", "codigo_neoenergia": "1105116"},
    "30234798000288": {"sigla": "SDBF", "nome": "SDBF", "ons": "3972", "codigo_neoenergia": "1105385"}
}

# Mapeamento de CNPJs de transmissoras para nomes
TRANSMISSORAS = {
    # "10338320000100": "AFLUENTE",  # Primeira transmissora catalogada
    # "17873542000171": "POTIGUAR",
    # "27848099000132": "ATIBAIA (EKTT 13)",
    # "27853556000187": "SOBRAL (EKTT 15)",
    # "27853497000147": "BIGUACU",
    # "10337920000153": "NARANDIBA",
    # "17079395000243":"CPFL-T",
    "31109417000110":"BORBOREMA",
    
}

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

def extrair_info_xml(caminho_arquivo):
    """Extrai informações do XML da NF-e"""
    try:
        # Registrar os namespaces
        namespaces = {
            'nfe': 'http://www.portalfiscal.inf.br/nfe'
        }
        
        # Analisar o XML
        tree = ET.parse(caminho_arquivo)
        root = tree.getroot()
        
        # Procurar elementos relevantes
        # Corrigindo os avisos de depreciação
        dest_element = root.find('.//nfe:dest', namespaces)
        if dest_element is None:
            dest_element = root.find('.//dest')
            
        emit_element = root.find('.//nfe:emit', namespaces)
        if emit_element is None:
            emit_element = root.find('.//emit')
        
        if dest_element is None or emit_element is None:
            print(f"Estrutura XML não reconhecida em: {caminho_arquivo}")
            return None, None, None, None, None
        
        # Extrair CNPJ do destinatário
        cnpj_dest_element = dest_element.find('.//nfe:CNPJ', namespaces)
        if cnpj_dest_element is None:
            cnpj_dest_element = dest_element.find('CNPJ')
        cnpj_dest = cnpj_dest_element.text if cnpj_dest_element is not None else None
        
        # Extrair nome do destinatário
        nome_dest_element = dest_element.find('.//nfe:xNome', namespaces)
        if nome_dest_element is None:
            nome_dest_element = dest_element.find('xNome')
        nome_dest = nome_dest_element.text if nome_dest_element is not None else None
        
        # Extrair CNPJ do emitente
        cnpj_emit_element = emit_element.find('.//nfe:CNPJ', namespaces)
        if cnpj_emit_element is None:
            cnpj_emit_element = emit_element.find('CNPJ')
        cnpj_emit = cnpj_emit_element.text if cnpj_emit_element is not None else None
        
        # Extrair nome do emitente
        nome_emit_element = emit_element.find('.//nfe:xNome', namespaces)
        if nome_emit_element is None:
            nome_emit_element = emit_element.find('xNome')
        nome_emit = nome_emit_element.text if nome_emit_element is not None else None
        
        # Extrair informações adicionais para identificar a Narandiba específica
        info_adicional = ""
        
        # Tentar encontrar informações no campo de descrição do produto
        produtos = root.findall('.//nfe:det', namespaces) or root.findall('.//det')
        if produtos:
            for produto in produtos:
                desc_element = produto.find('.//nfe:xProd', namespaces) or produto.find('.//xProd')
                if desc_element is not None and desc_element.text:
                    desc = desc_element.text
                    if "BRUMADO" in desc.upper():
                        info_adicional = "BRUMADO II"
                        break
                    elif "EXTREMOZ" in desc.upper():
                        info_adicional = "EXTREMOZ II"
                        break
        
        # Se não encontrou nas descrições, tentar no campo de informações complementares
        if not info_adicional:
            info_comp_element = root.find('.//nfe:infAdic/nfe:infCpl', namespaces) or root.find('.//infAdic/infCpl')
            if info_comp_element is not None and info_comp_element.text:
                info_comp = info_comp_element.text
                if "BRUMADO" in info_comp.upper():
                    info_adicional = "BRUMADO II"
                elif "EXTREMOZ" in info_comp.upper():
                    info_adicional = "EXTREMOZ II"
        
        print(f"Informações extraídas: Destinatário: {cnpj_dest} ({nome_dest}), Emitente: {cnpj_emit} ({nome_emit}), Info Adicional: {info_adicional}")
        return cnpj_dest, nome_dest, cnpj_emit, nome_emit, info_adicional
    
    except Exception as e:
        print(f"Erro ao analisar XML {caminho_arquivo}: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None, None, None, None

def processar_anexo_xml(caminho_original, nome_arquivo):
    """Processa um arquivo XML, extraindo informações e movendo para a pasta da transmissora"""
    # Extrair informações do XML
    cnpj_dest, nome_dest, cnpj_emit, nome_emit, info_adicional = extrair_info_xml(caminho_original)
    
    if cnpj_emit and cnpj_dest:
        # Determinar o nome da empresa destinatária para a pasta principal
        nome_empresa_pasta = "DESCONHECIDO"
        nome_empresa_arquivo = "DESCONHECIDO"
        
        # Verificar se o CNPJ do destinatário está no mapeamento de empresas
        if cnpj_dest in EMPRESAS:
            nome_empresa_pasta = EMPRESAS[cnpj_dest]["sigla"]
            nome_empresa_arquivo = nome_empresa_pasta
        # Se não estiver no mapeamento, usar o nome do destinatário
        elif nome_dest:
            # Extrair a primeira palavra ou usar abreviação do nome
            palavras = nome_dest.split()
            if palavras:
                nome_empresa_pasta = palavras[0]
                nome_empresa_arquivo = nome_empresa_pasta
                # Se for LIBRA LIGAS, usar LIBRA para pasta e LIBRAS para arquivo
                if nome_empresa_pasta.upper() == "RE":
                    nome_empresa_arquivo = "RE"
        
        # Verificar se é uma transmissora conhecida ou se contém "afluent" no nome
        nome_pasta_transmissora = None
        
        # Caso especial para Narandiba
        if cnpj_emit == "10337920000153":  # CNPJ da Narandiba
            if info_adicional == "BRUMADO II":
                nome_pasta_transmissora = "NARANDIBA (SE BRUMADO II)"
            elif info_adicional == "EXTREMOZ II":
                nome_pasta_transmissora = "NARANDIBA (SE EXTREMOZ II)"
            else:
                nome_pasta_transmissora = "NARANDIBA"
            print(f"Identificada transmissora Narandiba: {nome_pasta_transmissora}")
        # Verificar se o CNPJ está no dicionário de transmissoras
        elif cnpj_emit in TRANSMISSORAS:
            nome_pasta_transmissora = TRANSMISSORAS[cnpj_emit]
        # Verificar se o nome contém "afluent" (case insensitive)
        elif nome_emit and "afluent" in nome_emit.lower():
            nome_pasta_transmissora = "AFLUENTE"
            # Adicionar ao dicionário para uso futuro
            TRANSMISSORAS[cnpj_emit] = nome_pasta_transmissora
            print(f"Nova transmissora Afluente encontrada: {cnpj_emit} - {nome_emit}")
        else:
            # Para outras transmissoras, usar o nome do emitente como nome da pasta
            nome_pasta_transmissora = nome_emit.replace("/", "-").replace("\\", "-").strip()
            # Adicionar ao dicionário para uso futuro
            TRANSMISSORAS[cnpj_emit] = nome_pasta_transmissora
            print(f"Nova transmissora encontrada: {cnpj_emit} - {nome_emit}")
        
        # Criar pasta para a empresa se não existir
        pasta_empresa = os.path.join(PASTA_DESTINO_BASE, nome_empresa_pasta)
        if not os.path.exists(pasta_empresa):
            os.makedirs(pasta_empresa)
            print(f"Pasta criada para empresa: {pasta_empresa}")
        
        # Criar pasta para a transmissora dentro da pasta da empresa
        pasta_transmissora = os.path.join(pasta_empresa, nome_pasta_transmissora)
        if not os.path.exists(pasta_transmissora):
            os.makedirs(pasta_transmissora)
            print(f"Pasta criada para transmissora: {pasta_transmissora}")
        
        # Criar novo nome de arquivo com o nome da empresa destinatária
        _, extensao = os.path.splitext(nome_arquivo)
        novo_nome_arquivo = f"{nome_empresa_arquivo}{extensao}"
        
        # Caminho completo do novo arquivo
        novo_caminho = os.path.join(pasta_transmissora, novo_nome_arquivo)
        
        # Verificar se o arquivo já existe e adicionar sequencial se necessário
        if os.path.exists(novo_caminho):
            # Encontrar o próximo número sequencial disponível
            contador = 1
            while True:
                novo_nome_arquivo = f"{nome_empresa_arquivo}_{contador}{extensao}"
                novo_caminho = os.path.join(pasta_transmissora, novo_nome_arquivo)
                if not os.path.exists(novo_caminho):
                    break
                contador += 1
        
        try:
            # Mover arquivo
            os.rename(caminho_original, novo_caminho)
            print(f"Arquivo renomeado e movido para: {novo_caminho}")
            return novo_caminho
        except Exception as e:
            print(f"Erro ao mover arquivo: {str(e)}")
            # Tentar copiar e depois excluir
            import shutil
            try:
                shutil.copy2(caminho_original, novo_caminho)
                os.remove(caminho_original)
                print(f"Arquivo copiado para: {novo_caminho}")
                return novo_caminho
            except Exception as e2:
                print(f"Erro ao copiar arquivo: {str(e2)}")
                return caminho_original
    else:
        print(f"Não foi possível extrair informações do XML: {caminho_original}")
        # Mover para pasta de não processados
        pasta_nao_processados = os.path.join(PASTA_DESTINO_BASE, "NAO_PROCESSADOS")
        if not os.path.exists(pasta_nao_processados):
            os.makedirs(pasta_nao_processados)
        
        novo_caminho = os.path.join(pasta_nao_processados, os.path.basename(caminho_original))
        try:
            os.rename(caminho_original, novo_caminho)
            print(f"Arquivo movido para não processados: {novo_caminho}")
        except Exception as e:
            print(f"Erro ao mover arquivo para não processados: {str(e)}")
        
        return caminho_original

def processar_anexo_relacionado(caminho_original, nome_arquivo, caminho_xml):
    """Processa um arquivo relacionado (PDF, etc) movendo para a mesma pasta do XML"""
    if caminho_xml and caminho_xml != caminho_original:
        pasta_destino = os.path.dirname(caminho_xml)
        nome_base, extensao = os.path.splitext(nome_arquivo)
        
        # Usar o mesmo prefixo do XML
        prefixo = os.path.basename(caminho_xml).split('_')[0]
        novo_nome_arquivo = f"{prefixo}_{nome_base}{extensao}"
        
        novo_caminho = os.path.join(pasta_destino, novo_nome_arquivo)
        
        # Mover arquivo
        os.rename(caminho_original, novo_caminho)
        
        print(f"Arquivo relacionado movido para: {novo_caminho}")
        return novo_caminho
    
    return caminho_original

def baixar_anexos(conta_nome=None):
    """
    Baixa anexos XML de emails dos últimos 30 dias do remetente especificado.
    Se conta_nome for especificado, baixa apenas para essa conta.
    """
    # Criar pasta de destino base se não existir
    if not os.path.exists(PASTA_DESTINO_BASE):
        os.makedirs(PASTA_DESTINO_BASE)
    
    # Determinar quais contas processar
    contas_para_processar = {}
    if conta_nome and conta_nome in CONTAS_EMAIL:
        contas_para_processar[conta_nome] = CONTAS_EMAIL[conta_nome]
    else:
        contas_para_processar = CONTAS_EMAIL
    
    # Lista de CNPJs das transmissoras permitidas
    cnpjs_permitidos = list(TRANSMISSORAS.keys())
    
    # Processar cada conta
    for nome_conta, config_conta in contas_para_processar.items():
        email_conta = config_conta["email"]
        
        print(f"\n=== Processando conta: {nome_conta} ({email_conta}) ===")
        
        # Obter token OAuth2
        print("Obtendo token de autenticação OAuth2...")
        token = obter_token_oauth2()
        
        if not token:
            print("Falha ao obter token de autenticação.")
            continue
        
        try:
            # Conectar ao servidor IMAP
            print(f"Conectando ao servidor IMAP {IMAP_SERVER}...")
            imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
            
            # Autenticar com OAuth2
            auth_string = f'user={email_conta}\x01auth=Bearer {token}\x01\x01'
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
            contador_ignorados = 0
            
            print(f"Filtrando apenas transmissoras específicas: {', '.join(TRANSMISSORAS.values())}")
            
            # Processar cada mensagem
            for id_mensagem in ids_mensagens:
                contador_emails += 1
                
                # Buscar a mensagem completa
                status, dados = imap.fetch(id_mensagem, '(RFC822)')
                mensagem_raw = dados[0][1]
                mensagem = email.message_from_bytes(mensagem_raw)
                
                # Obter assunto e data
                assunto_header = decode_header(mensagem['Subject'])[0]
                assunto_bytes, charset = assunto_header[0], assunto_header[1]
                
                # Decodificar o assunto com o charset correto ou usar 'latin-1' como fallback
                if isinstance(assunto_bytes, bytes):
                    try:
                        if charset:
                            assunto = assunto_bytes.decode(charset)
                        else:
                            assunto = assunto_bytes.decode('utf-8')
                    except UnicodeDecodeError:
                        # Fallback para latin-1 que aceita qualquer byte
                        assunto = assunto_bytes.decode('latin-1')
                else:
                    assunto = assunto_bytes
                
                try:
                    data_recebimento = datetime.strptime(mensagem['Date'], "%a, %d %b %Y %H:%M:%S %z")
                except ValueError:
                    # Tentar formato alternativo se o padrão falhar
                    try:
                        data_recebimento = datetime.strptime(mensagem['Date'], "%a, %d %b %Y %H:%M:%S %Z")
                    except ValueError:
                        # Usar data atual como fallback
                        data_recebimento = datetime.now()
                
                print(f"Processando email: {assunto} ({data_recebimento.strftime('%Y-%m-%d')})")
                
                # Processar anexos - apenas XMLs
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
                        
                        # Verificar se é um arquivo XML
                        if not nome_arquivo.lower().endswith('.xml'):
                            continue  # Ignorar arquivos que não são XML
                        
                        # Criar caminho temporário para salvar o arquivo
                        caminho_temp = os.path.join(PASTA_DESTINO_BASE, "temp")
                        if not os.path.exists(caminho_temp):
                            os.makedirs(caminho_temp)
                        
                        caminho_arquivo = os.path.join(caminho_temp, nome_arquivo)
                        
                        # Verificar se arquivo já existe
                        if os.path.exists(caminho_arquivo):
                            nome_base, extensao = os.path.splitext(nome_arquivo)
                            data_formatada = data_recebimento.strftime("%Y-%m-%d")
                            caminho_arquivo = os.path.join(caminho_temp, f"{nome_base}_{data_formatada}{extensao}")
                        
                        # Salvar anexo temporariamente
                        with open(caminho_arquivo, 'wb') as arquivo:
                            arquivo.write(parte.get_payload(decode=True))
                        
                        # Extrair informações do XML para verificar se é de uma transmissora permitida
                        cnpj_dest, nome_dest, cnpj_emit, nome_emit, info_adicional = extrair_info_xml(caminho_arquivo)
                        
                        # Verificar se o CNPJ do destinatário corresponde a uma das empresas da conta atual
                        if True:  # Sempre processar para RE
                            # Verificar se o CNPJ do emitente está na lista de permitidos
                            if cnpj_emit in cnpjs_permitidos or (cnpj_emit and nome_emit and "afluent" in nome_emit.lower()):
                                contador_anexos += 1
                                print(f"Anexo XML de transmissora permitida para {nome_conta}: {nome_emit}")
                                
                                # Processar o XML
                                novo_caminho = processar_anexo_xml(caminho_arquivo, nome_arquivo)
                                print(f"XML processado: {novo_caminho}")
                            else:
                                # Remover arquivo temporário se não for de uma transmissora permitida
                                contador_ignorados += 1
                                print(f"Ignorando anexo de transmissora não catalogada: {nome_emit} ({cnpj_emit})")
                                try:
                                    os.remove(caminho_arquivo)
                                except Exception as e:
                                    print(f"Erro ao remover arquivo temporário: {str(e)}")
                        else:
                            # Remover arquivo temporário se não for para uma empresa desta conta
                            contador_ignorados += 1
                            print(f"Ignorando anexo para empresa não relacionada a esta conta: {nome_dest} ({cnpj_dest})")
                            try:
                                os.remove(caminho_arquivo)
                            except Exception as e:
                                print(f"Erro ao remover arquivo temporário: {str(e)}")
            
            print(f"Processamento da conta {nome_conta} concluído: {contador_emails} emails encontrados, {contador_anexos} XMLs salvos, {contador_ignorados} XMLs ignorados.")
            
            # Fechar conexão
            imap.close()
            imap.logout()
            
        except Exception as e:
            print(f"Erro durante o processamento da conta {nome_conta}: {str(e)}")
            import traceback
            traceback.print_exc()
    
    # Remover pasta temporária se estiver vazia
    caminho_temp = os.path.join(PASTA_DESTINO_BASE, "temp")
    if os.path.exists(caminho_temp) and not os.listdir(caminho_temp):
        os.rmdir(caminho_temp)

if __name__ == "__main__":
    try:
        print("Iniciando download de anexos do Outlook...")
        
        # Perguntar o remetente
        remetente_personalizado = input("Digite o email do remetente (ou pressione Enter para usar o padrão 'nfe@neoenergia.com'): ")
        
        if remetente_personalizado.strip():
            REMETENTE = remetente_personalizado.strip()
            print(f"Usando remetente personalizado: {REMETENTE}")
        else:
            print(f"Usando remetente padrão: {REMETENTE}")
        
        # Processando apenas a conta RE
        print("\nProcessando conta Rio Energy (RE)")
        baixar_anexos("RE")
            
        print("Download de anexos concluído com sucesso!")
    except Exception as e:
        print(f"Erro durante o processo: {str(e)}")
        import traceback
        traceback.print_exc()