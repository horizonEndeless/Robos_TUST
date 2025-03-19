from playwright.sync_api import sync_playwright
import time
import logging
from datetime import datetime
import os

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S'
)

# Adicione no início do arquivo, após as importações
EMPRESAS = [
    {"cnpj": "33485728000100", "nome": "BRJA"},
    {"cnpj": "33485874000135", "nome": "BRJB"},
    {"cnpj": "19233858000205", "nome": "CECA"},
    {"cnpj": "19235607000260", "nome": "CECB"},
    {"cnpj": "19560109000292", "nome": "CECC"},
    {"cnpj": "33457932000117", "nome": "CECD"},
    {"cnpj": "33471379000177", "nome": "CECE"},
    {"cnpj": "33468809000100", "nome": "CECF"},
    {"cnpj": "19560032000250", "nome": "ITA1"},
    {"cnpj": "19560074000291", "nome": "ITA2"},
    {"cnpj": "19560839000293", "nome": "ITA3"},
    {"cnpj": "20553751000223", "nome": "ITA4"},
    {"cnpj": "19560868000255", "nome": "ITA5"},
    {"cnpj": "20533879000225", "nome": "ITA6"},
    {"cnpj": "20533473000242", "nome": "ITA7"},
    {"cnpj": "20533310000260", "nome": "ITA8"},
    {"cnpj": "20533377000202", "nome": "ITA9"},
    {"cnpj": "30063842000234", "nome": "SDBA"},
    {"cnpj": "29527877000206", "nome": "SDBB"},
    {"cnpj": "29591504000296", "nome": "SDBC"},
    {"cnpj": "30062725000256", "nome": "SDBD"},
    {"cnpj": "30062736000236", "nome": "SDBE"},
    {"cnpj": "30234798000288", "nome": "SDBF"}
]

def expandir_subpastas(page, node_number):
    """
    Expande todas as subpastas de faturas dentro do mês selecionado
    """
    try:
        # Aguarda as subpastas carregarem
        time.sleep(2)
        
        # Localiza todas as subpastas (faturas) do mês
        subpastas = page.locator(f'#form\\:tree-d-{node_number} a[id^="form:tree"]')
        quantidade = subpastas.count()
        
        if quantidade > 0:
            logging.info(f"Encontradas {quantidade} faturas para expandir")
            
            # Para cada subpasta encontrada
            for i in range(quantidade):
                # Constrói o seletor para cada subpasta
                sub_selector = f"#form\\:tree\\:{node_number}-{i}"
                subpasta = page.locator(sub_selector)
                
                if subpasta.is_visible():
                    logging.info(f"Expandindo fatura {i+1} de {quantidade}")
                    subpasta.click()
                    time.sleep(1)  # Pequena pausa entre cliques
        else:
            logging.warning("Nenhuma subpasta encontrada para expandir")
            
    except Exception as e:
        logging.error(f"Erro ao expandir subpastas: {str(e)}")
        raise

def get_data_desejada(mes=None, ano=None):
    """
    Retorna a data no formato correto (MM/YYYY)
    Se não fornecido, usa o mês e ano atual
    """
    if mes is None or ano is None:
        data_atual = datetime.now()
        mes = mes or data_atual.month
        ano = ano or data_atual.year
    
    return f"{mes:02d}/{ano}"

def criar_estrutura_pastas(mes, ano, empresa, numero_fatura):
    """
    Cria a estrutura de pastas por empresa
    """
    base_path = os.path.join(os.path.expanduser("~"), "Downloads","TUST", "CPFL", f"{mes:02d}_{ano}", empresa, f"NF_{numero_fatura}")
    
    # Cria a pasta se não existir
    if not os.path.exists(base_path):
        os.makedirs(base_path)
        logging.info(f"Pasta criada: {base_path}")
    
    return base_path

def baixar_documentos(page, node_number, mes, ano, empresa_nome):
    """
    Baixa os XMLs e PDFs de todas as notas fiscais do mês para uma empresa específica
    """
    try:
        time.sleep(2)
        
        mapeamento_empresas = {
            "BRJA": "CEEE T",
            "BRJB": "CEEE T",
            "CECA": "CEEE T",
            "CECB": "CEEE T",
            "CECC": "CEEE T",
            "CECD": "CEEE T",
            "CECE": "CEEE T",
            "CECF": "CEEE T",
            "ITA1": "CEEE T",
            "ITA2": "CEEE T",
            "ITA3": "CEEE T",
            "ITA4": "CEEE T",
            "ITA5": "CEEE T",
            "ITA6": "CEEE T",
            "ITA7": "CEEE T",
            "ITA8": "CEEE T",
            "ITA9": "CEEE T",
            "SDBA": "CEEE T",
            "SDBB": "CEEE T",
            "SDBC": "CEEE T",
            "SDBD": "CEEE T",
            "SDBE": "CEEE T",
            "SDBF": "CEEE T",
            # ... adicione outras empresas conforme necessário
        }
        
        nome_fatura = mapeamento_empresas.get(empresa_nome, empresa_nome)
        faturas = page.locator(f'text={nome_fatura} - Fatura')
        quantidade = faturas.count()
        
        if quantidade > 0:
            logging.info(f"Encontradas {quantidade} faturas para {empresa_nome}")
            
            for i in range(quantidade):
                try:
                    # Primeiro clica na fatura para expandir
                    fatura = faturas.nth(i)
                    texto_fatura = fatura.inner_text()
                    numero_fatura = texto_fatura.split('Nº: ')[1].split(' -')[0].strip()
                    
                    # Cria pasta específica para esta fatura
                    pasta_fatura = criar_estrutura_pastas(mes, ano, empresa_nome, numero_fatura)
                    
                    # Clica na fatura para expandir
                    fatura_selector = f'span[class="iceOutTxt"][id="form:tree:n-0-{i}:TreeNode"]'
                    fatura_element = page.locator(fatura_selector)
                    if fatura_element.is_visible():
                        logging.info(f"Clicando na fatura {numero_fatura} para expandir")
                        fatura_element.click()
                        time.sleep(2)
                    
                    # Agora tenta baixar o PDF
                    pdf_icon = page.locator('img[src*="pdf_ico.png"]').last
                    if pdf_icon.is_visible():
                        logging.info(f"PDF icon encontrado para fatura {numero_fatura}")
                        with page.expect_download() as download_info:
                            pdf_icon.click()
                        download = download_info.value
                        nome_arquivo_pdf = f"NF_{numero_fatura}.pdf"
                        caminho_pdf = os.path.join(pasta_fatura, nome_arquivo_pdf)
                        download.save_as(caminho_pdf)
                        logging.info(f"PDF salvo em: {caminho_pdf}")
                        time.sleep(1)
                    else:
                        logging.warning(f"Ícone PDF não encontrado para fatura {numero_fatura} após expandir")
                    
                    # Download do XML
                    nota_fiscal = page.locator(f'text=Nota Fiscal Modelo').nth(i)
                    if nota_fiscal.is_visible():
                        nota_fiscal.click()
                        time.sleep(2)
                        
                        xml_icon = page.locator('img[src*="xml"]').last
                        if xml_icon.is_visible():
                            with page.expect_download() as download_info:
                                xml_icon.click()
                            download = download_info.value
                            nome_arquivo_xml = f"NF_{numero_fatura}.xml"
                            caminho_xml = os.path.join(pasta_fatura, nome_arquivo_xml)
                            download.save_as(caminho_xml)
                            logging.info(f"XML salvo em: {caminho_xml}")
                            time.sleep(1)
                    
                    time.sleep(2)
                        
                except Exception as e:
                    logging.error(f"Erro ao processar fatura {i+1} da empresa {empresa_nome}: {str(e)}")
                    continue
        else:
            logging.warning(f"Nenhuma fatura encontrada para a empresa {empresa_nome}")
            
    except Exception as e:
        logging.error(f"Erro ao baixar documentos da empresa {empresa_nome}: {str(e)}")
        raise

def encontrar_mes_mais_recente(page):
    """
    Encontra o mês mais recente disponível na plataforma
    Retorna uma tupla (mes, ano) do mês mais recente
    """
    try:
        logging.info("Procurando o mês mais recente disponível...")
        
        # Espera que a árvore de documentos seja carregada
        page.wait_for_selector('.iceTree', timeout=60000)
        
        # Localiza todos os elementos de data na árvore
        data_elements = page.locator("span.iceOutTxt:has-text('/')")
        count = data_elements.count()
        
        if count == 0:
            logging.warning("Nenhuma data encontrada na árvore de documentos")
            return None, None
        
        datas = []
        for i in range(count):
            texto = data_elements.nth(i).inner_text().strip()
            # Verifica se o texto corresponde ao formato MM/YYYY
            if len(texto) == 7 and '/' in texto:
                try:
                    mes, ano = texto.split('/')
                    mes = int(mes)
                    ano = int(ano)
                    datas.append((mes, ano))
                except ValueError:
                    continue
        
        if not datas:
            logging.warning("Nenhuma data válida encontrada")
            return None, None
        
        # Ordena as datas e pega a mais recente
        datas.sort(key=lambda x: (x[1], x[0]), reverse=True)
        mes_recente, ano_recente = datas[0]
        
        logging.info(f"Mês mais recente encontrado: {mes_recente:02d}/{ano_recente}")
        return mes_recente, ano_recente
        
    except Exception as e:
        logging.error(f"Erro ao buscar mês mais recente: {str(e)}")
        return None, None

def login_cpfl(cnpj: str, senha: str, mes=None, ano=None, usar_mes_recente=False):
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            logging.info("Iniciando o navegador...")
            logging.info("Acessando a página da CPFL...")
            
            # Aumentando timeout geral da página
            page.set_default_timeout(120000)  # 120 segundos
            
            page.goto('https://getweb.cpfl.com.br/getweb/getweb.jsf')
            
            # Preenche login
            campo_cnpj = page.locator('#form\\:documento')
            if campo_cnpj.is_visible():
                logging.info("Campo CNPJ encontrado com sucesso")
                campo_cnpj.fill(cnpj)
            
            campo_senha = page.locator('#form\\:senha')
            if campo_senha.is_visible():
                logging.info("Campo senha encontrado com sucesso")
                campo_senha.fill(senha)
            
            botao_login = page.locator('#form\\:j_idt22')
            if botao_login.is_visible():
                logging.info("Botão de login encontrado com sucesso")
                botao_login.click()

            # Nova lógica de espera baseada na estrutura real do HTML
            logging.info("Aguardando carregamento da página de faturas...")
            try:
                # Espera pela árvore de documentos
                page.wait_for_selector('.iceTree', timeout=60000)
                # Espera adicional pela div container
                page.wait_for_selector('.container', timeout=60000)
                # Espera pelo título da página
                page.wait_for_selector('.tituloPagina', timeout=60000)
                
                logging.info("Elementos principais da página encontrados")
                time.sleep(5)  # Pausa extra para garantir carregamento completo
                
            except Exception as e:
                logging.error(f"Erro ao aguardar elementos da página: {str(e)}")
                raise

            # Se usar_mes_recente for True, busca o mês mais recente
            if usar_mes_recente:
                mes, ano = encontrar_mes_mais_recente(page)
                if mes is None or ano is None:
                    logging.warning("Não foi possível encontrar o mês mais recente. Usando valores padrão.")
                    data_atual = datetime.now()
                    mes = mes or data_atual.month
                    ano = ano or data_atual.year

            # Formata a data desejada
            data_desejada = get_data_desejada(mes, ano)
            logging.info(f"Procurando a pasta do mês {data_desejada}...")

            # Localiza e clica na pasta
            selector = f"span.iceOutTxt:has-text('{data_desejada}')"
            data_element = page.locator(selector)
            
            if data_element.count() > 0:
                tree_node_id = data_element.first.evaluate("""el => {
                    const treeRow = el.closest('.iceTreeRow');
                    return treeRow ? treeRow.id : null;
                }""")
                
                if tree_node_id:
                    node_number = tree_node_id.split('-')[-1]
                    expand_selector = f"#form\\:tree\\:{node_number}"
                    
                    logging.info(f"Encontrou pasta {data_desejada} com ID {expand_selector}")
                    
                    expand_button = page.locator(expand_selector)
                    if expand_button.is_visible():
                        logging.info(f"Clicando na pasta {data_desejada}")
                        expand_button.click()
                        time.sleep(2)
                        
                        # Expande as subpastas
                        expandir_subpastas(page, node_number)
                        
                        # Baixa XMLs e PDFs organizados por empresa
                        empresa = next((emp['nome'] for emp in EMPRESAS if emp['cnpj'] == cnpj), "")
                        baixar_documentos(page, node_number, mes, ano, empresa)
            else:
                logging.warning(f"Pasta do mês {data_desejada} não encontrada")

            time.sleep(5)  # Tempo para visualização
            browser.close()

        except Exception as e:
            logging.error(f"Erro durante a execução: {str(e)}")
            raise
        finally:
            if 'browser' in locals():
                browser.close()

def processar_todas_empresas(mes=None, ano=None, usar_mes_recente=True):
    """
    Processa todas as empresas da lista
    Se mes e ano forem None e usar_mes_recente for True, 
    busca o mês mais recente disponível para cada empresa
    """
    for empresa in EMPRESAS:
        try:
            logging.info(f"Iniciando processamento da empresa {empresa['nome']} - CNPJ: {empresa['cnpj']}")
            login_cpfl(empresa['cnpj'], "Pontal!rsm24", mes, ano, usar_mes_recente)
            logging.info(f"Processamento da empresa {empresa['nome']} finalizado com sucesso!")
            time.sleep(10)  # Aumentando pausa entre empresas
            
        except Exception as e:
            logging.error(f"Erro ao processar empresa {empresa['nome']}: {str(e)}")
            continue

if __name__ == "__main__":
    # CONFIGURAÇÃO CENTRAL - Defina aqui suas preferências
    # Opção 1: Baixar mês específico (defina valores para MES_DESEJADO e ANO_DESEJADO)
    # Opção 2: Baixar mês mais recente (defina USAR_MES_RECENTE como True)
    
    # Defina apenas um dos modos abaixo:
    MODO_MES_ESPECIFICO = False  # Se True, usará MES_DESEJADO e ANO_DESEJADO
    USAR_MES_RECENTE = True      # Se True, buscará o mês mais recente disponível
    
    # Valores usados apenas se MODO_MES_ESPECIFICO for True
    MES_DESEJADO = 1
    ANO_DESEJADO = 2025
    
    try:
        if MODO_MES_ESPECIFICO:
            processar_todas_empresas(MES_DESEJADO, ANO_DESEJADO, False)
            logging.info(f"Processamento de todas as empresas finalizado para {MES_DESEJADO:02d}/{ANO_DESEJADO}!")
        else:
            processar_todas_empresas(None, None, USAR_MES_RECENTE)
            logging.info("Processamento de todas as empresas finalizado para o mês mais recente!")
    except Exception as e:
        logging.error(f"Erro no processamento geral: {str(e)}")
