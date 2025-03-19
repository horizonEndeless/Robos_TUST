from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import logging
import argparse

# Dicionário com todas as empresas organizadas por categoria
EMPRESAS = {
    "AE": [
        ('8011', 'LIBRA LIGAS DO BRASIL S/A', 'klebe1079', 'kl#b#1079'),
        ('3859', 'CELEO SAO JOAO DO PIAUI FV I S.A.', 'bruno1124', 'bruno1124'),
        ('3860', 'CELEO SAO JOAO DO PIAUI FV II S.A.', 'bruno1124', 'bruno1124'),
        ('3861', 'CELEO SAO JOAO DO PIAUI FV III S.A.', 'bruno1124', 'bruno1124'),
        ('3862', 'CELEO SAO JOAO DO PIAUI FV IV S.A.', 'bruno1124', 'bruno1124'),
        ('3863', 'CELEO SAO JOAO DO PIAUI FV V S.A.', 'bruno1124', 'bruno1124'),
        ('3864', 'CELEO SAO JOAO DO PIAUI FV VI S.A.', 'bruno1124', 'bruno1124'),
        ('3740', 'COREMAS I GERACAO DE ENERGIA SPE S.A.', 'anac1205', '@n@c1205'),
        ('3741', 'COREMAS II GERACAO DE ENERGIA II SPE S.A.', 'anac1205', '@n@c1205'),
        ('3750', 'COREMAS III GERACAO DE ENERGIA SPES.A.', 'anac1205', '@n@c1205'),
    ],
    "DE": [
        ('3748', 'DIAMANTE GERACAO DE ENERGIA LTDA', 'najla1447', 'n@jl@1447'),
    ],
    "RE": [
        ('3430', 'EOLICA CAETITE A S.A.', 'carol1758', 'c@rol1758'),
        ('3431', 'EOLICA CAETITE B S.A.', 'carol1758', 'c@rol1758'),
        ('3432', 'EOLICA CAETITE C S.A', 'carol1758', 'c@rol1758'),
        ('3497', 'EOLICA ITAREMA II S.A.', 'carol1758', 'c@rol1758'),
        ('3498', 'EOLICA ITAREMA V', 'carol1758', 'c@rol1758'),
        ('3502', 'EOLICA ITAREMA I S.A.', 'carol1758', 'c@rol1758'),
        ('3503', 'EOLICA ITAREMA III S.A.', 'carol1758', 'c@rol1758'),
        ('3530', 'EOLICA ITAREMA IV S.A.', 'carol1758', 'c@rol1758'),
        ('3531', 'EOLICA ITAREMA VI S.A.', 'carol1758', 'c@rol1758'),
        ('3532', 'EOLICA ITAREMA VII S.A.', 'carol1758', 'c@rol1758'),
        ('3537', 'EOLICA ITAREMA VIII S.A.', 'carol1758', 'c@rol1758'),
        ('3538', 'EOLICA ITAREMA IX S.A.', 'carol1758', 'c@rol1758'),
        ('3947', 'EOLICA SDB ALFA S.A.', 'carol1758', 'c@rol1758'),
        ('3948', 'EOLICA SDB B S.A.', 'carol1758', 'c@rol1758'),
        ('3969', 'EOLICA SDB C S.A.', 'carol1758', 'c@rol1758'),
        ('3970', 'EOLICA SDB D S.A.', 'carol1758', 'c@rol1758'),
        ('3972', 'EOLICA SDB F S.A.', 'carol1758', 'c@rol1758'),
        ('3976', 'EOLICA SDB ECO S.A', 'carol1758', 'c@rol1758'),
        ('4313', 'EOLICA BREJINHOS ALFA S.A', 'carol1758', 'c@rol1758'),
        ('4314', 'EOLICA BREJINHOS B S.A.', 'carol1758', 'c@rol1758'),
        ('4315', 'EOLICA CAETITE ECO S.A', 'carol1758', 'c@rol1758'),
        ('4316', 'EOLICA CAETITE F S.A.', 'carol1758', 'c@rol1758'),
        ('4415', 'EOLICA CAETITE D S.A.', 'carol1758', 'c@rol1758')
    ]
}

def setup_logger():
    """Configura e retorna o logger"""
    # Configurar o logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)

# Criar logger global
logger = setup_logger()

def create_download_dir(base_dir, cnpj, empresa_nome):
    """Cria diretório específico para a empresa"""
    empresa_nome = empresa_nome.replace('/', '-').replace('\\', '-').strip()
    download_dir = os.path.join(base_dir, f"CNPJ_{cnpj}", empresa_nome)
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    return download_dir

def processar_empresas(categorias):
    global logger
    
    # Lista para armazenar todas as empresas a serem processadas
    empresas_para_processar = []
    
    # Adicionar empresas das categorias selecionadas
    for categoria in categorias:
        if categoria in EMPRESAS:
            empresas_para_processar.extend([(codigo, nome, usuario, senha, categoria) 
                                           for codigo, nome, *credenciais in EMPRESAS[categoria]
                                           for usuario, senha in [credenciais if len(credenciais) == 2 else ('carol1758', 'c@rol1758')]])
    
    logger.info(f"Total de empresas a processar: {len(empresas_para_processar)}")
    
    for codigo_ons, nome_empresa, usuario, senha, categoria in empresas_para_processar:
        try:
            # Diretório base para downloads
            base_download_dir = os.path.join(r"C:\Users\Bruno\Downloads\TBE", categoria, codigo_ons)
            if not os.path.exists(base_download_dir):
                os.makedirs(base_download_dir)
            
            logger.info(f"\nIniciando processamento da empresa {nome_empresa} (Código ONS: {codigo_ons}, Categoria: {categoria})")
            
            # Configurar o driver do Chrome
            chrome_options = webdriver.ChromeOptions()
            prefs = {
                "download.default_directory": base_download_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            chrome_options.add_experimental_option("prefs", prefs)
            driver = webdriver.Chrome(options=chrome_options)
            
            try:
                # Abrir o site
                driver.get("https://portalcliente.tbenergia.com.br/")
                wait = WebDriverWait(driver, 10)
                
                # Login com credenciais específicas para cada empresa
                login_field = wait.until(EC.presence_of_element_located((By.NAME, "Login")))
                login_field.click()
                login_field.send_keys(usuario)
                
                # Senha
                senha_field = wait.until(EC.presence_of_element_located((By.NAME, "Senha")))
                senha_field.click()
                senha_field.send_keys(senha)
                
                # Botão de login
                login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
                login_button.click()
                
                # Aguardar a página de fechamento carregar
                wait.until(EC.url_to_be("https://portalcliente.tbenergia.com.br/Fechamento"))
                
                # Clicar no campo de seleção do Chosen
                chosen_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='CNPJ_chosen']/a/span")))
                chosen_field.click()
                
                # Clicar no campo de busca do Chosen
                search_field = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='CNPJ_chosen']/div/div/input")))
                search_field.click()
                
                # Selecionar a opção específica usando o código atual
                option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//*[@id='CNPJ_chosen']/div/ul/li[contains(text(), '{codigo_ons}')]")))
                option.click()
                
                time.sleep(2)
                
                # Clicar no botão Filtrar
                filtrar_button = wait.until(EC.element_to_be_clickable((By.ID, "BtnFiltrar")))
                filtrar_button.click()
                
                # Aguardar um momento para os dados carregarem
                time.sleep(3)
                
                # Aguardar a tabela de resultados carregar
                wait.until(EC.presence_of_element_located((By.ID, "NfRecentes")))
                
                # Inicializar contadores
                total_xmls = 0
                pagina_atual = 1
                empresas_processadas = set()
                
                logger.info("Iniciando processamento dos XMLs...")
                
                while True:
                    logger.info(f"\nProcessando página {pagina_atual}")
                   
                    xml_links = wait.until(EC.presence_of_all_elements_located(
                        (By.XPATH, "//table[@id='NfRecentes']//a[contains(text(), 'XML')]")))
                    rows = driver.find_elements(By.XPATH, "//table[@id='NfRecentes']/tbody/tr")
                   
                    logger.info(f"Encontrados {len(xml_links)} XMLs na página {pagina_atual}")
                   
                    for i, (row, link) in enumerate(zip(rows, xml_links), 1):
                        try:
                            # Obter informações da linha atual com o mapeamento correto
                            competencia = row.find_element(By.XPATH, "./td[1]").text    # Competência
                            nf_numero = row.find_element(By.XPATH, "./td[2]").text      # Nro. NF
                            cnpj_atual = row.find_element(By.XPATH, "./td[5]").text     # CNPJ (coluna 5)
                            empresa_atual = row.find_element(By.XPATH, "./td[4]").text  # Empresa do Grupo
                            valor = row.find_element(By.XPATH, "./td[6]").text          # R$ Valor
                           
                            # Limpar o CNPJ (remover caracteres especiais)
                            cnpj_atual = ''.join(filter(str.isdigit, cnpj_atual))
                           
                            # Log detalhado do download
                            logger.info(f"\nBaixando XML {i}/{len(xml_links)} da página {pagina_atual}")
                            logger.info(f"Transmissora: {empresa_atual}")
                            logger.info(f"CNPJ: {cnpj_atual}")
                            logger.info(f"NF: {nf_numero}")
                            logger.info(f"Competência: {competencia}")
                            logger.info(f"Valor: {valor}")
                           
                            # Se for uma nova transmissora, criar diretório específico
                            if (cnpj_atual, empresa_atual) not in empresas_processadas:
                                download_dir = create_download_dir(base_download_dir, cnpj_atual, empresa_atual)
                                driver.execute_cdp_cmd('Page.setDownloadBehavior', {
                                    'behavior': 'allow',
                                    'downloadPath': download_dir
                                })
                                empresas_processadas.add((cnpj_atual, empresa_atual))
                                logger.info(f"Nova transmissora detectada: {empresa_atual}")
                                logger.info(f"CNPJ: {cnpj_atual}")
                                logger.info(f"Criado diretório: {download_dir}")
 
                            # Download do XML
                            driver.execute_script("arguments[0].scrollIntoView(true);", link)
                            time.sleep(1)
                            link.click()
                            total_xmls += 1
                            logger.info(f"✓ Download iniciado com sucesso")
                           
                        except Exception as e:
                            logger.error(f"❌ Erro ao baixar XML na página {pagina_atual}: {str(e)}")
                            continue
                   
                    # Verificar se existe próxima página
                    try:
                        # Localizar o botão próximo
                        next_button = wait.until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "#NfRecentes_next:not(.disabled)")))
                       
                        # Rolar até o final da página para garantir que o botão de próximo está visível
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(1)
                       
                        # Verificar se o botão está habilitado
                        if "disabled" in next_button.get_attribute("class"):
                            logger.info("Chegou à última página")
                            break
                       
                        # Clicar no botão usando JavaScript
                        driver.execute_script("arguments[0].click();", next_button)
                       
                        # Aguardar a tabela atualizar
                        time.sleep(2)
                       
                    except Exception as e:
                        logger.error(f"Erro ao navegar para próxima página: {str(e)}")
                        break
               
                # Aguardar downloads finalizarem
                time.sleep(5)
               
            finally:
                driver.quit()
                logger.info(f"Finalizado processamento da empresa {nome_empresa}")
                time.sleep(5)  # Aguardar um pouco antes de processar a próxima empresa
                
        except Exception as e:
            logger.error(f"Erro ao processar empresa {nome_empresa}: {str(e)}")
            continue

def main():
    parser = argparse.ArgumentParser(description='Download de XMLs do Portal TBE Energia')
    parser.add_argument('--categorias', nargs='+', choices=['AE', 'DE', 'RE', 'TODAS'], 
                        default=['TODAS'], help='Categorias de empresas a processar (AE, DE, RE ou TODAS)')
    
    args = parser.parse_args()
    
    # Se TODAS for especificado, processar todas as categorias
    if 'TODAS' in args.categorias:
        categorias = ['AE', 'DE', 'RE']
    else:
        categorias = args.categorias
    
    logger.info(f"Iniciando processo de download de XMLs para as categorias: {', '.join(categorias)}")
    processar_empresas(categorias)
    logger.info("Processo finalizado")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Erro fatal: {str(e)}") 