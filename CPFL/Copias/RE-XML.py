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

def criar_estrutura_pastas(mes, ano):
    """
    Cria a estrutura de pastas necessária para os downloads
    """
    base_path = os.path.join(os.path.expanduser("~"), "Downloads", "CPFL", f"{mes:02d}_{ano}")
    
    # Cria a pasta base se não existir
    if not os.path.exists(base_path):
        os.makedirs(base_path)
        logging.info(f"Pasta criada: {base_path}")
    
    return base_path

def baixar_documentos(page, node_number, mes, ano):
    """
    Baixa os XMLs e PDFs de todas as notas fiscais do mês
    """
    try:
        # Cria estrutura de pastas
        base_path = criar_estrutura_pastas(mes, ano)
        
        # Aguarda as faturas carregarem
        time.sleep(2)
        
        # Localiza todas as faturas da CEEE T
        faturas = page.locator('text=CEEE T - Fatura')
        quantidade = faturas.count()
        
        if quantidade > 0:
            logging.info(f"Encontradas {quantidade} faturas para download")
            
            # Para cada fatura
            for i in range(quantidade):
                try:
                    # Extrai informações da fatura
                    fatura = faturas.nth(i)
                    texto_fatura = fatura.inner_text()
                    numero_fatura = texto_fatura.split('Nº: ')[1].split(' -')[0].strip()
                    logging.info(f"Processando fatura {numero_fatura} ({i+1} de {quantidade})")
                    
                    # Cria pasta específica para esta fatura
                    pasta_fatura = os.path.join(base_path, f"NF_{numero_fatura}")
                    if not os.path.exists(pasta_fatura):
                        os.makedirs(pasta_fatura)
                    
                    # Processo do XML (mantido como estava)
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
                    
                    # Processo do PDF (novo processo correto)
                    # Clica no span da fatura para expandir
                    span_selector = f'span[id="form:tree:n-0-{i}:TreeNode"]'
                    span_fatura = page.locator(span_selector)
                    if span_fatura.is_visible():
                        span_fatura.click()
                        time.sleep(2)
                        logging.info(f"Clicou na fatura para baixar PDF: {numero_fatura}")
                        
                        # Clica no ícone do PDF
                        pdf_selector = '#form\\:j_idt86'
                        pdf_button = page.locator(pdf_selector)
                        if pdf_button.is_visible():
                            with page.expect_download() as download_info:
                                pdf_button.click()
                            download = download_info.value
                            nome_arquivo_pdf = f"NF_{numero_fatura}.pdf"
                            caminho_pdf = os.path.join(pasta_fatura, nome_arquivo_pdf)
                            download.save_as(caminho_pdf)
                            logging.info(f"PDF salvo em: {caminho_pdf}")
                            time.sleep(1)
                        else:
                            logging.warning(f"Botão PDF não encontrado para fatura {numero_fatura}")
                            
                except Exception as e:
                    logging.error(f"Erro ao processar fatura {i+1}: {str(e)}")
                    continue
        else:
            logging.warning("Nenhuma fatura encontrada")
            
    except Exception as e:
        logging.error(f"Erro ao baixar documentos: {str(e)}")
        raise

def login_cpfl(cnpj: str, senha: str, mes=10, ano=2024):
    with sync_playwright() as p:
        try:
            # Inicia o navegador
            logging.info("Iniciando o navegador...")
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            # Acessa a página
            logging.info("Acessando a página da CPFL...")
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

            # Aguarda a página de faturas
            logging.info("Aguardando carregamento da página de faturas...")
            page.wait_for_selector('#form\\:j_idt63', timeout=30000)
            logging.info("Página de faturas carregada com sucesso!")

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
                        
                        # Baixa os XMLs e PDFs
                        baixar_documentos(page, node_number, mes, ano)

            time.sleep(5)  # Tempo para visualização
            browser.close()

        except Exception as e:
            logging.error(f"Erro durante a execução: {str(e)}")
            raise

if __name__ == "__main__":
    # Dados de acesso
    CNPJ = "33485728000100"
    SENHA = "Pontal!rsm24"
    
    # Para alterar o mês/ano, basta mudar estes valores
    MES_DESEJADO = 10
    ANO_DESEJADO = 2024
    
    try:
        login_cpfl(CNPJ, SENHA, MES_DESEJADO, ANO_DESEJADO)
        logging.info("Processo finalizado com sucesso!")
    except Exception as e:
        logging.error(f"Processo finalizado com erro: {str(e)}")
