from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configurações do ChromeDriver
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Descomente para executar em modo headless
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Iniciar o navegador usando o WebDriver Manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # Acessar a página de login
    driver.get("https://sintegre.ons.org.br/sites/1/18/paginas/servicos/historico-de-produtos.aspx")

    # Esperar até que o campo de nome de usuário esteja presente
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("tust@rioenergy.com.br")

    # Esperar até que o campo de senha esteja presente
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys("Ca2003@#")

    # Simular um pequeno atraso antes de clicar no botão de login
    time.sleep(2)

    # Submeter o formulário
    login_button = driver.find_element(By.ID, "kc-login")
    login_button.click()

    # Esperar um pouco para garantir que o login foi processado
    time.sleep(15)
    print("Procurando elemento baixar!")
    
    # Tentar localizar o elemento de diferentes formas
    try:
        # Tentativa 1: Por ID
        elemento = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "linkarquivo-455724"))
        )
    except:
        try:
            # Tentativa 2: Por classe
            elemento = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "default_btn_06918eef"))
            )
        except:
            try:
                # Tentativa 3: Por texto do link
                elemento = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Baixar"))
                )
            except:
                try:
                    # Tentativa 4: Por XPATH completo
                    elemento = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'EOLICA CAETITE')]"))
                    )
                except:
                    print("Não foi possível encontrar o elemento de download")
                    raise

    print("Elemento de download encontrado com sucesso")
    time.sleep(5)
    
    
    

finally:
    # Fechar o navegador
    driver.quit()
