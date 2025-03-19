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

def criar_df_transmissoras():
    """Cria DataFrame com as informações das transmissoras"""
    dados_transmissoras = '''CNPJ	TRANSMISSORA
25022221000191	LITORAL_SUL
43076117000242	EDP_NORTE
27831352000498	ALIANCA
07779299000173	CELG LT ITUMBIARA
24944194000141	PARAGUACU
49537506000204	EDP_NORTE2'''
    
    import io
    df = pd.read_csv(io.StringIO(dados_transmissoras), sep='\t', dtype={'CNPJ': str})
    df['CNPJ'] = df['CNPJ'].str.replace(r'[^\d]', '', regex=True)
    # Limpa o nome da transmissora
    df['TRANSMISSORA'] = df['TRANSMISSORA'].str.strip().str.replace(' ', '_')
    return df

def extrair_info_xml(arquivo_xml):
    """Extrai informações do arquivo XML"""
    try:
        tree = ET.parse(arquivo_xml)
        root = tree.getroot()
        
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        dest_cnpj = root.find('.//nfe:dest/nfe:CNPJ', ns).text
        emit_cnpj = root.find('.//nfe:emit/nfe:CNPJ', ns).text
        
        return {
            'dest_cnpj': dest_cnpj,
            'emit_cnpj': emit_cnpj
        }
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

def extrair_info_danfe(caminho_pdf, df_empresas):
    """Extrai informações da DANFE PDF"""
    try:
        with pdfplumber.open(caminho_pdf) as pdf:
            texto = pdf.pages[0].extract_text()
            
            # Procura por CNPJs no formato específico da DANFE
            import re
            # Padrão mais específico para CNPJs formatados (XX.XXX.XXX/XXXX-XX)
            padrao_cnpj = r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}'
            cnpjs_encontrados = re.findall(padrao_cnpj, texto)
            
            if cnpjs_encontrados:
                for cnpj in cnpjs_encontrados:
                    cnpj_limpo = re.sub(r'[^\d]', '', cnpj)
                    if cnpj_limpo in df_empresas['CNPJ'].values:
                        return {'cnpj': cnpj_limpo}
            
            # Se não encontrar CNPJs formatados, procura por números puros
            if not cnpjs_encontrados:
                padrao_cnpj_numerico = r'\d{14}'
                cnpjs_encontrados = re.findall(padrao_cnpj_numerico, texto)
                for cnpj in cnpjs_encontrados:
                    if cnpj in df_empresas['CNPJ'].values:
                        return {'cnpj': cnpj}
            
            return None
            
    except Exception as e:
        print(f"Erro ao processar DANFE: {str(e)}")
        return None

def verificar_arquivos_empresa(pasta_entrada, empresa):
    """Verifica se todos os arquivos necessários existem para uma empresa"""
    arquivos_necessarios = [
        f"{empresa}.xml",
        f"{empresa}.pdf",
        f"{empresa}_DANFE.pdf"
    ]
    
    arquivos_encontrados = {}
    for arquivo in arquivos_necessarios:
        caminho = os.path.join(pasta_entrada, arquivo)
        existe = os.path.exists(caminho)
        arquivos_encontrados[arquivo] = existe
        if not existe:
            print(f"AVISO: Arquivo {arquivo} não encontrado")
    
    return all(arquivos_encontrados.values()), arquivos_encontrados

def verificar_transmissora(info_xml, df_transmissoras):
    """Verifica se a transmissora foi encontrada e retorna detalhes"""
    if not info_xml:
        print("ERRO: Não foi possível extrair informações do XML")
        return None, "XML inválido"
    
    if 'emit_cnpj' not in info_xml:
        print("ERRO: CNPJ do emitente não encontrado no XML")
        return None, "CNPJ emitente não encontrado"
    
    cnpj_match = df_transmissoras[df_transmissoras['CNPJ'] == info_xml['emit_cnpj']]
    if cnpj_match.empty:
        print(f"ERRO: CNPJ da transmissora {info_xml['emit_cnpj']} não encontrado na tabela")
        return None, "CNPJ não cadastrado"
    
    return cnpj_match.iloc[0]['TRANSMISSORA'], None

def verificar_arquivos_subpastas(pasta_entrada, df_empresas, df_transmissoras):
    """Verifica arquivos em subpastas e reorganiza se necessário"""
    print("\nVerificando arquivos em subpastas...")
    
    # Lista todas as DANFEs na pasta principal e subpastas
    danfes_encontradas = []
    for root, _, files in os.walk(pasta_entrada):
        for arquivo in files:
            if arquivo.endswith('.pdf') and not arquivo.lower().startswith('boleto-'):
                caminho_completo = os.path.join(root, arquivo)
                # Tenta extrair informações da DANFE
                info = extrair_info_danfe(caminho_completo, df_empresas)
                if info:
                    cnpj_match = df_empresas[df_empresas['CNPJ'] == info['cnpj']]
                    if not cnpj_match.empty:
                        empresa = cnpj_match.iloc[0]
                        novo_nome = f"{empresa['EMPRESA']}_DANFE.pdf"
                        empresa_codigo = empresa['EMPRESA']
                        
                        # Renomeia a DANFE se necessário
                        if os.path.basename(caminho_completo) != novo_nome:
                            try:
                                novo_caminho = os.path.join(os.path.dirname(caminho_completo), novo_nome)
                                os.rename(caminho_completo, novo_caminho)
                                print(f"✓ DANFE renomeada: {os.path.basename(caminho_completo)} -> {novo_nome}")
                                caminho_completo = novo_caminho
                            except Exception as e:
                                print(f"✗ Erro ao renomear DANFE: {str(e)}")
                        
                        danfes_encontradas.append((empresa_codigo, novo_nome, caminho_completo))
    
    print(f"\nEncontradas {len(danfes_encontradas)} DANFEs para processar")
    
    # Para cada DANFE, procura os arquivos correspondentes
    for empresa, danfe_nome, danfe_caminho in danfes_encontradas:
        print(f"\nProcessando empresa: {empresa}")
        
        # Procura XML e boleto em todas as subpastas
        xml_encontrado = None
        boleto_encontrado = None
        
        for root, _, files in os.walk(pasta_entrada):
            for arquivo in files:
                if arquivo == f"{empresa}.xml":
                    xml_encontrado = os.path.join(root, arquivo)
                elif arquivo == f"{empresa}.pdf" and not arquivo.endswith('_DANFE.pdf'):
                    boleto_encontrado = os.path.join(root, arquivo)
        
        # Se encontrou XML, usa ele para determinar a pasta correta
        if xml_encontrado:
            info_xml = extrair_info_xml(xml_encontrado)
            if info_xml:
                transmissora, erro = verificar_transmissora(info_xml, df_transmissoras)
                if transmissora:
                    # Verifica se a DANFE ainda existe no local original
                    if os.path.exists(danfe_caminho):
                        pasta_destino = os.path.join(pasta_entrada, transmissora, empresa)
                        print(f"✓ Pasta destino determinada via XML: {transmissora}/{empresa}")
                        
                        # Cria a pasta se não existir
                        if not os.path.exists(pasta_destino):
                            os.makedirs(pasta_destino)
                            print(f"✓ Pasta criada: {transmissora}/{empresa}")
                        
                        # Move a DANFE se não estiver na pasta correta
                        if os.path.dirname(danfe_caminho) != pasta_destino:
                            try:
                                novo_caminho_danfe = os.path.join(pasta_destino, danfe_nome)
                                shutil.move(danfe_caminho, novo_caminho_danfe)
                                print(f"✓ DANFE movida para: {transmissora}/{empresa}/")
                                danfe_caminho = novo_caminho_danfe  # Atualiza o caminho após mover
                            except Exception as e:
                                print(f"✗ Erro ao mover DANFE: {str(e)}")
                        else:
                            print("✓ DANFE já está na pasta correta")
                    else:
                        print(f"✗ DANFE não encontrada em: {danfe_caminho}")
                else:
                    print(f"✗ Não foi possível identificar a transmissora para {empresa}")
            else:
                print(f"✗ Não foi possível extrair informações do XML para {empresa}")
        else:
            print(f"✗ XML não encontrado para {empresa}")
        
        # Status dos arquivos
        print("\nStatus dos arquivos:")
        print(f"XML: {'✓ Encontrado em ' + os.path.dirname(xml_encontrado) if xml_encontrado else '✗ Não encontrado'}")
        print(f"Boleto: {'✓ Encontrado em ' + os.path.dirname(boleto_encontrado) if boleto_encontrado else '✗ Não encontrado'}")
        print(f"DANFE: {'✓ Encontrado em ' + os.path.dirname(danfe_caminho) if os.path.exists(danfe_caminho) else '✗ Não encontrado'}")

    print("\nVerificação de subpastas concluída!")

def processar_arquivos(pasta_entrada):
    """Processa todos os arquivos e organiza em pastas"""
    print("\nIniciando processamento de arquivos...")
    
    # Carrega tabelas
    print("Carregando tabelas...")
    df_empresas = criar_df_empresas()
    df_transmissoras = criar_df_transmissoras()
    print(f"Tabelas carregadas: {len(df_empresas)} empresas e {len(df_transmissoras)} transmissoras")
    
    # Verifica e organiza os arquivos
    verificar_arquivos_subpastas(pasta_entrada, df_empresas, df_transmissoras)
    
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
