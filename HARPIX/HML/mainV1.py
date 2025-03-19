from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

def iniciar_automacao():
    driver = None
    try:
        # Configurar as opções do Chrome
        chrome_options = Options()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Inicializar o driver
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Definir tamanho da janela (1451x984)
        driver.set_window_size(1451, 984)
        
        # Acessar o site
        url = "https://harpixfat.mezenergia.com/FAT/open.do?sys=FAT"
        driver.get(url)
        
        # Mudar para o frame correto (index=0)
        driver.switch_to.frame(0)
        
        # Aguardar e interagir com o campo de input
        wait = WebDriverWait(driver, 10)
        campo_input = wait.until(EC.presence_of_element_located(
            (By.ID, "WFRInput1051800")
        ))
        
        # Clicar no campo
        campo_input.click()
        
        # Digitar o valor
        campo_input.clear()
        campo_input.send_keys("3748")
        
        # Aguardar e clicar no botão Entrar (usando várias opções de localização)
        try:
            # Tentativa 1: Usando o texto do botão
            botao_entrar = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Entrar')]")
            ))
        except:
            try:
                # Tentativa 2: Usando a classe do botão
                botao_entrar = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button.w-100.p-0.align-items-center.btn")
                ))
            except:
                # Tentativa 3: Usando o ícone dentro do botão
                botao_entrar = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//i[contains(@class, 'fas fa-sign-in-alt')]/..")
                ))
        
        # Clicar no botão
        botao_entrar.click()
        
        time.sleep(2)  # Pequena pausa para visualizar as ações
        
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")
    finally:
        if driver:
            try:
                time.sleep(3)
                driver.quit()
            except:
                pass

if __name__ == "__main__":
    iniciar_automacao()