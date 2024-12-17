import os
import xml.etree.ElementTree as ET
import pandas as pd
import pdfplumber
import shutil

def criar_df_empresas():
    """Cria DataFrame com as informações das empresas"""
    dados = '''CNPJ	ONS	Código Neoenergia	EMPRESA	Usuárias
33485728000100	4313	1108376	BRJA	EÓLICA BREJINHOS ALFA S.A
33485874000135	4314	1108377	BRJB	EÓLICA BREJINHOS B S.A.
19233858000205	3430	1101532	CECA	EOL CAETITÉ A
19235607000260	3431	1101533	CECB	EOL CAETITÉ B
19560109000292	3432	1101534	CECC	EOL CAETITÉ C
33457932000117	4415	1108935	CECD	EOL CAETITÉ D
33471379000177	4315	1108378	CECE	EÓLICA CAETITÉ ECO S.A
33468809000100	4316	1108379	CECF	EÓLICA CAETITÉ F S.A.
19560032000250	3502	1101690	ITA1	EOL ITAREMA I
19560074000291	3497	1101632	ITA2	EOL ITAREMA II
19560839000293	3503	1101691	ITA3	EOL ITAREMA III
20553751000223	3530	1101738	ITA4	EOL ITAREMA IV
19560868000255	3498	1101633	ITA5	EOL ITAREMA V
20533879000225	3531	1101739	ITA6	EOL ITAREMA VI
20533473000242	3532	1101740	ITA7	EOL ITAREMA VII
20533310000260	3537	1101754	ITA8	EOL ITAREMA VIII
20533377000202	3538	1101755	ITA9	EOL ITAREMA IX
30063842000234	3947	1105036	SDBA	EOL SERRA DA BABILÔNIA A
29527877000206	3948	1105037	SDBB	EOL SERRA DA BABILÔNIA B
29591504000296	3969	1105267	SDBC	EOL SERRA DA BABILÔNIA C
30062725000256	3970	1105268	SDBD	EOL SERRA DA BABILÔNIA D
30062736000236	3976	1105116	SDBE	EOL SERRA DA BABILÔNIA E
30234798000288	3972	1105385	SDBF	EOL SERRA DA BABILÔNIA F
30520122000170	-	-	SJP1	CELEO SAO JOAO DO PIAUI FV I S.A.
30432072000179	-	-	SJP2	CELEO SAO JOAO DO PIAUI FV II S.A.
30486042000145	-	-	SJP3	CELEO SAO JOAO DO PIAUI FV III S.A.
30425445000184	-	-	SJP4	CELEO SAO JOAO DO PIAUI FV IV S.A.
30456405000108	-	-	SJP5	CELEO SAO JOAO DO PIAUI FV V S.A.
30421756000175	-	-	SJP6	CELEO SAO JOAO DO PIAUI FV VI S.A.
14285232000148	-	-	COR1	COREMAS I GERAÇÃO DE ENERGIA SPE S.A.
14285242000183	-	-	COR2	COREMAS II GERACAO DE ENERGIA II SPE S.A.
24342513000149	-	-	COR3	COREMAS III GERAÇÃO DE ENERGIA SPE S.A.
10500221000182	-	-	LIBRA	LIBRA LIGAS DO BRASIL S/A
27093977000238	-	-	DE	DE DIAMANTE GERAÇÃO DE ENERGIA LTDA'''
    
    import io
    df = pd.read_csv(io.StringIO(dados), sep='\t', dtype={'CNPJ': str})
    df['CNPJ'] = df['CNPJ'].str.replace(r'[^\d]', '', regex=True)
    return df

def extrair_info_xml(arquivo_xml):
    """Extrai informações do arquivo XML"""
    try:
        tree = ET.parse(arquivo_xml)
        root = tree.getroot()
        
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        dest_cnpj = root.find('.//nfe:dest/nfe:CNPJ', ns).text
        
        return {'dest_cnpj': dest_cnpj}
    except Exception as e:
        print(f"Erro ao processar XML: {str(e)}")
        return None

def extrair_info_boleto(caminho_pdf, df_empresas):
    """Extrai informações do boleto PDF"""
    try:
        with pdfplumber.open(caminho_pdf) as pdf:
            texto = pdf.pages[0].extract_text()
            
            import re
            padrao_cnpj = r'(?:\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\d{14})'
            cnpjs_encontrados = re.findall(padrao_cnpj, texto)
            
            if cnpjs_encontrados:
                for cnpj in cnpjs_encontrados:
                    cnpj_limpo = re.sub(r'[^\d]', '', cnpj)
                    if cnpj_limpo in df_empresas['CNPJ'].values:
                        return {'cnpj': cnpj_limpo}
            return None
            
    except Exception as e:
        print(f"Erro ao processar PDF: {str(e)}")
        return None

def processar_arquivos(pasta_entrada):
    """Processa todos os arquivos e organiza em pastas"""
    print("\nIniciando processamento de arquivos...")
    
    # Carrega tabela de empresas
    print("Carregando tabela de empresas...")
    df_empresas = criar_df_empresas()
    print(f"Tabela carregada com {len(df_empresas)} empresas")
    
    # Processa XMLs
    print("\nProcessando arquivos XML...")
    xmls = [f for f in os.listdir(pasta_entrada) if f.endswith('.xml')]
    for arquivo in xmls:
        print(f"\nProcessando XML: {arquivo}")
        caminho_completo = os.path.join(pasta_entrada, arquivo)
        info = extrair_info_xml(caminho_completo)
        
        if info:
            cnpj_match = df_empresas[df_empresas['CNPJ'] == info['dest_cnpj']]
            if not cnpj_match.empty:
                empresa = cnpj_match.iloc[0]
                novo_nome = f"{empresa['EMPRESA']}.xml"
                novo_caminho = os.path.join(pasta_entrada, novo_nome)
                try:
                    os.rename(caminho_completo, novo_caminho)
                    print(f"XML renomeado para: {novo_nome}")
                except Exception as e:
                    print(f"Erro ao renomear XML: {str(e)}")
    
    # Processa PDFs
    print("\nProcessando arquivos PDF...")
    pdfs = [f for f in os.listdir(pasta_entrada) 
            if f.endswith('.pdf') and f.lower().startswith('boleto-')]
    for arquivo in pdfs:
        print(f"\nProcessando PDF: {arquivo}")
        caminho_completo = os.path.join(pasta_entrada, arquivo)
        info = extrair_info_boleto(caminho_completo, df_empresas)
        
        if info:
            cnpj_match = df_empresas[df_empresas['CNPJ'] == info['cnpj']]
            if not cnpj_match.empty:
                empresa = cnpj_match.iloc[0]
                novo_nome = f"{empresa['EMPRESA']}.pdf"
                novo_caminho = os.path.join(pasta_entrada, novo_nome)
                try:
                    os.rename(caminho_completo, novo_caminho)
                    print(f"PDF renomeado para: {novo_nome}")
                except Exception as e:
                    print(f"Erro ao renomear PDF: {str(e)}")
    
    # Consolida arquivos em pastas
    print("\nConsolidando arquivos em pastas...")
    arquivos = os.listdir(pasta_entrada)
    empresas_xml = [os.path.splitext(f)[0] for f in arquivos if f.endswith('.xml')]
    empresas_pdf = [os.path.splitext(f)[0] for f in arquivos if f.endswith('.pdf')]
    
    empresas_completas = set(empresas_xml) & set(empresas_pdf)
    print(f"Encontradas {len(empresas_completas)} empresas com ambos os documentos")
    
    for empresa in empresas_completas:
        print(f"\nOrganizando arquivos da empresa: {empresa}")
        pasta_empresa = os.path.join(pasta_entrada, empresa)
        
        if not os.path.exists(pasta_empresa):
            os.makedirs(pasta_empresa)
        
        # Move XML e PDF
        for ext in ['.xml', '.pdf']:
            origem = os.path.join(pasta_entrada, f"{empresa}{ext}")
            destino = os.path.join(pasta_empresa, f"{empresa}{ext}")
            try:
                shutil.move(origem, destino)
                print(f"Arquivo {ext} movido com sucesso")
            except Exception as e:
                print(f"Erro ao mover arquivo {ext}: {str(e)}")
    
    print("\nProcessamento concluído!")

def main():
    print("Iniciando programa de validação e organização de arquivos")
    pasta_entrada = input("Digite o caminho da pasta com os arquivos: ")
    
    if not os.path.exists(pasta_entrada):
        print("Erro: Pasta não encontrada!")
        return
    
    processar_arquivos(pasta_entrada)

if __name__ == "__main__":
    main()
