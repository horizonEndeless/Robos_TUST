import os
import xml.etree.ElementTree as ET
from pathlib import Path
import PyPDF2
import re
import shutil

def extrair_cnpj_do_pdf(arquivo):
    try:
        with open(arquivo, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            texto = ""
            for pagina in pdf_reader.pages:
                texto += pagina.extract_text()
            
            # Procura por padrões de CNPJ no texto
            padrao_cnpj = r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\d{14}'
            cnpjs_encontrados = re.findall(padrao_cnpj, texto)
            
            # Remove pontuação para comparação
            cnpjs_limpos = [''.join(filter(str.isdigit, cnpj)) for cnpj in cnpjs_encontrados]
            return cnpjs_limpos
    except Exception as e:
        print(f"Erro ao ler PDF {arquivo}: {str(e)}")
        return []

def renomear_e_organizar_arquivos(diretorio_base):
    # Dicionário de CNPJs e nomes das empresas
    empresas = {
        "40215231000137": "MEZ 5",
        "31231479000109": "MEZ 4",
        "33950678000194": "MEZ 1",
        "31231893000100": "MEZ 3",
        "36243890000100": "MEZ 2",
        # Você pode adicionar mais empresas aqui seguindo o mesmo formato
        # "CNPJ": "NOME_EMPRESA",
    }
    
    def processar_pasta(pasta_atual):
        print(f"\nProcessando pasta: {pasta_atual}")
        
        # Criar pastas MEZ dentro da pasta atual se não existirem
        for empresa in empresas.values():
            pasta_empresa = pasta_atual / empresa
            pasta_empresa.mkdir(exist_ok=True)
            print(f"Pasta criada/verificada: {pasta_empresa}")
        
        # Procura por arquivos XML e PDF na pasta atual
        for arquivo in pasta_atual.glob("*.*"):
            if arquivo.suffix.lower() not in ['.xml', '.pdf']:
                continue
                
            try:
                if arquivo.suffix.lower() == '.xml':
                    # Processamento de XML
                    tree = ET.parse(arquivo)
                    root = tree.getroot()
                    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
                    cnpj_emit = root.find('.//nfe:emit/nfe:CNPJ', ns).text
                    
                    # Se o CNPJ estiver no nosso dicionário de empresas
                    if cnpj_emit in empresas:
                        nome_empresa = empresas[cnpj_emit]
                        novo_nome = f"{nome_empresa}.xml"
                        pasta_destino = pasta_atual / nome_empresa
                        novo_caminho = pasta_destino / novo_nome
                        arquivo.rename(novo_caminho)
                        print(f"XML movido para: {pasta_destino}/{novo_nome}")
                        
                elif arquivo.suffix.lower() == '.pdf':
                    # Tenta encontrar CNPJs no PDF
                    cnpjs_encontrados = extrair_cnpj_do_pdf(arquivo)
                    
                    # Verifica se algum CNPJ encontrado corresponde às empresas
                    empresa_encontrada = False
                    for cnpj in cnpjs_encontrados:
                        if cnpj in empresas:
                            nome_empresa = empresas[cnpj]
                            novo_nome = f"{nome_empresa}.pdf"
                            pasta_destino = pasta_atual / nome_empresa
                            novo_caminho = pasta_destino / novo_nome
                            arquivo.rename(novo_caminho)
                            print(f"Boleto movido para: {pasta_destino}/{novo_nome}")
                            empresa_encontrada = True
                            break
                    
                    # Se não encontrou CNPJ, tenta pelo nome no arquivo
                    if not empresa_encontrada:
                        for cnpj, nome_empresa in empresas.items():
                            if nome_empresa in arquivo.name.upper() or f"MEZ{nome_empresa[-1]}" in arquivo.name.upper():
                                novo_nome = f"{nome_empresa}.pdf"
                                pasta_destino = pasta_atual / nome_empresa
                                novo_caminho = pasta_destino / novo_nome
                                arquivo.rename(novo_caminho)
                                print(f"Boleto movido para: {pasta_destino}/{novo_nome}")
                                break
                
            except Exception as e:
                print(f"Erro ao processar {arquivo}: {str(e)}")
    
    # Procura por todas as subpastas específicas (LIBRA, COR3, etc.)
    for pasta in Path(diretorio_base).iterdir():
        if pasta.is_dir():
            # Para cada subpasta (LIBRA, COR3, etc.), processa seus arquivos
            processar_pasta(pasta)

# Exemplo de uso
if __name__ == "__main__":
    diretorio = input("Digite o caminho da pasta principal (ex: C:\\Users\\Bruno\\Downloads\\MEZ\\AE): ")
    renomear_e_organizar_arquivos(diretorio)
