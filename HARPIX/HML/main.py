from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def iniciar_automacao():
    driver = None
    try:
        logger.info("Iniciando automação...")
        
        # Configurar as opções do Chrome
        chrome_options = Options()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Inicializar o driver
        logger.info("Inicializando o Chrome WebDriver...")
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Definir tamanho da janela
        driver.set_window_size(1451, 984)
        logger.info("Tamanho da janela definido: 1451x984")
        
        # Acessar o site
        url = "https://harpixfat.mezenergia.com/FAT/open.do?sys=FAT"
        logger.info(f"Acessando URL: {url}")
        driver.get(url)
        
        # Mudar para o frame inicial
        logger.info("Mudando para o frame inicial (index=0)")
        driver.switch_to.frame(0)
        
        # Configurar wait
        wait = WebDriverWait(driver, 10)
        
        # Login
        logger.info("Tentando fazer login...")
        campo_input = wait.until(EC.presence_of_element_located(
            (By.ID, "WFRInput1051800")
        ))
        campo_input.clear()
        campo_input.send_keys("3748")
        logger.info("Código digitado: 3748")
        
        botao_entrar = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Entrar')]")
        ))
        botao_entrar.click()
        logger.info("Botão Entrar clicado")
        
        # Aguardar após login
        logger.info("Aguardando 10 segundos após o login...")
        time.sleep(10)
        
        # Voltar ao contexto padrão
        logger.info("Voltando ao contexto padrão da página")
        driver.switch_to.default_content()
        
        # Verificar frames disponíveis
        frames = driver.find_elements(By.TAG_NAME, "iframe")
        logger.info(f"Frames encontrados na página: {len(frames)}")
        for idx, frame in enumerate(frames):
            name = frame.get_attribute("name")
            src = frame.get_attribute("src")
            logger.info(f"Frame {idx}: name='{name}', src='{src}'")
        
        # Tentar acessar mainsystem
        logger.info("Tentando acessar frame 'mainsystem'...")
        wait = WebDriverWait(driver, 15)
        try:
            mainsystem_frame = wait.until(EC.presence_of_element_located(
                (By.NAME, "mainsystem")
            ))
            logger.info("Frame 'mainsystem' encontrado")
            driver.switch_to.frame(mainsystem_frame)
            logger.info("Mudou para frame 'mainsystem' com sucesso")
        except Exception as e:
            logger.error(f"Erro ao acessar frame 'mainsystem': {str(e)}")
            raise
        
        # Aguardar e verificar frames dentro de mainsystem
        logger.info("Verificando frames dentro de mainsystem...")
        time.sleep(5)  # Aguardar carregamento dos frames internos
        frames_internos = driver.find_elements(By.TAG_NAME, "iframe")
        for idx, frame in enumerate(frames_internos):
            name = frame.get_attribute("name")
            src = frame.get_attribute("src")
            logger.info(f"Frame interno {idx}: name='{name}', src='{src}'")
        
        # Tentar acessar mainform com mais tempo de espera
        logger.info("Tentando acessar frame 'mainform'...")
        wait = WebDriverWait(driver, 20)  # Aumentado para 20 segundos
        mainform_frame = wait.until(EC.presence_of_element_located(
            (By.NAME, "mainform")
        ))
        logger.info("Frame 'mainform' encontrado")
        driver.switch_to.frame(mainform_frame)
        logger.info("Mudou para frame 'mainform' com sucesso")
        
        # Continuar com o resto do código...
        logger.info("Tentando acessar outros frames e elementos...")
        
        # Frame com xpath específico
        form_frame = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//iframe[contains(@src, 'form.jsp?sys=FAT')]")
        ))
        driver.switch_to.frame(form_frame)
        
        # Voltar ao mainform
        driver.switch_to.parent_frame()
        mainform_frame = wait.until(EC.presence_of_element_located(
            (By.NAME, "mainform")
        ))
        driver.switch_to.frame(mainform_frame)
        
        # Clicar no elemento grid
        elemento_grid = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class, 'gridDarkAltCol')]//img[contains(@src, 'openImageStreamFromGal')]")
        ))
        elemento_grid.click()
        
        # Sequência de cliques nos botões
        botoes_ids = ['16', '19', '22', '25', '28']
        for id in botoes_ids:
            botao = wait.until(EC.element_to_be_clickable(
                (By.XPATH, f"//img[@id='grid1051940button{id}']")
            ))
            botao.click()
            time.sleep(1)
        
    except Exception as e:
        logger.error(f"Erro durante a execução: {str(e)}")
        import traceback
        logger.error(f"Detalhes do erro:\n{traceback.format_exc()}")
    finally:
        if driver:
            try:
                logger.info("Finalizando o driver...")
                time.sleep(3)
                driver.quit()
                logger.info("Driver finalizado com sucesso")
            except:
                logger.error("Erro ao finalizar o driver")

if __name__ == "__main__":
    iniciar_automacao()