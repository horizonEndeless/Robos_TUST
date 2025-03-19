import os
import xml.etree.ElementTree as ET
import logging
import traceback
from datetime import datetime

# Pasta onde estão os arquivos XML
pasta = r"C:\Users\Bruno\Downloads\CPFL 0225\CPFL0225Copia"

# Adiciona log para verificar a pasta
print(f"Verificando pasta: {pasta}")
logging.info(f"Verificando pasta: {pasta}")

# Verifica se a pasta existe
if not os.path.exists(pasta):
    msg = f"A pasta {pasta} não existe!"
    print(msg)
    logging.error(msg)
    exit()

# Lista todos os arquivos na pasta
arquivos = os.listdir(pasta)
print(f"Total de arquivos na pasta: {len(arquivos)}")

# Mostra as extensões únicas encontradas
extensoes = set(os.path.splitext(f)[1].lower() for f in arquivos)
print("Extensões encontradas:", extensoes)

# Mostra alguns exemplos de nomes de arquivos
print("Exemplos de arquivos:", arquivos[:5])

# Registra o namespace
ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

# Dicionário para controlar contadores de valores duplicados
contadores = {}

# Configuração do logging
log_filename = f"log_processamento_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Percorre todos os arquivos na pasta
total_arquivos = 0
arquivos_processados = 0

for arquivo in os.listdir(pasta):
    if arquivo.lower().endswith('.xml'):
        total_arquivos += 1
        caminho_completo = os.path.join(pasta, arquivo)
        
        try:
            # Lê o arquivo XML
            tree = ET.parse(caminho_completo)
            root = tree.getroot()
            
            # Procura o elemento vLiq usando o namespace correto
            vliq = None
            fat_elem = root.find('.//nfe:NFe/nfe:infNFe/nfe:cobr/nfe:fat', ns)
            if fat_elem is not None:
                vliq_elem = fat_elem.find('nfe:vLiq', ns)
                if vliq_elem is not None:
                    vliq = vliq_elem.text
                    logging.info(f"Valor vLiq encontrado no arquivo {arquivo}: {vliq}")
                else:
                    logging.warning(f"Elemento vLiq não encontrado dentro de fat no arquivo {arquivo}")
            else:
                logging.warning(f"Elemento fat não encontrado no arquivo {arquivo}")
            
            if vliq:
                arquivos_processados += 1
                # Verifica se já existe um arquivo com este valor
                if vliq in contadores:
                    contadores[vliq] += 1
                    novo_nome = f"{vliq}_{contadores[vliq]}.xml"
                else:
                    contadores[vliq] = 1
                    novo_nome = f"{vliq}.xml"
                
                novo_caminho = os.path.join(pasta, novo_nome)
                
                # Renomeia o arquivo
                os.rename(caminho_completo, novo_caminho)
                logging.info(f"Arquivo renomeado com sucesso: {arquivo} -> {novo_nome}")
            else:
                logging.warning(f"Valor vLiq não encontrado no arquivo: {arquivo}")
                
        except ET.ParseError as e:
            erro_msg = f"Erro de parsing XML no arquivo {arquivo}: {str(e)}"
            print(erro_msg)
            logging.error(erro_msg)
            logging.error(traceback.format_exc())
        except PermissionError as e:
            erro_msg = f"Erro de permissão ao acessar o arquivo {arquivo}: {str(e)}"
            print(erro_msg)
            logging.error(erro_msg)
            logging.error(traceback.format_exc())
        except Exception as e:
            erro_msg = f"Erro inesperado ao processar o arquivo {arquivo}: {str(e)}"
            print(erro_msg)
            logging.error(erro_msg)
            logging.error(traceback.format_exc())

msg_final = f"Processamento concluído! Total de arquivos XML: {total_arquivos}, Processados com sucesso: {arquivos_processados}"
print(msg_final)
logging.info(msg_final)
