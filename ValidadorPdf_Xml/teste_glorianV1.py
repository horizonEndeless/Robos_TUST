import os
import xml.etree.ElementTree as ET

# Solicita ao usuário o caminho da pasta onde estão os arquivos XML
pasta = input("Digite o caminho da pasta onde estão os arquivos XML: ")

# Verifica se a pasta existe
if not os.path.exists(pasta):
    print(f"A pasta {pasta} não existe!")
    exit()

# Registra o namespace
ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

# Dicionário para controlar contadores de valores duplicados
contadores = {}

# Percorre todos os arquivos na pasta
for arquivo in os.listdir(pasta):
    if arquivo.endswith('.xml'):
        caminho_completo = os.path.join(pasta, arquivo)
        
        try:
            # Lê o arquivo XML
            tree = ET.parse(caminho_completo)
            root = tree.getroot()
            
            # Procura o elemento vLiq usando o namespace correto
            vliq = None
            fat_elem = root.find('.//nfe:fat', ns)
            if fat_elem is not None:
                vliq_elem = fat_elem.find('nfe:vLiq', ns)
                if vliq_elem is not None:
                    vliq = vliq_elem.text
            
            if vliq:
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
                print(f"Arquivo renomeado: {arquivo} -> {novo_nome}")
            else:
                print(f"Valor vLiq não encontrado no arquivo: {arquivo}")
                
        except Exception as e:
            print(f"Erro ao processar o arquivo {arquivo}: {str(e)}")

print("Processamento concluído!")
