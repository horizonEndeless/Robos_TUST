import os
import requests
import email
import imaplib
import xml.etree.ElementTree as ET
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
PASTA_DESTINO_BASE = r"C:\Users\Bruno\Downloads\TUST\ANEXOS OUTLOOK"

# Mapeamento de CNPJs para siglas de empresas
EMPRESAS = {
    "10500221000182": {"sigla": "LIBRA", "nome": "LIBRA LIGAS DO BRASIL S/A"},
    "30520122000170": {"sigla": "SJP1", "nome": "CELEO SAO JOAO DO PIAUI FV I S.A."},
    "30432072000179": {"sigla": "SJP2", "nome": "CELEO SAO JOAO DO PIAUI FV II S.A."},
    "30486042000145": {"sigla": "SJP3", "nome": "CELEO SAO JOAO DO PIAUI FV III S.A."},
    "30425445000184": {"sigla": "SJP4", "nome": "CELEO SAO JOAO DO PIAUI FV IV S.A."},
    "30456405000108": {"sigla": "SJP5", "nome": "CELEO SAO JOAO DO PIAUI FV V S.A."},
    "30421756000175": {"sigla": "SJP6", "nome": "CELEO SAO JOAO DO PIAUI FV VI S.A."},
    "14285232000148": {"sigla": "COR1", "nome": "COREMAS I GERAÇÃO DE ENERGIA SPE S.A."},
    "14285242000183": {"sigla": "COR2", "nome": "COREMAS II GERACAO DE ENERGIA II SPE S.A."},
    "24342513000149": {"sigla": "COR3", "nome": "COREMAS III GERAÇÃO DE ENERGIA SPE S.A."}
}

# Mapeamento de CNPJs de transmissoras para nomes
TRANSMISSORAS = {
    "10338320000100": "AFLUENTE",  # Primeira transmissora catalogada
    "17873542000171": "POTIGUAR",
    "27848099000132": "ATIBAIA (EKTT 13)",
    "27853556000187": "SOBRAL (EKTT 15)",
    "27853497000147": "BIGUACU",
    "10337920000153": "NARANDIBA",
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
                if nome_empresa_pasta.upper() == "LIBRA":
                    nome_empresa_arquivo = "LIBRAS"
        
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

def baixar_anexos():
    """Baixa apenas anexos XML de emails dos últimos 30 dias do remetente especificado e de transmissoras específicas"""
    # Criar pasta de destino base se não existir
    if not os.path.exists(PASTA_DESTINO_BASE):
        os.makedirs(PASTA_DESTINO_BASE)
    
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
        contador_ignorados = 0
        
        # Lista de CNPJs das transmissoras permitidas
        cnpjs_permitidos = list(TRANSMISSORAS.keys())
        print(f"Filtrando apenas transmissoras específicas: {', '.join(TRANSMISSORAS.values())}")
        
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
                    
                    # Verificar se o CNPJ do emitente está na lista de permitidos
                    if cnpj_emit in cnpjs_permitidos or (cnpj_emit and nome_emit and "afluent" in nome_emit.lower()):
                        contador_anexos += 1
                        print(f"Anexo XML de transmissora permitida: {nome_emit}")
                        
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
        
        print(f"Processamento concluído: {contador_emails} emails encontrados, {contador_anexos} XMLs salvos, {contador_ignorados} XMLs ignorados.")
        
        # Remover pasta temporária se estiver vazia
        caminho_temp = os.path.join(PASTA_DESTINO_BASE, "temp")
        if os.path.exists(caminho_temp) and not os.listdir(caminho_temp):
            os.rmdir(caminho_temp)
        
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